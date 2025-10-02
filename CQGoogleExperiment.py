import Experiment

# Based on https://developers.google.com/media/vp9/settings/vod
# I'll later add support for other screen resolutions, for now it's only testing 1080p

class CQGoogleExperiment(Experiment.Experiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogle', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return ['crf',
                'target_bitrate',
                'min_bitrate',
                'max_bitrate']
    
    def run_experiment(self):
        super().run_experiment()

        # for crf in range(0, 63, 5):
        #     CQGoogleExperiment.SubExperiment(self, crf).run_sub_experiment()

        # for crf in range(0, 63, 5):
        #     CQGoogleExperiment.SubExperiment(self, crf, two_pass_encoding = True).run_sub_experiment()

        CQGoogleExperiment.SubExperiment(self, crf=31, target_bitrate=1800, min_bitrate=900, max_bitrate=2610).run_sub_experiment()
        CQGoogleExperiment.SubExperiment(self, crf=31, target_bitrate=1800, min_bitrate=900, max_bitrate=2610, two_pass_encoding=True).run_sub_experiment()

    class SubExperiment(Experiment.Experiment.SubExperiment):
        def __init__(self, experiment, crf, target_bitrate, min_bitrate, max_bitrate, two_pass_encoding = False):
            super().__init__(experiment, f'crf:{crf}', two_pass_encoding)
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
        
        def get_extra_ffmpeg_parameters_pass1(self):
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