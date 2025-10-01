import subprocess
import sys

import csv
import json
import statistics
import math
import time

class Experiment:
    def __init__(self, experiment_name, input_video_file_name, output_video_file_basename):
        self.experiment_name = experiment_name
        self.input_video_file_name = input_video_file_name
        self.output_video_file_basename = output_video_file_basename

        self.csv_file_name = f"{self.output_video_file_basename}-{experiment_name}.csv"
        self.csv_file = None
        
    def create_csv(self):
        # Create and write header to csv
        csv_header = (self.get_extra_csv_header_columns() +
        [
            #'link', 
            'video id',
            'actual_bitrate',
            'vmaf_hmean', 
            'vmaf_stddev',
            'bpb',
            'encoding_time_s'
        ])

        with open(self.csv_file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)

    def get_extra_csv_header_columns(self):
        return []

    def run_experiment(self):
        self.create_csv()

    class SubExperiment:
        def __init__(self, experiment, sub_experiment_name):
            self.experiment = experiment
            self.sub_experiment_name = sub_experiment_name

            self.video_filename = f"{self.experiment.output_video_file_basename}-{self.experiment.experiment_name}-{self.sub_experiment_name}.webm"
            self.ffprobe_filename = f"{self.experiment.output_video_file_basename}-{self.experiment.experiment_name}-{self.sub_experiment_name}.probe.json"
            self.vmaf_filename = f"{self.experiment.output_video_file_basename}-{self.experiment.experiment_name}-{self.sub_experiment_name}.vmaf.json"

            self.transcode_seconds = 0.0
            self.vmaf_harmonic_mean = 0.0
            self.vmaf_std_dev = 0.0
            self.actual_bitrate = None
            self.bpb = None    

        def run_sub_experiment(self):
            print(f'==================\nRunning: {self.get_sub_experiment_name()}')
            self.transcode()
            self.ffprobe()
            self.vmaf()
            self.process_results()
            self.write_csv_row()

        def get_sub_experiment_name(self):
            return f'{self.experiment.experiment_name}: {self.sub_experiment_name}'
            
        def transcode(self):
            print('==================\nRunning ffmpeg...')

            ffmpeg_cmd = ([
                'ffmpeg',
                '-hide_banner',

                '-i', self.experiment.input_video_file_name,

                '-vf', 'scale=1920:-1',
                '-fps_mode', 'passthrough',

                # drop metadata things
                '-dn',
                '-sn',
                '-map_metadata', '-1',
                '-map_chapters', '-1',

                '-c:v', 'libvpx-vp9',
            ]
            + self.get_extra_ffmpeg_parameters() +
            [
                '-f', 'webm',
                self.video_filename,
                '-y',
            ])

            for arg in ffmpeg_cmd:
                print (arg, end = ' ')
            print('\n')        

            start = time.perf_counter()
            result = subprocess.run(ffmpeg_cmd)
            end = time.perf_counter()

            if result.returncode != 0:
                print('ffmpeg failed.')
                sys.exit(1)
            self.transcode_seconds = end - start

        def get_extra_ffmpeg_parameters(self):
            return []

        def ffprobe(self):
            print('==================\nRunning ffprobe...')

            ffprobe_cmd = ['ffprobe', 
                        '-print_format', 
                        'json', 
                        #'-show_frames', 
                        '-show_streams', 
                        self.video_filename]
            
            for arg in ffprobe_cmd:
                print (arg, end = ' ')
            print('\n')
            
            with open(self.ffprobe_filename, 'w') as f:
                result = subprocess.run(ffprobe_cmd, stdout=f)
                if result.returncode != 0:
                    print('ffprobe failed.')
                    sys.exit(1)

        def vmaf(self):
            print('==================\nRunning vmaf...')

            vmaf_command = [
                'ffmpeg',
                '-hide_banner',
                '-i', self.experiment.input_video_file_name,
                '-i', self.video_filename,
                '-lavfi', f"[0:v]settb=AVTB,setpts=PTS-STARTPTS,fps=30,scale=1920:-1:flags=bicubic[reference];[1:v]settb=AVTB,setpts=PTS-STARTPTS,fps=30,scale=1920:-1:flags=bicubic[distorted];[distorted][reference]libvmaf=log_fmt=json:log_path={self.vmaf_filename}:n_threads=4",
                '-f', 'null',
                '-'
            ]

            for arg in vmaf_command:
                print (arg, end = ' ')
            print('\n')

            result = subprocess.run(vmaf_command)
            if result.returncode != 0:
                print('ffmpeg vmaf failed.')
                sys.exit(1)

        def process_results(self):
            # Read VMAF and probe data
            with open(self.vmaf_filename, 'r') as f:
                vmaf_data = json.load(f)
            with open(self.ffprobe_filename, 'r') as f:
                probe_data = json.load(f)

            # Find video stream and get actual bitrate
            for stream in probe_data.get('streams', []):
                if stream.get('codec_type') == 'video':
                    self.actual_bitrate = stream.get('bit_rate')
                    break

            # Extract required data
            self.vmaf_harmonic_mean = vmaf_data["pooled_metrics"]["vmaf"]["harmonic_mean"]
            vmafs = [x["metrics"]["vmaf"] for x in vmaf_data["frames"]]
            self.vmaf_std_dev = statistics.stdev(vmafs)
            if self.actual_bitrate is not None:
                self.bpb = self.vmaf_harmonic_mean / math.log2(int(self.actual_bitrate))

            print (f"==================\nResults: {self.get_sub_experiment_name()}\n\tvmaf_harmonic_mean:{self.vmaf_harmonic_mean}\n\tvmaf_std_dev:{self.vmaf_std_dev}\n\tactual_bitrate:{self.actual_bitrate}\n\tbpb:{self.bpb}")

        def write_csv_row(self):
            # Prepare data row
            csv_row = (self.get_extra_csv_columns() +
            [
                #s3_link,
                self.video_filename,
                str(self.actual_bitrate) if self.actual_bitrate is not None else 'N/A',
                self.vmaf_harmonic_mean,
                self.vmaf_std_dev,
                str(self.bpb) if self.bpb is not None else 'N/A',
                str(self.transcode_seconds)
            ])

            # Append row to CSV
            with open(self.experiment.csv_file_name, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(csv_row)

        def get_extra_csv_columns(self):
            return []
