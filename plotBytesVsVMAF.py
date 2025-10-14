import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_bd_per_width(csv_path, min_crf=None, max_crf=None):
    df = pd.read_csv(csv_path, sep=',')
    df['file_bytes'] = df['file_bytes'].astype(str).str.replace(',', '')
    df['file_MB'] = df['file_bytes'].astype(int) / 1_048_576
    df['crf'] = pd.to_numeric(df['crf'], errors='coerce')

    # Filter by CRF range if specified
    if min_crf is not None and max_crf is not None:
        df = df[(df['crf'] >= min_crf) & (df['crf'] <= max_crf)]

    # Robust pass type detection
    def detect_pass_type(x):
        if pd.isna(x):
            return '1-pass'
        val = str(x).strip().lower()
        if val in ('n/a', 'na', ''):
            return '1-pass'
        return '2-pass'

    df['pass_type'] = df['encoding_time_pass1_s'].apply(detect_pass_type)

    for width in sorted(df['width'].unique()):
        subset = df[df['width'] == width]
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = {'1-pass': 'tab:blue', '2-pass': 'tab:orange'}

        for pass_type, group in subset.groupby('pass_type'):
            ax.scatter(group['file_MB'], group['vmaf_mean'], label=pass_type, color=colors[pass_type])
            for _, row in group.iterrows():
                ax.text(row['file_MB'], row['vmaf_mean'], str(int(row['crf'])),
                        fontsize=8, ha='left', va='bottom', color=colors[pass_type])

        ax.set_xlabel('File Size (MB)')
        ax.set_ylabel('VMAF Mean')
        ax.set_title(f'BD Curve for Width {width}')
        ax.legend()
        plt.tight_layout()
        plt.show()
        plt.close(fig)

# Example usage:
# plot_bd_per_width('your_file.csv', min_crf=18, max_crf=42)

plot_bd_per_width('Out/CRF/sonichd/sonichd-CRF.csv', min_crf=18, max_crf=42)