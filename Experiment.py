import os

import csv
import json
import statistics
import math
from fractions import Fraction

import Util

class Experiment:
    def __init__(self, experiment_name, input_video_file_name, output_video_file_basename):
        self.experiment_name = experiment_name
        self.input_video_file_name = input_video_file_name
        self.output_video_file_basename = output_video_file_basename

        self.base_directory = f"Out/{experiment_name}/{self.output_video_file_basename}"

        os.makedirs(self.base_directory, exist_ok=True)
        
        self.csv_file_name = f"{self.base_directory}/{self.output_video_file_basename}-{experiment_name}.csv"
        self.input_ffprobe_filename = f"{self.base_directory}/{self.output_video_file_basename}-{self.experiment_name}.input_probe.json"
        self.input_csv_file_name = f"{self.base_directory}/{self.output_video_file_basename}-{experiment_name}.input_info.csv"
        self.csv_file = None

        self.input_width = None
        self.input_height = None
        self.input_fps = None
        self.input_duration_s = None
        self.input_bitrate = None
        self.input_bytes = None

    def ffprobe(self):
        print(f'{Util.HEADER}\nRunning ffprobe on Input...')

        Util.ffprobe(self.input_video_file_name, self.input_ffprobe_filename, show_streams=True,
        params = [
            '-show_entries', 'format=duration'
        ])

    def process_input(self):
        with open(self.input_ffprobe_filename, 'r') as f:
            probe_data = json.load(f)

        format = probe_data.get('format')

        if format is not None:
            self.input_duration_s = format.get('duration')

        # Find video stream and get actual bitrate
        for stream in probe_data.get('streams', []):
            if stream.get('codec_type') == 'video':
                self.input_width = stream.get('width')
                self.input_height = stream.get('height')
                self.input_bitrate = stream.get('bit_rate')
                fps_str = stream.get('avg_frame_rate')
                self.input_fps = float(Fraction(fps_str)) if '/' in fps_str else float(fps_str)
                break

        self.input_bytes = os.path.getsize(self.input_video_file_name)

        print (f"{Util.HEADER}\
            \n\tInput: {self.input_video_file_name}\
            \n\twidth:{str(self.input_width) if self.input_width is not None else 'N/A'}\
            \n\theight:{str(self.input_height) if self.input_height is not None else 'N/A'}\
            \n\tfps:{str(self.input_fps) if self.input_fps is not None else 'N/A'}\
            \n\tduration_s:{str(self.input_duration_s) if self.input_duration_s is not None else 'N/A'}\
            \n\tbitrate:{f'{int(self.input_bitrate):,}' if self.input_bitrate is not None else 'N/A'}\
            \n\tsize_bytes:{f'{self.input_bytes:,}' if self.input_bytes is not None else 'N/A'}")
        
    def write_input_csv(self):
        # Create a csv that outputs info about the experiment and the input itself
        csv_header = (self.get_extra_input_csv_header_columns() +
        [
            #'link', 
            'input',
            'width',
            'height',
            'fps',
            'duration_s',
            'bitrate',
            'file_bytes'
        ])

        csv_row = (self.get_extra_input_csv_columns() +
        [
            #s3_link,
            self.input_video_file_name,
            str(self.input_width) if self.input_width is not None else 'N/A',
            str(self.input_height) if self.input_height is not None else 'N/A',
            str(self.input_fps) if self.input_fps is not None else 'N/A',
            str(self.input_duration_s) if self.input_duration_s is not None else 'N/A',
            f'{int(self.input_bitrate):,}' if self.input_bitrate is not None else 'N/A',
            f'{self.input_bytes:,}' if self.input_bytes is not None else 'N/A',
        ])

        with open(self.input_csv_file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
            writer.writerow(csv_row)

    def get_extra_input_csv_header_columns(self):
        return []
    
    def get_extra_input_csv_columns(self):
        return []

    def create_csv(self):
        # Create and write header to csv
        csv_header = (self.get_extra_csv_header_columns() +
        [
            'width',
            'height',
            'fps',
            
            'vmaf_mean',
            'vmaf_harmonic_mean',
            'vmaf_min',
            'vmaf_max',
            'vmaf_stddev',

            'encoding_time_s',
            'encoding_time_pass1_s',
            'encoding_time_pass2_s',

            'file_bytes',

            'actual_bitrate',
            'bpb',            
            
            'video id',
            #'link', 
        ])

        with open(self.csv_file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)

    def get_extra_csv_header_columns(self):
        return []

    def run_experiment(self):
        self.ffprobe()
        self.process_input()
        self.write_input_csv()
        self.create_csv()

    def get_scaled_down_to_fit_resolutions(self, resolutions: list[tuple[int, int]]) -> list[tuple[int, int]]:
        results: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()

        for res in resolutions:
            new_res = self.scale_down_to_fit(res[0], res[1])
            if new_res not in seen:
                seen.add(new_res)
                results.append(new_res)

        return results    

    def scale_down_to_fit(self, destination_long_side: int, destination_short_side: int) -> tuple[int, int]:
        transposed = self.input_width < self.input_height
        long_side = max(self.input_width, self.input_height)
        short_side = min(self.input_width, self.input_height)

        return Util.maybe_scale_down_to_fit(long_side, short_side, destination_long_side, destination_short_side, transposed)
    
    def get_scaled_down_common_resolutions(self) -> list[tuple[int, int]]:
        return self.get_scaled_down_to_fit_resolutions(Util.RES_COMMON)
    
    def get_scaled_down_rbx_resolutions(self) -> list[tuple[int, int]]:
        return self.get_scaled_down_to_fit_resolutions(Util.RES_RBX)
    
    def get_scaled_down_all_resolutions(self) -> list[tuple[int, int]]:
        return self.get_scaled_down_to_fit_resolutions(Util.RES_ALL)

    class SubExperiment:
        def __init__(self, experiment,
                     sub_experiment_name: str,
                     output_width: int = -1,
                     output_height: int = -1,
                     output_fps: int = -1,
                     two_pass_encoding: bool = False):
            self.experiment = experiment
            self.sub_experiment_name = sub_experiment_name
            self.output_width = output_width if output_width >= 0 else experiment.input_width
            self.output_height = output_height if output_height >= 0 else experiment.input_height
            self.output_fps = output_fps if output_fps >= 0 else experiment.input_fps
            self.two_pass_encoding = two_pass_encoding

            self.video_filename = f"{self.experiment.base_directory}/{self.experiment.output_video_file_basename}-{self.experiment.experiment_name}-{self.sub_experiment_name}.webm"
            self.output_ffprobe_filename = f"{self.experiment.base_directory}/{self.experiment.output_video_file_basename}-{self.experiment.experiment_name}-{self.sub_experiment_name}.probe.json"
            self.vmaf_filename = f"{self.experiment.base_directory}/{self.experiment.output_video_file_basename}-{self.experiment.experiment_name}-{self.sub_experiment_name}.vmaf.json"

            self.passlog_filename = f"{self.experiment.base_directory}/{self.experiment.output_video_file_basename}-{self.experiment.experiment_name}-{self.sub_experiment_name}-passlog" if two_pass_encoding else None

            self.transcode_seconds = 0.0
            self.transcode_pass_1_seconds = None
            self.transcode_pass_2_seconds = None
            self.vmaf_mean = 0.0
            self.vmaf_harmonic_mean = 0.0
            self.vmaf_min = 0.0
            self.vmaf_max = 0.0
            self.vmaf_std_dev = 0.0
            self.actual_bitrate = None
            self.bpb = None    

        def run_sub_experiment(self):
            print(f'{Util.HEADER}\nRunning: {self.get_sub_experiment_name()}')
            self.transcode()
            self.ffprobe()
            self.vmaf()
            self.process_results()
            self.write_csv_row()

        def get_sub_experiment_name(self):
            return f'{self.experiment.experiment_name}: {self.sub_experiment_name}'
        
        def ffmpeg(self, params):
            return Util.ffmpeg(self.experiment.input_video_file_name,
            [
                '-vf', f'fps={self.output_fps},scale={self.output_width}:{self.output_height},setsar=1/1',
                '-fps_mode', 'cfr',

                # drop metadata things
                '-dn',
                '-sn',
                '-map_metadata', '-1',
                '-map_chapters', '-1',

                '-row-mt', '1',
                '-c:v', 'libvpx-vp9',
            ] + params)

        def transcode(self):
            output_params = [
                    '-f', 'webm',
                    self.video_filename,
                    '-y',
                ]

            if self.two_pass_encoding:
                print(f'{Util.HEADER}\nRunning two pass transcode (Pass 1)...')

                self.transcode_pass_1_seconds = self.ffmpeg(
                    self.get_extra_ffmpeg_parameters_pass1() 
                    + [
                        '-pass', '1', '-passlogfile', self.passlog_filename,
                        '-f', 'null', 'dev/null',    # For windows, dev/null should be NUL, handle this somehow later?
                        '-y'
                    ])

                print(f'{Util.HEADER}\nRunning two pass transcode (Pass 2)...')

                self.transcode_pass_2_seconds = self.ffmpeg(
                    self.get_extra_ffmpeg_parameters_pass2() 
                    + [
                        '-pass', '2', '-passlogfile', self.passlog_filename,
                    ]
                    + output_params)

                self.transcode_seconds = self.transcode_pass_1_seconds + self.transcode_pass_2_seconds

            else:
                print(f'{Util.HEADER}\nRunning one pass transcode...')
                self.transcode_seconds = self.ffmpeg(
                    self.get_extra_ffmpeg_parameters_single_pass() 
                    + output_params)

        def get_extra_ffmpeg_parameters(self):
            return []
        
        def get_extra_ffmpeg_parameters_single_pass(self):
            return self.get_extra_ffmpeg_parameters()
        
        def get_extra_ffmpeg_parameters_pass1(self):
            return self.get_extra_ffmpeg_parameters()
        
        def get_extra_ffmpeg_parameters_pass2(self):
            return self.get_extra_ffmpeg_parameters()

        def ffprobe(self):
            print(f'{Util.HEADER}\nRunning ffprobe on Output...')

            Util.ffprobe(self.video_filename, self.output_ffprobe_filename, show_streams=True)

        def vmaf(self):
            print(f'{Util.HEADER}\nRunning vmaf...')

            # If downscaling choose area filter
            # If upscaling choose lanczos filter

            reference_filter = 'area' if self.experiment.input_width > 1920 else 'lanczos'
            distorted_filter = 'area' if self.output_width > 1920 else 'lanczos'

            aspect_fit_params = 'decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2'
            aspect_fill_params = 'increase,crop=1920:1080'

            aspect_fill = True
            force_aspect_ratio = True

            aspect_ratio_params = f':force_original_aspect_ratio={aspect_fill_params if aspect_fill else aspect_fit_params}' if force_aspect_ratio else ''

            # This forces the timestamps to align, fps to align to 30, scale resolution to 1920x1080 for the default VMAF model, and either aspect fit or aspect fill
            stream_str = f'[1:v]setsar=1/1,settb=AVTB,setpts=PTS-STARTPTS,fps=30,scale=1920:1080:flags={reference_filter}{aspect_ratio_params},setsar=1/1,settb=AVTB,setpts=N/FRAME_RATE/TB[reference];'\
                         f'[0:v]setsar=1/1,settb=AVTB,setpts=PTS-STARTPTS,fps=30,scale=1920:1080:flags={distorted_filter}{aspect_ratio_params},setsar=1/1,settb=AVTB,setpts=N/FRAME_RATE/TB[distorted];'

            debug_vmaf = True

            if debug_vmaf:
                # outputs a video of side by side comparison and diff comparison
                Util.ffmpeg(self.experiment.input_video_file_name,
                [
                    '-i', self.video_filename,

                    '-filter_complex',
                    f"{stream_str}"
                    
                    # debug print info about each frame, if things don't match this could be a problem
                    # also split into 3 streams for the 3 outputs below
                    f"[reference]showinfo@REFERENCE,split=3[r_vmaf][r_side_by_side][r_diff];"
                    f"[distorted]showinfo@DISTORTED,split=3[d_vmaf][d_side_by_side][d_diff];"
                    
                    # run vmaf
                    f"[d_vmaf][r_vmaf]libvmaf=log_path={self.vmaf_filename}:log_fmt=json[vmaf];"
                    
                    # output side by side video
                    f"[d_side_by_side][r_side_by_side]hstack=inputs=2,format=yuv420p,drawbox=x=(iw-2)/2:y=0:w=2:h=ih:color=white@0.6:t=fill,settb=AVTB,setpts=N/FRAME_RATE/TB[side_by_side];"
                    
                    # output diff video, this should show as few diffs as possible
                    f"[d_diff][r_diff]blend=all_mode=difference,format=yuv420p,eq=contrast=5:brightness=0.1,settb=AVTB,setpts=N/FRAME_RATE/TB[diff]",
                    
                    '-map', '[side_by_side]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', f'{self.video_filename}.side_by_side.mp4', '-y',
                    '-map', '[diff]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', f'{self.video_filename}.diff.mp4', '-y',
                    '-map', '[vmaf]', '-f', 'null', '-',
                ])
            else:
                Util.ffmpeg(self.experiment.input_video_file_name,
                [
                    '-i', self.video_filename,
                    '-lavfi',

                    f"{stream_str}"
                    f"[distorted][reference]libvmaf=log_fmt=json:log_path={self.vmaf_filename}:n_threads=4",

                    '-f', 'null',
                    '-'
                ])

        def process_results(self):
            # Read VMAF and probe data
            with open(self.vmaf_filename, 'r') as f:
                vmaf_data = json.load(f)
            with open(self.output_ffprobe_filename, 'r') as f:
                probe_data = json.load(f)

            # Find video stream and get actual bitrate
            for stream in probe_data.get('streams', []):
                if stream.get('codec_type') == 'video':
                    self.actual_bitrate = stream.get('bit_rate')
                    break

            # Extract required data
            self.vmaf_mean = vmaf_data["pooled_metrics"]["vmaf"]["harmonic_mean"]
            self.vmaf_harmonic_mean = vmaf_data["pooled_metrics"]["vmaf"]["harmonic_mean"]
            self.vmaf_min = vmaf_data["pooled_metrics"]["vmaf"]["min"]
            self.vmaf_max = vmaf_data["pooled_metrics"]["vmaf"]["max"]
            vmafs = [x["metrics"]["vmaf"] for x in vmaf_data["frames"]]
            self.vmaf_std_dev = statistics.stdev(vmafs)
            if self.actual_bitrate is not None:
                self.bpb = self.vmaf_harmonic_mean / math.log2(int(self.actual_bitrate))

            print (f"{Util.HEADER}\nResults: {self.get_sub_experiment_name()}\
                \n\tvmaf_mean:{self.vmaf_mean}\
                \n\tvmaf_harmonic_mean:{self.vmaf_harmonic_mean}\
                \n\tvmaf_min:{self.vmaf_min}\
                \n\tvmaf_max:{self.vmaf_max}\
                \n\tvmaf_std_dev:{self.vmaf_std_dev}\
                \n\tactual_bitrate:{self.actual_bitrate}\
                \n\tbpb:{self.bpb}")

        def write_csv_row(self):
            # Prepare data row
            csv_row = (self.get_extra_csv_columns() +
            [
                str(self.output_width),
                str(self.output_height),
                str(self.output_fps),
                                
                self.vmaf_mean,
                self.vmaf_harmonic_mean,
                self.vmaf_min,
                self.vmaf_max,
                self.vmaf_std_dev,

                str(self.transcode_seconds),
                str(self.transcode_pass_1_seconds) if self.transcode_pass_1_seconds is not None else 'N/A',
                str(self.transcode_pass_2_seconds) if self.transcode_pass_2_seconds is not None else 'N/A',

                f'{os.path.getsize(self.video_filename):,}',

                f'{int(self.actual_bitrate):,}' if self.actual_bitrate is not None else 'N/A',
                f'{self.bpb:,}' if self.bpb is not None else 'N/A',
                
                self.video_filename,
                #s3_link,
            ])

            # Append row to CSV
            with open(self.experiment.csv_file_name, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(csv_row)

        def get_extra_csv_columns(self):
            return []
