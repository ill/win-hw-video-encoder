import CQExperiment

# Based on https://developers.google.com/media/vp9/settings/vod
class CQGoogleExperiment(CQExperiment.CQExperiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogle', input_video_file_name, output_video_file_basename)
    
    def run_experiment(self):
        super().run_experiment()

        for res in self.get_scaled_down_common_resolutions():
            print(f'==================\nRunning Resolution: {res}')

            if res[0] == 1920:
                CQGoogleExperiment.SubExperiment(self, crf=31, target_bitrate=1800, min_bitrate=900, max_bitrate=2610, output_width=res[0], output_height=res[1], threads=4).run_sub_experiment()
                CQGoogleExperiment.SubExperiment(self, crf=31, target_bitrate=1800, min_bitrate=900, max_bitrate=2610, output_width=res[0], output_height=res[1], threads=4, two_pass_encoding=True).run_sub_experiment()
            elif res[0] == 1280:
                CQGoogleExperiment.SubExperiment(self, crf=32, target_bitrate=1024, min_bitrate=512, max_bitrate=1485, output_width=res[0], output_height=res[1], threads=4).run_sub_experiment()
                CQGoogleExperiment.SubExperiment(self, crf=32, target_bitrate=1024, min_bitrate=512, max_bitrate=1485, output_width=res[0], output_height=res[1], threads=4, two_pass_encoding=True).run_sub_experiment()
            elif res[0] == 640:
                if res[1] <= 360:
                    CQGoogleExperiment.SubExperiment(self, crf=36, target_bitrate=276, min_bitrate=138, max_bitrate=400, output_width=res[0], output_height=res[1], threads=2).run_sub_experiment()
                    CQGoogleExperiment.SubExperiment(self, crf=36, target_bitrate=276, min_bitrate=138, max_bitrate=400, output_width=res[0], output_height=res[1], threads=2, two_pass_encoding=True).run_sub_experiment()
                else:
                    CQGoogleExperiment.SubExperiment(self, crf=33, target_bitrate=750, min_bitrate=375, max_bitrate=1088, output_width=res[0], output_height=res[1], threads=2).run_sub_experiment()
                    CQGoogleExperiment.SubExperiment(self, crf=33, target_bitrate=750, min_bitrate=375, max_bitrate=1088, output_width=res[0], output_height=res[1], threads=2, two_pass_encoding=True).run_sub_experiment()
            else:
                CQGoogleExperiment.SubExperiment(self, crf=37, target_bitrate=150, min_bitrate=75, max_bitrate=218, output_width=res[0], output_height=res[1]).run_sub_experiment()
                CQGoogleExperiment.SubExperiment(self, crf=37, target_bitrate=150, min_bitrate=75, max_bitrate=218, output_width=res[0], output_height=res[1], two_pass_encoding=True).run_sub_experiment()