from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import itertools
import numpy as np
import matplotlib.patheffects as path_effects
from adjustText import adjust_text  # pip install adjustText

# ======================================================
# Data classes & utilities
# ======================================================

@dataclass
class DimensionSettings:
    enable_1pass: bool = True
    enable_2pass: bool = True
    crf_range: Optional[Tuple[float, float]] = None  # (min_crf, max_crf)
    gsun_range: Optional[Tuple[Optional[float], Optional[float]]] = None  # (min_gsun, max_gsun)

@dataclass
class FileSettings:
    csv_file: str
    # Key: (width, height). Use -1 for width or height to mean "all".
    dims: Dict[Tuple[int, int], DimensionSettings] = field(default_factory=dict)
    label: Optional[str] = None
    # Per-file label toggles (default off)
    show_crf: bool = False
    show_gsun: bool = False

def get_distinct_colors(n: int):
    base_palettes = ['tab20', 'tab20b', 'tab20c']
    colors = []
    for palette in base_palettes:
        cmap = plt.get_cmap(palette)
        colors.extend([cmap(i) for i in range(cmap.N)])
    if n > len(colors):
        remaining = max(0, n - len(colors))
        hsv_colors = [plt.cm.hsv(i / max(1, remaining)) for i in range(remaining)]
        colors.extend(hsv_colors)
    return colors[:n]

def format_bytes(num_bytes: float):
    num_bytes = float(num_bytes)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num_bytes < 1000:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1000
    return f"{num_bytes:.1f} PB"

def compute_normals(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    n = len(x)
    dx = np.zeros(n)
    dy = np.zeros(n)
    if n > 1:
        dx[1:-1] = (x[2:] - x[:-2]) / 2
        dy[1:-1] = (y[2:] - y[:-2]) / 2
        dx[0] = x[1] - x[0]
        dy[0] = y[1] - y[0]
        dx[-1] = x[-1] - x[-2]
        dy[-1] = y[-1] - y[-2]
    norm = np.sqrt(dx**2 + dy**2)
    norm[norm == 0] = 1
    return -dy / norm, dx / norm

def pick_bitrate_unit(values: np.ndarray) -> Tuple[float, str]:
    """Pick a consistent bitrate unit for a row. Returns (scale_divisor, unit_label)."""
    if values is None or len(values) == 0 or np.all(np.isnan(values)):
        return 1.0, "bps"
    vmax = float(np.nanmax(values))
    if vmax >= 1e9:
        return 1e9, "Gbps"
    if vmax >= 1e6:
        return 1e6, "Mbps"
    if vmax >= 1e3:
        return 1e3, "Kbps"
    return 1.0, "bps"

def clean_xticks(ax) -> np.ndarray:
    """Return unique tick locations within xlim to avoid a duplicate rightmost tick."""
    xmin, xmax = ax.get_xlim()
    ticks = np.asarray(ax.get_xticks(), dtype=float)
    eps = (xmax - xmin) * 1e-9 if xmax > xmin else 1e-9
    ticks = ticks[(ticks >= xmin - eps) & (ticks <= xmax + eps)]
    ticks_sorted = np.sort(ticks)
    dedup = []
    for t in ticks_sorted:
        if not dedup or not np.isclose(t, dedup[-1], rtol=0, atol=max(abs(xmax - xmin), 1.0) * 1e-12):
            dedup.append(t)
    dedup = [t for t in dedup if t <= xmax + eps]
    return np.array(dedup, dtype=float)

# ======================================================
# Main plotting function
# ======================================================

def plot_combined_bd_class_dim(
    file_settings_list: List[FileSettings],
    output_filename: str,
    show_plot: bool = False,
    use_leader_lines: bool = True,   # kept for API parity; ignored for text placement now
    normal_offset: float = 0.18      # kept for API parity; not used for text placement
):
    marker_cycle = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '<', '>', 'h', 'H', 'd', 'p', '|', '_', '+', 'x', '1', '2', '3', '4']

    def build_plot_data(allow_fallback_all: bool = False):
        plot_data, legend_labels = [], []
        for fs in file_settings_list:
            csv_file = fs.csv_file
            label = fs.label or csv_file
            df = pd.read_csv(csv_file)

            # numeric cleanup (handle commas)
            df['file_bytes'] = df['file_bytes'].astype(str).str.replace(',', '', regex=False).astype(int)
            df['file_MB'] = df['file_bytes'] / 1_048_576
            df['crf'] = pd.to_numeric(df['crf'], errors='coerce')

            # parse bitrate (already in CSV per your data)
            if 'actual_bitrate_bps' in df.columns:
                df['actual_bitrate_bps'] = (
                    df['actual_bitrate_bps'].astype(str).str.replace(',', '', regex=False)
                    .apply(lambda x: pd.to_numeric(x, errors='coerce'))
                )
            else:
                df['actual_bitrate_bps'] = np.nan

            # parse GSUN if present
            if 'gsun' in df.columns:
                df['gsun'] = (
                    df['gsun'].astype(str).str.replace(',', '', regex=False)
                    .apply(lambda x: pd.to_numeric(x, errors='coerce'))
                )
            else:
                df['gsun'] = np.nan

            # pass type detection
            def pass_type(x):
                if pd.isna(x):
                    return '1-pass'
                val = str(x).strip().lower()
                if val in ('n/a', 'na', ''):
                    return '1-pass'
                return '2-pass'
            df['pass_type'] = df['encoding_time_pass1_s'].apply(pass_type)

            # prepare dims (wildcard support)
            dims = fs.dims
            if not dims:
                unique_dims = set(zip(df['width'], df['height']))
                dims = {dim: DimensionSettings() for dim in unique_dims}

            # if fallback requested, override dims to "all"
            if allow_fallback_all:
                dims = {(-1, -1): DimensionSettings(
                    enable_1pass=True, enable_2pass=True, crf_range=None, gsun_range=None
                )}

            # iterate dims and pass types
            for (w, h), d in dims.items():
                if w >= 0 and h >= 0:
                    sub = df[(df['width'] == w) & (df['height'] == h)]
                    group_label = f"{label} | {w}x{h}"
                elif w >= 0 and h < 0:
                    sub = df[df['width'] == w]
                    group_label = f"{label} | width={w}"
                elif w < 0 and h >= 0:
                    sub = df[df['height'] == h]
                    group_label = f"{label} | height={h}"
                else:
                    sub = df
                    group_label = f"{label} | all"

                # apply CRF range if provided
                if d.crf_range is not None:
                    lo, hi = d.crf_range
                    sub = sub[(sub['crf'] >= lo) & (sub['crf'] <= hi)]

                # apply GSUN range if provided (each bound optional)
                if d.gsun_range is not None:
                    gmin, gmax = d.gsun_range
                    if gmin is not None:
                        sub = sub[sub['gsun'] >= gmin]
                    if gmax is not None:
                        sub = sub[sub['gsun'] <= gmax]

                # pass filter
                pass_types: List[str] = []
                if d.enable_1pass:
                    pass_types.append('1-pass')
                if d.enable_2pass:
                    pass_types.append('2-pass')

                sub = sub[sub['pass_type'].isin(pass_types)]
                if sub.empty:
                    continue

                for pt in pass_types:
                    g = sub[sub['pass_type'] == pt].sort_values('file_MB')
                    if g.empty:
                        continue
                    plot_data.append({
                        'file': label,
                        'dim': (w, h),
                        'pass': pt,
                        'file_MB': g['file_MB'].values,
                        'vmaf': g['vmaf_mean'].values,
                        'crf': g['crf'].values,
                        'bitrate': g['actual_bitrate_bps'].values,
                        'gsun': g['gsun'].values,
                        # per-file label toggles snapshot
                        'show_crf': fs.show_crf,
                        'show_gsun': fs.show_gsun,
                    })
                    legend_labels.append(f"{group_label} | {pt}")
        return plot_data, legend_labels

    # Build data
    plot_data, legend_labels = build_plot_data(allow_fallback_all=False)
    if not plot_data:
        plot_data, legend_labels = build_plot_data(allow_fallback_all=True)
        if not plot_data:
            raise ValueError("No plot data available (even after fallback). Check your filters and CSVs.")

    # ordering of file rows (first-seen)
    ordered_files: List[str] = []
    for pdict in plot_data:
        if pdict['file'] not in ordered_files:
            ordered_files.append(pdict['file'])
    n_files = max(1, len(ordered_files))

    # ---------- Draw main plot ----------
    colors = get_distinct_colors(len(plot_data))
    fig, ax = plt.subplots(figsize=(14, 9))
    marker_iter = itertools.cycle(marker_cycle)

    for i, pdict in enumerate(plot_data):
        color = colors[i]
        marker = next(marker_iter)
        ax.plot(
            pdict['file_MB'],
            pdict['vmaf'],
            color=color,
            marker=marker,
            linestyle='-',
            linewidth=2,
            markersize=7,
            label=legend_labels[i],
            alpha=0.9
        )

        # Per-dot labels (comma-separated, numbers only), aligned exactly at the dot (no offset)
        for xi, yi, crf_val, gsun_val in zip(
            pdict['file_MB'], pdict['vmaf'], pdict['crf'], pdict['gsun']
        ):
            parts = []
            if pdict.get('show_crf', False) and pd.notna(crf_val):
                parts.append(f"{int(crf_val)}")
            if pdict.get('show_gsun', False) and pd.notna(gsun_val):
                parts.append(f"{gsun_val:.2f}")
            if not parts:
                continue
            label_str = ", ".join(parts)
            # place text exactly at the data point; no leader lines when labels are not offset
            txt = ax.text(
                xi, yi, label_str,
                fontsize=8, ha='center', va='center', color=color, zorder=10
            )
            txt.set_path_effects([
                path_effects.Stroke(linewidth=1.4, foreground='black'),
                path_effects.Normal()
            ])
            # No leader line drawn because there is no displacement

    # ---------- Style ----------
    ax.set_xlabel("File Size (MB)")
    ax.set_ylabel("VMAF Mean")
    ax.set_title("Combined BD Curve (Grouped by File, (Width, Height), Pass Type)")
    ax.legend(fontsize=8, loc='best', ncol=2)

    ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=16))
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=12))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.grid(which='major', axis='both', linestyle='-', alpha=0.35)
    ax.grid(which='minor', axis='both', linestyle=':', alpha=0.25)
    ax.margins(x=0)
    ax.set_xlim(left=0)

    # compute clean tick locations after limits are final
    tick_locs = clean_xticks(ax)

    # ---------- Reserve space and place the bitrate panel below the main axis ----------
    panel_h_fig = 0.12 + 0.06 * (n_files - 1)  # panel height scales with number of files
    gap_fig = 0.05                              # extra gap between main axis and panel
    plt.subplots_adjust(left=0.10, bottom=max(0.15, panel_h_fig + gap_fig + 0.06))

    # Recompute main axis position after subplots_adjust
    axpos = ax.get_position()  # in figure coords (x0, y0, x1, y1)
    panel_rect = [axpos.x0, max(0.02, axpos.y0 - panel_h_fig - gap_fig), axpos.width, panel_h_fig]
    strip = plt.gcf().add_axes(panel_rect)
    xmin, xmax = ax.get_xlim()
    strip.set_xlim([xmin, xmax])
    strip.set_ylim(0, n_files)
    strip.axis("off")

    # Header separator
    strip.plot([xmin, xmax], [n_files, n_files], lw=0.8, alpha=0.5)

    # ---------- Multi-row bitrate panel (tick-aligned) ----------
    for row_idx, fname in enumerate(ordered_files):
        y_center = n_files - 1 - row_idx + 0.5
        # subtle row rule
        strip.plot([xmin, xmax], [y_center, y_center], lw=0.4, alpha=0.25)

        # Collect all bitrates for this file to pick a stable unit
        file_series = [p for p in plot_data if p['file'] == fname]
        all_vals = np.concatenate(
            [s['bitrate'] for s in file_series if s['bitrate'] is not None and len(s['bitrate']) > 0]
        ) if file_series else np.array([])
        scale, unit = pick_bitrate_unit(all_vals)

        # Row label with units
        strip.text(xmin, y_center + 0.35, f"{fname}: Actual bitrate ({unit})",
                   ha='left', va='center', fontsize=8)

        # For each x tick, find the nearest point from each series; average their bitrates
        for tick in tick_locs:
            candidates = []
            for series in file_series:
                xs = series['file_MB']
                bs = series['bitrate']
                if len(xs) == 0 or len(bs) == 0 or np.all(np.isnan(bs)):
                    continue
                idx_min = int(np.argmin(np.abs(xs - tick)))
                val = bs[idx_min]
                if not np.isnan(val):
                    candidates.append(val)
            if candidates:
                avg_bps = float(np.nanmean(candidates))
                scaled = avg_bps / scale if scale else avg_bps
                strip.text(tick, y_center - 0.1, f"{scaled:,.2f}",
                           ha='center', va='center', fontsize=7)

    # ---------- Save / show ----------
    plt.gcf().savefig(output_filename, dpi=150, bbox_inches="tight")
    print(f"Saved plot to {output_filename}")
    if show_plot:
        plt.show()
    plt.close(plt.gcf())





# Example usage:
# Plot all widths:
# plot_bd('your_file.csv', min_crf=18, max_crf=42)
# Plot a specific width:
# plot_bd('your_file.csv', width=1920, min_crf=18, max_crf=42)

#plot_bd('Out/CRF/sonichd/sonichd-CRF.csv', min_crf=18, max_crf=42)

#plot_bd('Out/CRF/sonichd/sonichd-CRF.csv', min_crf=18, max_crf=42)


def highGraphs():
    # Define your settings using the classes
    file_structs = [
        # FileSettings(
        #     csv_file='Out/CRF/sonichd/sonichd-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='SonicHD'
        # ),
        # FileSettings(
        #     csv_file='Out/CRF/badminton/badminton-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='badminton'
        # ),
        # FileSettings(
        #     csv_file='Out/CRF/1440p-av1-42sec/1440p-av1-42sec-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='1440p-av1-42sec'
        # ),
        # FileSettings(
        #     csv_file='Out/CRF/steal-a-brainrot/steal-a-brainrot-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (960, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='steal-a-brainrot'
        # ),
        FileSettings(
            csv_file='Out/CQGoogleGSunExperiment/bipbop15_270_mono/bipbop15_270_mono-CQGoogleGSunExperiment.csv',
            dims={
                (480, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (160, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
            },
            label='bipbop15_270_mono',
            show_gsun=True,
            show_crf=True,
        ),
    ]

    plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

def lowMotionGraphs():
    # Define your settings using the classes
    file_structs = [
        FileSettings(
            csv_file='Out--Latest/CRF-Backup/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CRF.csv',
            dims={
                (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(8, 42))
            },
            label='Halo_NoMotion_20sec_1080p'
        )
    ]

    plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        output_filename='combined_low_motion_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

def highGraphs_gsun():
    # Define your settings using the classes
    file_structs = [
        FileSettings(
            csv_file='Out/CQGoogleGSunExperiment/bipbop15_270_mono/bipbop15_270_mono-CQGoogleGSunExperiment.csv',
            dims={
                (480, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (160, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
            },
            label='bipbop15_270_mono'
        ),
        # FileSettings(
        #     csv_file='Out/CRF/badminton/badminton-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='badminton'
        # ),
        # FileSettings(
        #     csv_file='Out/CRF/1440p-av1-42sec/1440p-av1-42sec-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='1440p-av1-42sec'
        # ),
        # FileSettings(
        #     csv_file='Out/CRF/steal-a-brainrot/steal-a-brainrot-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (960, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='steal-a-brainrot'
        # ),
    ]

    plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

if __name__ == "__main__":
    highGraphs()

    #lowMotionGraphs()

    #sonichdGraphs()
