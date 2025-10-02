import Experiment

class CQExperiment(Experiment.Experiment):
    def get_extra_csv_header_columns(self):
        return ['crf',
                'target_bitrate',
                'min_bitrate',
                'max_bitrate']

    class SubExperiment(Experiment.Experiment.SubExperiment):
        def __init__(self, experiment, crf, target_bitrate_kbps, min_bitrate_kbps, max_bitrate_kbps, output_width: int = 1920, output_height: int = 1080, threads: int = 1, two_pass_encoding: bool = False):
            super().__init__(experiment, f'crf-{crf}-bp-{target_bitrate_kbps}k-mnbp-{min_bitrate_kbps}k-mxbp-{max_bitrate_kbps}k-w-{output_width}-h-{output_height}-t-{threads}-{"2Pass" if two_pass_encoding else "1Pass"}', output_width, output_height, two_pass_encoding)
            self.crf = crf
            self.target_bitrate_kbps = target_bitrate_kbps
            self.min_bitrate_kbps = min_bitrate_kbps
            self.max_bitrate_kbps = max_bitrate_kbps
            self.threads = threads

        # Some of this is currently hardcoded for 1080p, I'll make that more configurable later

        def get_extra_ffmpeg_parameters(self):
            return [
                '-crf', str(self.crf),
                '-b:v', f'{self.target_bitrate_kbps}k',
                '-minrate', f'{self.min_bitrate_kbps}k',
                '-maxrate', f'{self.max_bitrate_kbps}k',
                '-quality', 'good',
                '-threads', str(self.threads),
                '-tile-columns', '2'
            ]
        
        def get_extra_ffmpeg_parameters_pass1(self):
            return (self.get_extra_ffmpeg_parameters()
                + [
                    '-speed', '4'
                ])
        
        def get_extra_ffmpeg_parameters_pass2(self):
            return (self.get_extra_ffmpeg_parameters()
                + [
                    '-speed', '2'
                ])
        
        def get_extra_csv_columns(self):
            return [
                str(self.crf),
                f'{self.target_bitrate_kbps}k',
                f'{self.min_bitrate_kbps}k',
                f'{self.max_bitrate_kbps}k'
            ]