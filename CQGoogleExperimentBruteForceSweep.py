import CQGoogleExperimentBase

# Based on https://developers.google.com/media/vp9/settings/vod
class CQGoogleExperimentBruteForceSweep(CQGoogleExperimentBase.CQGoogleExperimentBase):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogleBruteForceSweep', input_video_file_name, output_video_file_basename)

    def run_experiment_on_cq_params(self, resolution: tuple[int, int], cq_params: CQGoogleExperimentBase.CQExperiment.CQExperiment.SubExperiment.CQParams):
        super().run_experiment_on_cq_params(self, resolution, cq_params)

    def run_experiment_on_cq_sub_params(self, resolution: tuple[int, int], cq_params: CQGoogleExperimentBase.CQExperiment.CQExperiment.SubExperiment.CQParams):
        pass