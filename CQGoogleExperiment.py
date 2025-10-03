import CQGoogleExperimentBase

# Based on https://developers.google.com/media/vp9/settings/vod
class CQGoogleExperiment(CQGoogleExperimentBase.CQGoogleExperimentBase):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogle', input_video_file_name, output_video_file_basename)