import Experiment

class QualityExperiment(Experiment.Experiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('Quality', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return ['quality']
    
    def run_experiment(self):
        super().run_experiment()

        QualityExperiment.SubExperiment(self, 'good').run_sub_experiment()
        QualityExperiment.SubExperiment(self, 'realtime').run_sub_experiment()
        QualityExperiment.SubExperiment(self, 'best').run_sub_experiment()

    class SubExperiment(Experiment.Experiment.SubExperiment):
        def __init__(self, experiment, quality):
            super().__init__(experiment, quality)
            self.crf = quality

        def get_extra_ffmpeg_parameters(self):
            return [
                '-quality', self.quality
            ]
        
        def get_extra_csv_columns(self):
            return [
                self.quality
            ]