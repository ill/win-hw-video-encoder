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
                'speed_2']

    class SubExperiment(Experiment.Experiment.SubExperiment):
        class CQParams:
            crf: int = 32
            target_bitrate_kbps: int = 0
            min_bitrate_kbps: int = 0
            max_bitrate_kbps: int = 0
            threads: int = 1
            tile_columns: int = 1
            speed: int = 0
            speed_pass2: int = 0

        def __init__(self, experiment,
                     cq_params: CQParams,
                     output_width: int = 1920,
                     output_height: int = 1080,
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
                             f'-s-{cq_params.speed}'
                             f'-s2-{cq_params.speed_pass2}'
                             f'-{"2Pass" if two_pass_encoding else "1Pass"}',
                             output_width,
                             output_height,
                             two_pass_encoding)
            self.cq_params = cq_params

        # Some of this is currently hardcoded for 1080p, I'll make that more configurable later

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
                    '-speed', str(self.cq_params.speed)
                ])
        
        def get_extra_ffmpeg_parameters_pass1(self):
            return (self.get_extra_ffmpeg_parameters()
                + [
                    '-speed', str(self.cq_params.speed)
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
                str(self.cq_params.speed),
                str(self.cq_params.speed_pass2)
            ]