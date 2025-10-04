import CQGoogleExperimentBase

# Based on https://developers.google.com/media/vp9/settings/vod
class CQGoogleExperimentBruteForceSweep(CQGoogleExperimentBase.CQGoogleExperimentBase):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogleBruteForceSweep', input_video_file_name, output_video_file_basename)

    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        cq_params_base = CQGoogleExperimentBase.get_google_cq_params(resolution)

        super().run_experiment_on_cq_params(resolution=resolution, cq_params=cq_params_base)
