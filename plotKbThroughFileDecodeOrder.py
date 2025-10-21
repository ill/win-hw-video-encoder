import subprocess
import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_frame_sizes_by_file(video_files):
    """
    Given a list of video files, extract per-frame (or per-packet) sizes in KB,
    plot them by decode order (frame index) with unique colors, and return a combined DataFrame.
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
            "-show_entries", "frame=pkt_size,coded_picture_number,pts_time,best_effort_timestamp_time",
            "-print_format", "json",
            video_path
        ]
        data = run_ffprobe(cmd)
        if not data or "frames" not in data:
            return pd.DataFrame()

        rows = []
        for f in data["frames"]:
            pkt_size = f.get("pkt_size")
            if pkt_size is None:
                continue
            try:
                size_kb = int(pkt_size) / 1024.0
            except Exception:
                continue
            # pick whichever timestamp is available
            t = f.get("pts_time") or f.get("best_effort_timestamp_time")
            try:
                t = float(t) if t is not None else None
            except Exception:
                t = None
            rows.append({
                "frame_size_kb": size_kb,
                "time_s": t
            })
        df = pd.DataFrame(rows)
        if not df.empty:
            # force decode/display order purely by sequential index
            df = df.reset_index(drop=True)
            df["frame_number"] = df.index
        return df

    def extract_packets(video_path):
        """Fallback: extract packet.size (in KB) via -show_packets"""
        cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_packets",
            "-show_entries", "packet=size,pts_time,dts_time",
            "-print_format", "json",
            video_path
        ]
        data = run_ffprobe(cmd)
        if not data or "packets" not in data:
            return pd.DataFrame()

        rows = []
        for p in data["packets"]:
            size = p.get("size")
            if size is None:
                continue
            try:
                size_kb = int(size) / 1024.0
            except Exception:
                continue
            t = p.get("pts_time") or p.get("dts_time")
            try:
                t = float(t) if t is not None else None
            except Exception:
                t = None
            rows.append({
                "frame_size_kb": size_kb,
                "time_s": t
            })
        df = pd.DataFrame(rows)
        if not df.empty:
            # use sequential decode order
            df = df.reset_index(drop=True)
            df["frame_number"] = df.index
        return df

    def get_sizes(video_path):
        df = extract_frames(video_path)
        if df.empty:
            df = extract_packets(video_path)
        if df.empty:
            print(f"⚠️ No data extracted for {video_path}")
            return pd.DataFrame()
        df["file"] = os.path.basename(video_path)
        return df

    # --- Collect data ---
    all_dfs = []
    for f in video_files:
        print(f"Processing {f}...")
        df = get_sizes(f)
        if not df.empty:
            print(f"  -> {len(df)} frames/packets")
            all_dfs.append(df)

    if not all_dfs:
        print("❌ No data extracted from any file.")
        return pd.DataFrame()

    df_all = pd.concat(all_dfs, ignore_index=True)

    # --- Summary ---
    print("\n=== Frame/Packet Size Summary (KB) ===")
    print(df_all.groupby("file")["frame_size_kb"].agg(["count", "mean", "max", "min"]).round(2))

    # --- Plot by decode order ---
    plt.figure(figsize=(14, 7))
    for file_name, group in df_all.groupby("file"):
        plt.plot(group["frame_number"], group["frame_size_kb"], label=file_name, lw=0.8)

    plt.xlabel("Decode order (frame index)")
    plt.ylabel("Size (KB)")
    plt.title("Frame/Packet size by decode order (grouped by file)")
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
