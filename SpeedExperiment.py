import Experiment

class SpeedExperiment(Experiment.Experiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('Speed', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return ['speed']
    
    def experiment_implementation(self):
        for speed in range(0, 7):
            sub_experiment = SpeedExperiment.SubExperiment(self, speed)
            sub_experiment.run_sub_experiment()

    class SubExperiment(Experiment.Experiment.SubExperiment):
        def __init__(self, experiment, speed):
            super().__init__(experiment, str(speed))
            self.speed = speed

        def get_extra_ffmpeg_parameters(self):
            return [
                '-speed', str(self.speed)
            ]
        
        def get_extra_csv_columns(self):
            return [
                str(self.speed)
            ]