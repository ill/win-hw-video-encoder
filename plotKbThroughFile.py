import subprocess
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_frame_sizes_by_file(video_files):
    """
    Given a list of video files, extract per-frame (or per-packet) sizes in KB,
    plot them with unique colors, and return a combined DataFrame.
    """
    def run_ffprobe(cmd):
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return None

    def extract_frames(video_path):
        """Try to extract frame.pkt_size (in KB) via -show_frames"""
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_frames",
            "-show_entries", "frame=best_effort_timestamp_time,pts_time,pkt_size,coded_picture_number",
            "-print_format", "json",
            video_path
        ]
        data = run_ffprobe(cmd)
        if not data or "frames" not in data:
            return pd.DataFrame()

        rows = []
        for f in data["frames"]:
            if f.get("pkt_size") is None:
                continue
            try:
                size_kb = int(f["pkt_size"]) / 1024.0
                t = float(f.get("pts_time") or f.get("best_effort_timestamp_time") or 0)
            except Exception:
                continue
            rows.append({
                "time_s": t,
                "frame_size_kb": size_kb,
                "frame_number": f.get("coded_picture_number")
            })
        return pd.DataFrame(rows)

    def extract_packets(video_path):
        """Fallback: extract packet.size (in KB) via -show_packets"""
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_packets",
            "-show_entries", "packet=pts_time,dts_time,size",
            "-print_format", "json",
            video_path
        ]
        data = run_ffprobe(cmd)
        if not data or "packets" not in data:
            return pd.DataFrame()

        rows = []
        for p in data["packets"]:
            if p.get("size") is None:
                continue
            try:
                size_kb = int(p["size"]) / 1024.0
                t = float(p.get("pts_time") or p.get("dts_time") or 0)
            except Exception:
                continue
            rows.append({
                "time_s": t,
                "frame_size_kb": size_kb
            })
        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.sort_values("time_s").reset_index(drop=True)
            df["frame_number"] = df.index
        return df

    def get_sizes(video_path):
        """Try frames first, then packets fallback."""
        df = extract_frames(video_path)
        if df.empty:
            df = extract_packets(video_path)
        if df.empty:
            print(f"⚠️ No data extracted for {video_path}")
            return pd.DataFrame()
        df["file"] = os.path.basename(video_path)
        return df

    # --- Gather all ---
    all_dfs = []
    for f in video_files:
        print(f"Processing {f}...")
        df = get_sizes(f)
        if not df.empty:
            print(f"  -> {len(df)} data points")
            all_dfs.append(df)

    if not all_dfs:
        print("❌ No frame or packet size data extracted from any file.")
        return pd.DataFrame()

    df_all = pd.concat(all_dfs, ignore_index=True)

    # --- Summary stats ---
    print("\n=== Frame/Packet Size Summary (KB) ===")
    print(df_all.groupby("file")["frame_size_kb"].agg(["count", "mean", "max", "min"]).round(2))

    # --- Plot ---
    plt.figure(figsize=(14, 7))
    for file_name, group in df_all.groupby("file"):
        plt.plot(group["time_s"], group["frame_size_kb"], label=file_name, lw=0.8)

    plt.xlabel("Time (seconds)")
    plt.ylabel("Size (KB)")
    plt.title("Frame/Packet size over time (grouped by file)")
    plt.grid(True, alpha=0.3)
    plt.legend(title="File", fontsize=9)
    plt.tight_layout()
    plt.show()

    return df_all



if __name__ == "__main__":
    video_files = [
        "Out/CRF/sonichd/sonichd-CRF-crf-33-w-1920-h-888-fps--1-2Pass.webm",
        "Out/CQGoogleGSunExperiment/sonichd/sonichd-CQGoogleGSunExperiment-crf-31-bp-12531k-mnbp-6265k-mxbp-18796k-w-1920-h-888-fps-30-t-4-tc-2-2Pass-s1-0-s2-0.webm",
    ]
    df = plot_frame_sizes_by_file(video_files)
