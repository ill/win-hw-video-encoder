from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import itertools
import numpy as np
import matplotlib.patheffects as path_effects
from adjustText import adjust_text  # <-- Correct import

@dataclass
class DimensionSettings:
    enable_1pass: bool = True
    enable_2pass: bool = True
    crf_range: Optional[Tuple[float, float]] = None  # (min_crf, max_crf) or None

@dataclass
class FileSettings:
    csv_file: str
    # Key: (width, height) tuple. Use -1 for width or height to mean "all".
    dims: Dict[Tuple[int, int], DimensionSettings] = field(default_factory=dict)
    label: Optional[str] = None  # Optional label for legend; defaults to csv_file if not set

def get_distinct_colors(n):
    base_palettes = ['tab20', 'tab20b', 'tab20c']
    colors = []
    for palette in base_palettes:
        cmap = plt.get_cmap(palette)
        colors.extend([cmap(i) for i in range(cmap.N)])
    if n > len(colors):
        hsv_colors = [plt.cm.hsv(i / n) for i in range(n - len(colors))]
        colors.extend(hsv_colors)
    return colors[:n]

def format_bytes(num_bytes):
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
    dx[1:-1] = (x[2:] - x[:-2]) / 2
    dy[1:-1] = (y[2:] - y[:-2]) / 2
    dx[0] = x[1] - x[0]
    dy[0] = y[1] - y[0]
    dx[-1] = x[-1] - x[-2]
    dy[-1] = y[-1] - y[-2]
    norm = np.sqrt(dx**2 + dy**2)
    norm[norm == 0] = 1
    nx = -dy / norm
    ny = dx / norm
    return nx, ny

def plot_combined_bd_class_dim(
    file_settings_list: List[FileSettings],
    output_filename: str,
    show_plot: bool = False,
    use_leader_lines: bool = True,
    show_crf: bool = True,
    show_filesize: bool = True,
    normal_offset: float = 0.18  # Offset distance along normal (in data units)
):
    marker_cycle = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '<', '>', 'h', 'H', 'd', 'p', '|', '_', '+', 'x', '1', '2', '3', '4']
    plot_data = []
    legend_labels = []

    for file_idx, file_settings in enumerate(file_settings_list):
        csv_file = file_settings.csv_file
        label = file_settings.label or csv_file
        dims_settings = file_settings.dims

        df = pd.read_csv(csv_file, sep=',')
        df['file_bytes_raw'] = df['file_bytes'].astype(str).str.replace(',', '')
        df['file_bytes'] = df['file_bytes_raw'].astype(int)
        df['file_MB'] = df['file_bytes'] / 1_048_576
        df['crf'] = pd.to_numeric(df['crf'], errors='coerce')

        def detect_pass_type(x):
            if pd.isna(x):
                return '1-pass'
            val = str(x).strip().lower()
            if val in ('n/a', 'na', ''):
                return '1-pass'
            return '2-pass'
        df['pass_type'] = df['encoding_time_pass1_s'].apply(detect_pass_type)

        if not dims_settings:
            unique_dims = set(zip(df['width'], df['height']))
            dims_settings = {dim: DimensionSettings() for dim in unique_dims}

        for (width, height), dsettings in dims_settings.items():
            if width >= 0 and height >= 0:
                sub = df[(df['width'] == width) & (df['height'] == height)]
                group_label = f"{label} | {width}x{height}"
            elif width >= 0 and height < 0:
                sub = df[df['width'] == width]
                group_label = f"{label} | width={width}"
            elif width < 0 and height >= 0:
                sub = df[df['height'] == height]
                group_label = f"{label} | height={height}"
            else:
                sub = df
                group_label = f"{label} | all"

            pass_types = []
            if dsettings.enable_1pass:
                pass_types.append('1-pass')
            if dsettings.enable_2pass:
                pass_types.append('2-pass')
            sub = sub[sub['pass_type'].isin(pass_types)]

            if dsettings.crf_range is not None:
                min_crf, max_crf = dsettings.crf_range
                sub = sub[(sub['crf'] >= min_crf) & (sub['crf'] <= max_crf)]
            if sub.empty:
                continue

            for pass_type in pass_types:
                group = sub[sub['pass_type'] == pass_type]
                if group.empty:
                    continue
                sort_idx = np.argsort(group['file_MB'].values)
                plot_data.append({
                    'file': label,
                    'dim': (width, height),
                    'pass_type': pass_type,
                    'file_MB': group['file_MB'].values[sort_idx],
                    'vmaf_mean': group['vmaf_mean'].values[sort_idx],
                    'crf': group['crf'].values[sort_idx],
                    'file_bytes': group['file_bytes'].values[sort_idx]
                })
                legend_labels.append(f"{group_label} | {pass_type}")

    n_groups = len(plot_data)
    colors = get_distinct_colors(n_groups)
    marker_iter = itertools.cycle(marker_cycle)

    fig, ax = plt.subplots(figsize=(14, 9))

    if use_leader_lines:
        all_texts = []
        all_label_points = []
        all_label_colors = []

        for i, pdict in enumerate(plot_data):
            color = colors[i]
            marker = next(marker_iter)
            ax.plot(
                pdict['file_MB'],
                pdict['vmaf_mean'],
                color=color,
                marker=marker,
                linestyle='-',
                linewidth=2,
                markersize=8,
                label=legend_labels[i],
                alpha=0.85
            )
            ax.scatter(
                pdict['file_MB'],
                pdict['vmaf_mean'],
                color=color,
                marker=marker,
                edgecolor='black',
                s=80,
                alpha=0.95
            )
            x = np.array(pdict['file_MB'])
            y = np.array(pdict['vmaf_mean'])
            nx, ny = compute_normals(x, y)
            texts = []
            label_points = []
            label_colors = []
            for idx, (xi, yi, nxi, nyi, crf, file_bytes) in enumerate(zip(x, y, nx, ny, pdict['crf'], pdict['file_bytes'])):
                label_parts = []
                if show_crf:
                    label_parts.append(f"{int(crf)}")
                if show_filesize:
                    label_parts.append(f"({format_bytes(file_bytes)})")
                label_str = " ".join(label_parts)
                lx = xi + normal_offset * nxi
                ly = yi + normal_offset * nyi
                txt = ax.text(
                    lx, ly, label_str,
                    fontsize=8, ha='left', va='bottom', color=color, zorder=10
                )
                txt.set_path_effects([
                    path_effects.Stroke(linewidth=1.5, foreground='black'),
                    path_effects.Normal()
                ])
                texts.append(txt)
                label_points.append((xi, yi))
                label_colors.append(color)
            # Per-group adjustText to minimize intra-group overlap and line crossings
            adjust_text(
                texts,
                ax=ax,
                expand_points=(1.2, 1.2),
                expand_text=(1.2, 1.2),
                force_text=(0.5, 0.5),
                only_move={'points':'none', 'text':'xy'},
                arrowprops=None
            )
            all_texts.extend(texts)
            all_label_points.extend(label_points)
            all_label_colors.extend(label_colors)

        # Global adjustText pass to resolve any remaining inter-group overlaps
        adjust_text(
            all_texts,
            ax=ax,
            expand_points=(1.1, 1.1),
            expand_text=(1.1, 1.1),
            force_text=(0.2, 0.2),
            only_move={'points':'none', 'text':'xy'},
            arrowprops=None
        )
        # Draw leader lines in the correct color, from point to label
        for txt, (x, y), color in zip(all_texts, all_label_points, all_label_colors):
            label_pos = txt.get_position()
            ax.plot([x, label_pos[0]], [y, label_pos[1]], color=color, lw=1, alpha=0.8, zorder=9)
    else:
        for i, pdict in enumerate(plot_data):
            color = colors[i]
            marker = next(marker_iter)
            ax.plot(
                pdict['file_MB'],
                pdict['vmaf_mean'],
                color=color,
                marker=marker,
                linestyle='-',
                linewidth=2,
                markersize=8,
                label=legend_labels[i],
                alpha=0.85
            )
            ax.scatter(
                pdict['file_MB'],
                pdict['vmaf_mean'],
                color=color,
                marker=marker,
                edgecolor='black',
                s=80,
                alpha=0.95
            )
            for x, y, crf, file_bytes in zip(pdict['file_MB'], pdict['vmaf_mean'], pdict['crf'], pdict['file_bytes']):
                label_parts = []
                if show_crf:
                    label_parts.append(f"{int(crf)}")
                if show_filesize:
                    label_parts.append(f"({format_bytes(file_bytes)})")
                label_str = " ".join(label_parts)
                txt = ax.text(
                    x + 0.03, y + 0.03, label_str,
                    fontsize=8, ha='left', va='bottom', color=color, zorder=10
                )
                txt.set_path_effects([
                    path_effects.Stroke(linewidth=1.5, foreground='black'),
                    path_effects.Normal()
                ])

    # X-axis and Y-axis formatting for more subdivisions and less left padding
    ax.xaxis.set_major_locator(mticker.MaxNLocator(nbins=16))
    ax.xaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.grid(which='major', axis='x', linestyle='-', alpha=0.5)
    ax.grid(which='minor', axis='x', linestyle=':', alpha=0.3)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(nbins=12))
    ax.yaxis.set_minor_locator(mticker.AutoMinorLocator(2))
    ax.grid(which='major', axis='y', linestyle='-', alpha=0.5)
    ax.grid(which='minor', axis='y', linestyle=':', alpha=0.3)
    ax.margins(x=0)
    plt.subplots_adjust(left=0.10)
    ax.set_xlim(left=0)

    ax.set_xlabel('File Size (MB)')
    ax.set_ylabel('VMAF Mean')
    ax.set_title('Combined BD Curve (Grouped by File, (Width, Height), Pass Type)')
    ax.legend(fontsize=8, loc='best', ncol=2)
    plt.tight_layout()

    fig.savefig(output_filename)
    print(f"Saved plot to {output_filename}")
    if show_plot:
        plt.show()
    plt.close(fig)

# Example usage:
# Plot all widths:
# plot_bd('your_file.csv', min_crf=18, max_crf=42)
# Plot a specific width:
# plot_bd('your_file.csv', width=1920, min_crf=18, max_crf=42)

#plot_bd('Out/CRF/sonichd/sonichd-CRF.csv', min_crf=18, max_crf=42)

#plot_bd('Out/CRF/sonichd/sonichd-CRF.csv', min_crf=18, max_crf=42)


if __name__ == "__main__":
    # Define your settings using the classes
    file_structs = [
        FileSettings(
            csv_file='Out--Latest/CRF-Backup/sonichd/sonichd-CRF.csv',
            dims={
                (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (640, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 54))
            },
            label='SonicHD'
        ),
        FileSettings(
            csv_file='Out--Latest/CRF-Backup/badminton/badminton-CRF.csv',
            dims={
                (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (640, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 54))
            },
            label='Badminton'
        ),
        # FileSettings(
        #     csv_file='Out/CRF/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CRF.csv',
        #     widths={
        #         1920: WidthSettings(enable_1pass=False, crf_range=(8, 42))
        #     },
        #     label='Halo_NoMotion_20sec_1080p'
        # )
    ]

    plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=True,
        show_crf=False,
        show_filesize=True
    )