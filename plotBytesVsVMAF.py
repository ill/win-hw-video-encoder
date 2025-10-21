from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import itertools
import numpy as np
import matplotlib.patheffects as path_effects
from adjustText import adjust_text  # for completeness

# ======================================================
# Data classes & utilities
# ======================================================

@dataclass
class DimensionSettings:
    enable_1pass: bool = True
    enable_2pass: bool = True
    crf_range: Optional[Tuple[float, float]] = None
    gsun_range: Optional[Tuple[Optional[float], Optional[float]]] = None

@dataclass
class FileSettings:
    csv_file: str
    dims: Dict[Tuple[int, int], DimensionSettings] = field(default_factory=dict)
    label: Optional[str] = None
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


def clean_xticks(ax) -> np.ndarray:
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
    use_leader_lines: bool = True,     # kept for API compatibility
    normal_offset: float = 0.18,       # kept for API compatibility
    fast_interaction: bool = True,
    interaction_max_ticks: int = 8,
    debounce_ms: int = 80
):
    marker_cycle = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '<', '>', 'h', 'H', 'd', 'p', '|', '_', '+', 'x']

    # ======================================================
    # Data loading
    # ======================================================
    def build_plot_data(allow_fallback_all: bool = False):
        plot_data, legend_labels = [], []
        for fs in file_settings_list:
            csv_file = fs.csv_file
            label = fs.label or csv_file
            df = pd.read_csv(csv_file)

            df['file_bytes'] = df['file_bytes'].astype(str).str.replace(',', '', regex=False).astype(int)
            df['file_MB'] = df['file_bytes'] / 1_048_576
            df['crf'] = pd.to_numeric(df['crf'], errors='coerce')

            if 'actual_bitrate_bps' in df.columns:
                df['actual_bitrate_bps'] = (
                    df['actual_bitrate_bps'].astype(str).str.replace(',', '', regex=False)
                    .apply(lambda x: pd.to_numeric(x, errors='coerce'))
                )
            else:
                df['actual_bitrate_bps'] = np.nan

            if 'gsun' in df.columns:
                df['gsun'] = (
                    df['gsun'].astype(str).str.replace(',', '', regex=False)
                    .apply(lambda x: pd.to_numeric(x, errors='coerce'))
                )
            else:
                df['gsun'] = np.nan

            def pass_type(x):
                if pd.isna(x): return '1-pass'
                val = str(x).strip().lower()
                return '1-pass' if val in ('n/a', 'na', '') else '2-pass'
            df['pass_type'] = df['encoding_time_pass1_s'].apply(pass_type)

            dims = fs.dims
            if not dims:
                unique_dims = set(zip(df['width'], df['height']))
                dims = {dim: DimensionSettings() for dim in unique_dims}

            if allow_fallback_all:
                dims = {(-1, -1): DimensionSettings(enable_1pass=True, enable_2pass=True)}

            for (w, h), d in dims.items():
                if w >= 0 and h >= 0:
                    sub = df[(df['width'] == w) & (df['height'] == h)]
                    group_label = f"{label} | {w}x{h}"
                elif w >= 0 and h < 0:
                    sub = df[df['width'] == w]; group_label = f"{label} | width={w}"
                elif w < 0 and h >= 0:
                    sub = df[df['height'] == h]; group_label = f"{label} | height={h}"
                else:
                    sub = df; group_label = f"{label} | all"

                if d.crf_range:
                    lo, hi = d.crf_range
                    sub = sub[(sub['crf'] >= lo) & (sub['crf'] <= hi)]

                if d.gsun_range:
                    gmin, gmax = d.gsun_range
                    if gmin is not None: sub = sub[sub['gsun'] >= gmin]
                    if gmax is not None: sub = sub[sub['gsun'] <= gmax]

                passes = []
                if d.enable_1pass: passes.append('1-pass')
                if d.enable_2pass: passes.append('2-pass')
                sub = sub[sub['pass_type'].isin(passes)]
                if sub.empty:
                    continue

                for pt in passes:
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
                        'show_crf': fs.show_crf,
                        'show_gsun': fs.show_gsun,
                    })
                    legend_labels.append(f"{group_label} | {pt}")
        return plot_data, legend_labels

    plot_data, legend_labels = build_plot_data(allow_fallback_all=False)
    if not plot_data:
        plot_data, legend_labels = build_plot_data(allow_fallback_all=True)
        if not plot_data:
            raise ValueError("No plot data available. Check your filters and CSVs.")

    ordered_files = list(dict.fromkeys(p['file'] for p in plot_data))
    n_files = max(1, len(ordered_files))

    # ======================================================
    # Main plot
    # ======================================================
    colors = get_distinct_colors(len(plot_data))
    fig, ax = plt.subplots(figsize=(14, 9))
    marker_iter = itertools.cycle(marker_cycle)
    label_artists = []

    for i, pdict in enumerate(plot_data):
        color = colors[i]
        marker = next(marker_iter)
        ax.plot(
            pdict['file_MB'], pdict['vmaf'],
            color=color, marker=marker, linestyle='-',
            linewidth=2, markersize=7, label=legend_labels[i], alpha=0.9
        )

        # Labels directly on the dots
        for xi, yi, crf_val, gsun_val in zip(pdict['file_MB'], pdict['vmaf'], pdict['crf'], pdict['gsun']):
            parts = []
            if pdict.get('show_crf') and pd.notna(crf_val): parts.append(f"{int(crf_val)}")
            if pdict.get('show_gsun') and pd.notna(gsun_val): parts.append(f"{gsun_val:.2f}")
            if not parts: continue
            lbl = ", ".join(parts)
            txt = ax.text(xi, yi, lbl, fontsize=8, ha='center', va='center', color=color, zorder=10)
            txt.set_path_effects([
                path_effects.Stroke(linewidth=1.4, foreground='black'),
                path_effects.Normal()
            ])
            label_artists.append(txt)

    # ======================================================
    # Styling
    # ======================================================
    ax.set_xlabel("File Size (MB)")
    ax.set_ylabel("VMAF Mean")
    ax.set_title("Combined BD Curve (Grouped by File, (Width, Height), Pass Type)")
    ax.legend(fontsize=8, loc='best', ncol=2)

    # Fewer ticks while interacting for speed (tweakable)
    if fast_interaction:
        ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=interaction_max_ticks))
    else:
        ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=16))
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=12))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.grid(which='major', axis='both', linestyle='-', alpha=0.35)
    ax.grid(which='minor', axis='both', linestyle=':', alpha=0.25)
    ax.margins(x=0)
    ax.set_xlim(left=0)

    # ======================================================
    # Bitrate strip (fixed Kbps, derived from x-ticks and duration)
    # ======================================================
    panel_h_fig = 0.12 + 0.06 * (n_files - 1)
    gap_fig = 0.05
    plt.subplots_adjust(left=0.10, bottom=max(0.15, panel_h_fig + gap_fig + 0.06))
    axpos = ax.get_position()
    panel_rect = [axpos.x0, max(0.02, axpos.y0 - panel_h_fig - gap_fig), axpos.width, panel_h_fig]
    strip = fig.add_axes(panel_rect, sharex=ax)
    strip.set_ylim(0, n_files)
    strip.axis("off")

    # Resolve per-file duration (seconds) from any valid row: duration = file_bytes / actual_bitrate_bps
    durations_s: Dict[str, float] = {}
    for fname in ordered_files:
        duration = np.nan
        for s in (p for p in plot_data if p['file'] == fname):
            fb = s['file_MB'] * 1_048_576  # back to bytes
            br = s['bitrate']
            if fb is None or br is None or len(fb) == 0 or len(br) == 0:
                continue
            # find any index where both are finite
            mask = ~np.isnan(fb) & ~np.isnan(br)
            if mask.any():
                idx = np.flatnonzero(mask)[0]
                if br[idx] != 0:
                    duration = float(fb[idx] / br[idx])
                    break
        durations_s[fname] = duration

    # Create artists ONCE and just update them
    header_line = strip.plot([], [], lw=0.8, alpha=0.5)[0]
    row_lines, row_labels, tick_texts = [], [], []

    for row_idx, fname in enumerate(ordered_files):
        y_center = n_files - 1 - row_idx + 0.5
        row_line = strip.plot([], [], lw=0.4, alpha=0.25)[0]
        row_lines.append(row_line)
        row_label = strip.text(0, 0, f"{fname}: Actual bitrate (Kbps)", ha='left', va='center', fontsize=8)
        row_labels.append(row_label)
        tick_texts.append([])

    def _layout_static_parts():
        xmin, xmax = ax.get_xlim()
        header_line.set_data([xmin, xmax], [n_files, n_files])
        for row_idx in range(n_files):
            y_center = n_files - 1 - row_idx + 0.5
            row_lines[row_idx].set_data([xmin, xmax], [y_center, y_center])
            row_labels[row_idx].set_position((xmin, y_center + 0.35))

    _layout_static_parts()

    timer = fig.canvas.new_timer(interval=max(1, int(debounce_ms)))
    timer.single_shot = True

    def redraw_bitrate_panel():
        _layout_static_parts()
        tick_locs_MB = clean_xticks(ax)  # in MB, exactly the primary axis ticks
        bytes_per_MB = 1_048_576.0
        for row_idx, fname in enumerate(ordered_files):
            row_tick_texts = tick_texts[row_idx]
            # ensure we have the right number of text artists
            if len(row_tick_texts) < len(tick_locs_MB):
                for _ in range(len(tick_locs_MB) - len(row_tick_texts)):
                    row_tick_texts.append(strip.text(0, 0, "", ha='center', va='center', fontsize=7))
            elif len(row_tick_texts) > len(tick_locs_MB):
                for t in row_tick_texts[len(tick_locs_MB):]:
                    t.set_visible(False)

            dur = durations_s.get(fname, np.nan)
            y_center = n_files - 1 - row_idx + 0.5

            # Compute bitrate at each tick: bitrate(Kbps) = (size_bytes / duration_s) / 1_000
            if not np.isnan(dur) and dur > 0:
                br_kbps = (tick_locs_MB * bytes_per_MB / dur) / 1_000.0
            else:
                br_kbps = np.zeros_like(tick_locs_MB)

            for i, tick in enumerate(tick_locs_MB):
                txt = row_tick_texts[i]
                txt.set_visible(True)
                txt.set_position((tick, y_center - 0.1))
                txt.set_text(f"{br_kbps[i]:,.2f}")

    def _debounced_redraw(_=None):
        timer.stop()
        timer.start()

    def _on_timer():
        redraw_bitrate_panel()
        fig.canvas.draw_idle()

    timer.add_callback(_on_timer)
    redraw_bitrate_panel()

    # Keep panel synced and hide out-of-view labels
    def _on_limits_changed(event_ax):
        if event_ax is ax:
            _debounced_redraw()
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            for txt in label_artists:
                x, y = txt.get_position()
                txt.set_visible((xmin <= x <= xmax) and (ymin <= y <= ymax))
            fig.canvas.draw_idle()

    ax.callbacks.connect('xlim_changed', _on_limits_changed)
    ax.callbacks.connect('ylim_changed', _on_limits_changed)

    fig.savefig(output_filename, dpi=150, bbox_inches="tight")
    print(f"Saved plot to {output_filename}")
    if show_plot:
        plt.show()
    plt.close(fig)
