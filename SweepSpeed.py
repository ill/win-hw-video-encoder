import argparse
import subprocess
import sys

import platform
import os
import csv
import json
import statistics
import math
import time

import boto3
from botocore.exceptions import ClientError

def generate_video_filename(video_filename, speed):
    """
    Generate output video file name in the format:
    """
    return f"{video_filename}-speed-{speed}.webm"

def generate_ffprobe_filename(video_filename, speed):
    """
    Generate output FFProbe file name in the format:
    "<video_filename>.probe.json"
    """
    return f"{video_filename}-speed-{speed}.probe.json"

def generate_vmaf_filename(video_filename, speed):
    """
    Generate output VMAF file name in the format:
    "<video_filename>.vmaf.json"
    """
    return f"{video_filename}-speed-{speed}.vmaf.json"

def upload_to_s3(file):
    print(f"Uploading {file} to S3...")
    object_name = "videos/ffmpeg-video-quallity/sweep-speed/" + file

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file, 'audiovisual-test-public', object_name, ExtraArgs={'ACL': 'public-read'})
        print("Upload succeeded with response:", response)
    except ClientError as e:
        print("Upload failed with error:", e)
        return False
    return True

def parse_args():
    parser = argparse.ArgumentParser(description="Video transcode automation script.")
    parser.add_argument('--sso', type=bool, default=False, help='Use AWS SSO to login before uploading to S3')
    return parser.parse_args()

def transcode(input_filename, speed, output_filename):

    ffmpeg_cmd = [
        'ffmpeg',
        '-hide_banner',

        '-i', input_filename,

        '-vf', 'scale=1920:-1',
        '-fps_mode', 'passthrough',

        # drop metadata things
        '-dn',
        '-sn',
        '-map_metadata', '-1',
        '-map_chapters', '-1',

        '-c:v', 'libvpx-vp9',
        '-speed', str(speed),

        '-f', 'webm',
        output_filename,
        '-y',
    ]
    print (ffmpeg_cmd)
    start = time.perf_counter()
    result = subprocess.run(ffmpeg_cmd)
    end = time.perf_counter()
    if result.returncode != 0:
        print('ffmpeg failed.')
        sys.exit(1)
    return end - start

def main():
    args = parse_args()

    if (args.sso):
        aws_sso_cmd = ['aws', 'sso', 'login', '--profile', 'test-audiovisual']
        result = subprocess.run(aws_sso_cmd)
        if result.returncode != 0:
            print('AWS SSO login failed. Will use existing AWS tokens in the environment.')
    
    # Create and write header to csv
    csv_file = 'ffmpeg_vp9_sweep_speed.csv'
    csv_header = [
        'speed',
        'link', 
        'video id',
        'actual_bitrate',
        'vmaf_hmean', 
        'vmaf_stddev',
        'bpb',
        'encoding_time_s'
    ]
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

    for speed in range(0, 15):
        print(f"Running with \"difficult video\" speed: {speed}")

        output_filename = generate_video_filename("1440p-av1-42sec", speed)

        transcode_time = 0#transcode("1440p-av1-42sec.mp4", speed, output_filename)

        ffprobe_filename = generate_ffprobe_filename("1440p-av1-42sec", speed)

        print(f'Running ffprobe...')
        ffprobe_cmd = ['ffprobe', 
                       '-print_format', 
                       'json', 
                       #'-show_frames', 
                       '-show_streams', 
                       output_filename]
        with open(ffprobe_filename, 'w') as f:
            result = subprocess.run(ffprobe_cmd, stdout=f)
            if result.returncode != 0:
                print('ffprobe failed.')
                sys.exit(1)

        vmaf_filename = generate_vmaf_filename("1440p-av1-42sec", speed)

        print(f'Running vmaf...')
        vmaf_command = [
            'ffmpeg',
            '-hide_banner',
            '-i', "1440p-av1-42sec.mp4",
            '-i', output_filename,
            '-lavfi', f"[0:v]settb=AVTB,setpts=PTS-STARTPTS,fps=30,scale=1920:-1:flags=bicubic[reference];[1:v]settb=AVTB,setpts=PTS-STARTPTS,fps=30,scale=1920:-1:flags=bicubic[distorted];[distorted][reference]libvmaf=log_fmt=json:log_path={vmaf_filename}:n_threads=4",
            '-f', 'null',
            '-'
        ]

        print(vmaf_command)

        result = subprocess.run(vmaf_command)
        if result.returncode != 0:
            print('ffmpeg vmaf failed.')
            sys.exit(1)

        # --- CSV WRITING LOGIC ---
        # Read VMAF and probe data
        with open(vmaf_filename, 'r') as f:
            vmaf_data = json.load(f)
        with open(ffprobe_filename, 'r') as f:
            probe_data = json.load(f)

        # Find video stream and get actual bitrate
        actual_bitrate = None
        for stream in probe_data.get('streams', []):
            if stream.get('codec_type') == 'video':
                actual_bitrate = stream.get('bit_rate')
                break

        # Extract required data
        vmaf_harmonic_mean = vmaf_data["pooled_metrics"]["vmaf"]["harmonic_mean"]
        vmafs = [x["metrics"]["vmaf"] for x in vmaf_data["frames"]]
        vmaf_std_dev = statistics.stdev(vmafs)
        bpb = vmaf_harmonic_mean / math.log2(int(actual_bitrate)) if actual_bitrate is not None else 'N/A'

        print (f"=====RESULTS:\n\tSpeed{speed}\n\tvmaf_harmonic_mean:{vmaf_harmonic_mean}\n\tvmaf_std_dev{vmaf_std_dev}")

        # Construct S3 link
        s3_link = f"https://audiovisual-test-public.s3.us-east-1.amazonaws.com/videos/ffmpeg-video-quallity/sweep-speed/{output_filename}"

        # Prepare data row
        csv_row = [
            speed,
            #s3_link,
            output_filename,
            str(actual_bitrate) if actual_bitrate is not None else 'N/A',
            vmaf_harmonic_mean,
            vmaf_std_dev,
            str(bpb),
            str(transcode_time)
        ]

        # Append row to CSV
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)
        # --- END CSV WRITING LOGIC ---

        #upload_to_s3(output_filename)
        #upload_to_s3('vmaf.json', device_id, generate_vmaf_filename(video_s3_file_name))

    # os.remove('vid.h264')
    # os.remove('vid.mp4')
    # os.remove('probe.json')
    # os.remove('vmaf.json')
    print('Done.')

if __name__ == '__main__':
    main()
