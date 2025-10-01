import Experiment

class CRFExperiment(Experiment.Experiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CRF', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return ['crf']
    
    def run_experiment(self):
        super().run_experiment()

        for crf in range(0, 63, 5):
            CRFExperiment.SubExperiment(self, crf).run_sub_experiment()

        for crf in range(0, 63, 5):
            CRFExperiment.SubExperiment(self, crf, two_pass_encoding = True).run_sub_experiment()

    class SubExperiment(Experiment.Experiment.SubExperiment):
        def __init__(self, experiment, crf, two_pass_encoding = False):
            super().__init__(experiment, str(crf), two_pass_encoding)
            self.crf = crf

        def get_extra_ffmpeg_parameters(self):
            return [
                '-crf', str(self.crf)
            ]
        
        def get_extra_csv_columns(self):
            return [
                str(self.crf)
            ]