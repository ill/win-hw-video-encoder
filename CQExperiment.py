import Experiment

class CQExperiment(Experiment.Experiment):
    def get_extra_csv_header_columns(self):
        return ['crf',
                'target_bitrate',
                'min_bitrate',
                'max_bitrate']

    class SubExperiment(Experiment.Experiment.SubExperiment):
        def __init__(self, experiment, crf, target_bitrate, min_bitrate, max_bitrate, output_width: int = 1920, output_height: int = 1080, two_pass_encoding = False):
            super().__init__(experiment, f'crf-{crf}-bp-{target_bitrate}-mnbp-{min_bitrate}-mxbp-{max_bitrate}-w-{output_width}-h-{output_height}-{"2Pass" if two_pass_encoding else "1Pass"}', output_width, output_height, two_pass_encoding)
            self.crf = crf
            self.target_bitrate = target_bitrate
            self.min_bitrate = min_bitrate
            self.max_bitrate = max_bitrate

        # Some of this is currently hardcoded for 1080p, I'll make that more configurable later

        def get_extra_ffmpeg_parameters(self):
            return [
                '-crf', str(self.crf),
                '-b:v', str(self.target_bitrate),
                '-minrate', str(self.min_bitrate),
                '-maxrate', str(self.max_bitrate),
                '-quality', 'good',
                '-threads', '4',
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
                str(self.target_bitrate),
                str(self.min_bitrate),
                str(self.max_bitrate)
            ]