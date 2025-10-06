import Experiment

class CQExperiment(Experiment.Experiment):
    def get_extra_csv_header_columns(self):
        return ['crf',
                'target_bitrate',
                'min_bitrate',
                'max_bitrate',
                'threads',
                'tile-columns',
                'speed',
                'speed_pass2']

    class SubExperiment(Experiment.Experiment.SubExperiment):
        class CQParams:
            crf: int = 32
            target_bitrate_kbps: int = 0
            min_bitrate_kbps: int = 0
            max_bitrate_kbps: int = 0
            threads: int = 1
            tile_columns: int = 1
            speed_single_pass: int = 0
            speed_pass1: int = 0
            speed_pass2: int = 0

            def __str__(self):
                return (f'\n\tcrf: {self.crf}'
                    f'\n\ttarget_bitrate_kbps: {self.target_bitrate_kbps}'
                    f'\n\tmin_bitrate_kbps: {self.min_bitrate_kbps}'
                    f'\n\tmax_bitrate_kbps: {self.max_bitrate_kbps}'
                    f'\n\tthreads: {self.threads}'
                    f'\n\ttile_columns: {self.tile_columns}'
                    f'\n\tspeed_single_pass: {self.speed_single_pass}'
                    f'\n\tspeed_pass1: {self.speed_pass1}'
                    f'\n\tspeed_pass2: {self.speed_pass2}')

        def __init__(self, experiment,
                     cq_params: CQParams,
                     output_width: int = -1,
                     output_height: int = -1,
                     output_fps: int = -1,
                     two_pass_encoding: bool = False):
            super().__init__(experiment,
                             f'crf-{cq_params.crf}'
                             f'-bp-{cq_params.target_bitrate_kbps}k'
                             f'-mnbp-{cq_params.min_bitrate_kbps}k'
                             f'-mxbp-{cq_params.max_bitrate_kbps}k'
                             f'-w-{output_width}'
                             f'-h-{output_height}'
                             f'-t-{cq_params.threads}'
                             f'-tc-{cq_params.tile_columns}'
                             f'-{"2Pass" if two_pass_encoding else "1Pass"}'
                             f'-{f"s1-{cq_params.speed_pass1}-s2-{cq_params.speed_pass2}" if two_pass_encoding else f"s-{cq_params.speed_single_pass}"}',
                             output_width = output_width,
                             output_height = output_height,
                             output_fps = output_fps,
                             two_pass_encoding = two_pass_encoding)
            self.cq_params = cq_params

        def get_extra_ffmpeg_parameters(self):
            return [
                '-crf', str(self.cq_params.crf),
                '-b:v', f'{self.cq_params.target_bitrate_kbps}k',
                '-minrate', f'{self.cq_params.min_bitrate_kbps}k',
                '-maxrate', f'{self.cq_params.max_bitrate_kbps}k',
                '-quality', 'good',
                '-threads', str(self.cq_params.threads),
                '-tile-columns', str(self.cq_params.tile_columns)
            ]
        
        def get_extra_ffmpeg_parameters_single_pass(self):
            return (self.get_extra_ffmpeg_parameters()
                + [
                    '-speed', str(self.cq_params.speed_single_pass)
                ])
        
        def get_extra_ffmpeg_parameters_pass1(self):
            return (self.get_extra_ffmpeg_parameters()
                + [
                    '-speed', str(self.cq_params.speed_pass1)
                ])
        
        def get_extra_ffmpeg_parameters_pass2(self):
            return (self.get_extra_ffmpeg_parameters()
                + [
                    '-speed', str(self.cq_params.speed_pass2)
                ])
        
        def get_extra_csv_columns(self):
            return [
                str(self.cq_params.crf),
                f'{self.cq_params.target_bitrate_kbps}k',
                f'{self.cq_params.min_bitrate_kbps}k',
                f'{self.cq_params.max_bitrate_kbps}k',
                str(self.cq_params.threads),
                str(self.cq_params.tile_columns),
                str(self.cq_params.speed_pass1) if self.two_pass_encoding else str(self.cq_params.speed_single_pass),
                str(self.cq_params.speed_pass2) if self.two_pass_encoding else 'N/A'
            ]