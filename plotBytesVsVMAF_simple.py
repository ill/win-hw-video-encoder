import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as path_effects

def detect_pass_type(x):
    if pd.isna(x):
        return '1-pass'
    val = str(x).strip().lower()
    if val in ('n/a', 'na', ''):
        return '1-pass'
    return '2-pass'

def get_distinct_colors(n):
    # Use matplotlib's tab20, tab20b, tab20c, and hsv for up to 100+ colors
    base_palettes = ['tab20', 'tab20b', 'tab20c']
    colors = []
    for palette in base_palettes:
        cmap = plt.get_cmap(palette)
        colors.extend([cmap(i) for i in range(cmap.N)])
    if n > len(colors):
        hsv_colors = [plt.cm.hsv(i / n) for i in range(n - len(colors))]
        colors.extend(hsv_colors)
    return colors[:n]

def plot_simple_bd(
    file_configs,
    output_filename=None,
    show_plot=True
):
    """
    file_configs: list of dicts, each with:
        - 'csv_file': path to CSV file
        - 'label': label for legend (optional)
        - 'enable_1pass': bool (default True)
        - 'enable_2pass': bool (default True)
    output_filename: if provided, save the plot to this file
    show_plot: whether to display the plot interactively
    """
    # Count total groups (file x pass type) for color assignment
    n_groups = sum(
        (1 if cfg.get('enable_1pass', True) else 0) +
        (1 if cfg.get('enable_2pass', True) else 0)
        for cfg in file_configs
    )
    color_cycle = get_distinct_colors(n_groups)
    marker_cycle = ['o', 's', 'D', '^', 'v', 'P', 'X', '*', '<', '>', 'h', 'H', 'd', 'p', '|', '_', '+', 'x', '1', '2', '3', '4']
    # Assign a unique color/marker to each (file, pass type) group
    group_keys = []
    for idx, cfg in enumerate(file_configs):
        if cfg.get('enable_1pass', True):
            group_keys.append((idx, '1-pass'))
        if cfg.get('enable_2pass', True):
            group_keys.append((idx, '2-pass'))
    color_marker_map = {}
    for i, key in enumerate(group_keys):
        color_marker_map[key] = (color_cycle[i % len(color_cycle)], marker_cycle[i % len(marker_cycle)])

    fig, ax = plt.subplots(figsize=(12, 8))

    for idx, cfg in enumerate(file_configs):
        label_base = cfg.get('label', cfg['csv_file'])
        df = pd.read_csv(cfg['csv_file'], sep=',')
        df['file_bytes'] = df['file_bytes'].astype(str).str.replace(',', '')
        df['file_MB'] = df['file_bytes'].astype(int) / 1_048_576
        df['crf'] = pd.to_numeric(df['crf'], errors='coerce')
        df['pass_type'] = df['encoding_time_pass1_s'].apply(detect_pass_type)

        for pass_type in ['1-pass', '2-pass']:
            if (pass_type == '1-pass' and not cfg.get('enable_1pass', True)) or \
               (pass_type == '2-pass' and not cfg.get('enable_2pass', True)):
                continue
            group = df[df['pass_type'] == pass_type]
            if group.empty:
                continue
            color, marker = color_marker_map[(idx, pass_type)]
            # Sort by file_MB for line plotting
            group_sorted = group.sort_values('file_MB')
            # Connect points with a line of the same color
            ax.plot(
                group_sorted['file_MB'],
                group_sorted['vmaf_mean'],
                color=color,
                marker=marker,
                linestyle='-',
                linewidth=2,
                markersize=8,
                label=f"{label_base} ({pass_type})",
                alpha=0.85
            )
            # Scatter points for emphasis
            ax.scatter(
                group_sorted['file_MB'],
                group_sorted['vmaf_mean'],
                color=color,
                marker=marker,
                edgecolor='black',
                s=70,
                alpha=0.85
            )
            # Label each point by width with a black outline and group color
            for _, row in group_sorted.iterrows():
                txt = ax.text(
                    row['file_MB'],
                    row['vmaf_mean'],
                    str(int(row['width'])),
                    fontsize=8,
                    ha='left',
                    va='bottom',
                    color=color,
                    zorder=10
                )
                txt.set_path_effects([
                    path_effects.Stroke(linewidth=1.5, foreground='black'),
                    path_effects.Normal()
                ])

    # X/Y axis formatting and gridlines
    import matplotlib.ticker as mticker
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
    ax.set_title('BD Curve (Grouped by File and Pass Type, Labeled by Width)')
    ax.legend(fontsize=9, loc='best', ncol=2)
    plt.tight_layout()

    if output_filename:
        fig.savefig(output_filename)
        print(f"Saved plot to {output_filename}")
    if show_plot:
        plt.show()
    plt.close(fig)

# Example usage:
if __name__ == "__main__":
    file_configs = [
        {
            'csv_file': 'Out/CQGoogle/sonichd/sonichd-CQGoogle.csv',
            'label': 'SonicHD',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/badminton/badminton-CQGoogle.csv',
            'label': 'badminton',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/1440p-av1-42sec/1440p-av1-42sec-CQGoogle.csv',
            'label': '1440p-av1-42sec',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/Halo_Montage_1080p/Halo_Montage_1080p-CQGoogle.csv',
            'label': 'Halo_Montage_1080p',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CQGoogle.csv',
            'label': 'Halo_NoMotion_20sec_1080p',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/ios_native_recorder/ios_native_recorder-CQGoogle.csv',
            'label': 'ios_native_recorder',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/steal-a-brainrot/steal-a-brainrot-CQGoogle.csv',
            'label': 'steal-a-brainrot',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/strongest-battlegrounds-mac-1440/strongest-battlegrounds-mac-1440-CQGoogle.csv',
            'label': 'strongest-battlegrounds-mac-1440',
            'enable_1pass': False,
            'enable_2pass': True
        },
        {
            'csv_file': 'Out/CQGoogle/TinyWheelsiPad1920x1440x60xHEVCScreenRecording/TinyWheelsiPad1920x1440x60xHEVCScreenRecording-CQGoogle.csv',
            'label': 'TinyWheelsiPad1920x1440x60xHEVCScreenRecording',
            'enable_1pass': False,
            'enable_2pass': True
        },
    ]
    plot_simple_bd(
        file_configs=file_configs,
        output_filename='simple_bd_graph.png',
        show_plot=True
    )