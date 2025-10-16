from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import numpy as np
import matplotlib.patheffects as path_effects

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
    """Return n visually distinct colors using matplotlib's tab20, tab20b, tab20c, and hsv if needed."""
    base_palettes = ['tab20', 'tab20b', 'tab20c']
    colors = []
    for palette in base_palettes:
        cmap = plt.get_cmap(palette)
        colors.extend([cmap(i) for i in range(cmap.N)])
    if n > len(colors):
        # Use HSV for even more colors
        hsv_colors = [plt.cm.hsv(i / n) for i in range(n - len(colors))]
        colors.extend(hsv_colors)
    return colors[:n]

def plot_combined_bd_class_dim(
    file_settings_list: List[FileSettings],
    output_filename: str,
    show_plot: bool = False
):
    """
    file_settings_list: List of FileSettings instances.
    output_filename: Path to save the combined plot.
    show_plot: Whether to display the plot interactively.
    """
    marker_cycle = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '<', '>', 'h', 'H', 'd', 'p', '|', '_', '+', 'x', '1', '2', '3', '4']
    plot_data = []
    legend_labels = []

    for file_idx, file_settings in enumerate(file_settings_list):
        csv_file = file_settings.csv_file
        label = file_settings.label or csv_file
        dims_settings = file_settings.dims

        df = pd.read_csv(csv_file, sep=',')
        df['file_bytes'] = df['file_bytes'].astype(str).str.replace(',', '')
        df['file_MB'] = df['file_bytes'].astype(int) / 1_048_576
        df['crf'] = pd.to_numeric(df['crf'], errors='coerce')

        # Robust pass type detection
        def detect_pass_type(x):
            if pd.isna(x):
                return '1-pass'
            val = str(x).strip().lower()
            if val in ('n/a', 'na', ''):
                return '1-pass'
            return '2-pass'
        df['pass_type'] = df['encoding_time_pass1_s'].apply(detect_pass_type)

        # If dims dict is empty, use all (width, height) pairs with defaults
        if not dims_settings:
            unique_dims = set(zip(df['width'], df['height']))
            dims_settings = {dim: DimensionSettings() for dim in unique_dims}

        for (width, height), dsettings in dims_settings.items():
            # Filtering logic
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
                # Both negative: all data
                sub = df
                group_label = f"{label} | all"

            # Pass type filtering
            pass_types = []
            if dsettings.enable_1pass:
                pass_types.append('1-pass')
            if dsettings.enable_2pass:
                pass_types.append('2-pass')
            sub = sub[sub['pass_type'].isin(pass_types)]

            # CRF range filtering
            if dsettings.crf_range is not None:
                min_crf, max_crf = dsettings.crf_range
                sub = sub[(sub['crf'] >= min_crf) & (sub['crf'] <= max_crf)]
            if sub.empty:
                continue

            for pass_type in pass_types:
                group = sub[sub['pass_type'] == pass_type]
                if group.empty:
                    continue
                # Sort by file_MB for line plotting
                sort_idx = np.argsort(group['file_MB'].values)
                plot_data.append({
                    'file': label,
                    'dim': (width, height),
                    'pass_type': pass_type,
                    'file_MB': group['file_MB'].values[sort_idx],
                    'vmaf_mean': group['vmaf_mean'].values[sort_idx],
                    'crf': group['crf'].values[sort_idx]
                })
                legend_labels.append(f"{group_label} | {pass_type}")

    n_groups = len(plot_data)
    colors = get_distinct_colors(n_groups)
    marker_iter = itertools.cycle(marker_cycle)

    fig, ax = plt.subplots(figsize=(14, 9))
    for i, pdict in enumerate(plot_data):
        color = colors[i]
        marker = next(marker_iter)
        # Draw lines between points
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
        # Draw scatter points (for emphasis)
        ax.scatter(
            pdict['file_MB'],
            pdict['vmaf_mean'],
            color=color,
            marker=marker,
            edgecolor='black',
            s=80,
            alpha=0.95
        )
        # Label each point with its CRF value in white with a black outline for contrast
        for x, y, crf in zip(pdict['file_MB'], pdict['vmaf_mean'], pdict['crf']):
            txt = ax.text(
                x, y, str(int(crf)),
                fontsize=8, ha='left', va='bottom', color='white', zorder=10
            )
            txt.set_path_effects([
                path_effects.Stroke(linewidth=1.5, foreground='black'),
                path_effects.Normal()
            ])

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
        show_plot=True
    )