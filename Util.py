import sys
import time
import subprocess

RES_1080p = (1920, 1080)
RES_720p = (1280, 720)
RES_540p = (960, 540)
RES_480p = (640, 480)
RES_360p = (640, 360)
RES_240p = (320, 240)
RES_180p = (320, 180)
RES_90p = (160, 90)

RES_COMMON = [
    RES_1080p,
    RES_720p,
    RES_480p,
    RES_360p,
    RES_240p,
]

RES_RBX = [
    RES_720p,
    RES_360p,
    RES_180p,
    RES_90p,
]

RES_ALL = [
    RES_1080p,
    RES_720p,
    RES_540p,
    RES_480p,
    RES_360p,
    RES_240p,
    RES_180p,
    RES_90p
]

GSUN = 0.07

CRF_MAX = 63

VP9_TILE_DIM = 256

HEADER = '=================='

def ceil_to_divisible_by(original: int, divisible_by: int) -> int:
    return (int((original - 1) / divisible_by) + 1) * divisible_by

def sign(number):
    return (number > 0) - (number < 0)

def maybe_scale_down_to_fit(current_long_side: int, current_short_side: int, max_long_side: int, max_short_side: int, transposed: bool) -> tuple[int, int]:
    long_side: int = 0
    short_side: int = 0

    if (current_long_side <= max_long_side and current_short_side <= max_short_side):
        # Fit; still try to make it divisible by 8.
        long_side = ceil_to_divisible_by(current_long_side, 8)
        short_side = ceil_to_divisible_by(current_short_side, 8)
    elif (current_long_side / current_short_side > max_long_side / max_short_side):
        # If long side is too long; should scale down with long side to fit.
        long_side = ceil_to_divisible_by(max_long_side, 8)
        short_side = ceil_to_divisible_by(max_long_side * current_short_side / current_long_side, 8)
    else:
        # If short side is too long; should scale down with short side to fit.
        long_side = ceil_to_divisible_by(max_short_side * current_long_side / current_short_side, 8)
        short_side = ceil_to_divisible_by(max_short_side, 8)

    return (short_side if transposed else long_side, 
            long_side if transposed else short_side)

def print_collection(collection):
    for arg in collection:
        print (arg, end = ' ')
    print('\n')

def get_target_bitrate_kbps(width, height, fps, gsun) -> int:
    return int(width * height * fps * gsun * GSUN / 1000)

# Runs ffmpeg and returns the time it took to run
def ffmpeg(input, params = []) -> float:
    print(f'{HEADER}\nRunning ffmpeg...')

    ffmpeg_cmd = ([
        'ffmpeg',
        '-hide_banner',
        '-i', input,
    ]
    + params)

    print_collection(ffmpeg_cmd)

    start = time.perf_counter()
    result = subprocess.run(ffmpeg_cmd)
    end = time.perf_counter()

    if result.returncode != 0:
        print('ffmpeg failed.')
        sys.exit(1)
    return end - start

def ffprobe(input, output, show_frames = False, show_streams = False, params = []):
    print(f'{HEADER}\nRunning ffprobe...')

    ffprobe_cmd = (['ffprobe',
        '-hide_banner',
        '-print_format', 
        'json',
    ]
    + params
    + (['-show_frames'] if show_frames else [])
    + (['-show_streams'] if show_streams else [])
    + [input])

    print_collection(ffprobe_cmd)
    
    with open(output, 'w') as f:
        result = subprocess.run(ffprobe_cmd, stdout=f)
        if result.returncode != 0:
            print('ffprobe failed.')
            sys.exit(1)