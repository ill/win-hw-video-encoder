import CQExperiment

# Based on https://developers.google.com/media/vp9/settings/vod
class CQGoogleExperiment(CQExperiment.CQExperiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogle', input_video_file_name, output_video_file_basename)

    def run_experiment(self):
        super().run_experiment()

        for res in self.get_scaled_down_all_resolutions():
            print(f'==================\nRunning Resolution: {res}')

            cq_params = CQExperiment.CQExperiment.SubExperiment.CQParams()

            # kinda janky way to figure out settings based on the table

            if res[0] > 1280:       # 1920
                cq_params.target_bitrate_kbps = 1800
                cq_params.min_bitrate_kbps = 900
                cq_params.max_bitrate_kbps = 2610
                cq_params.tile_columns = 2

            elif res[0] > 640:      # 1280
                cq_params.target_bitrate_kbps = 1024
                cq_params.min_bitrate_kbps = 512
                cq_params.max_bitrate_kbps = 1485
                cq_params.tile_columns = 2

            elif res[0] > 320:      
                if res[1] > 360:    # 640x480
                    cq_params.target_bitrate_kbps = 750
                    cq_params.min_bitrate_kbps = 375
                    cq_params.max_bitrate_kbps = 1088
                    cq_params.tile_columns = 1

                else:               # 640x360
                    cq_params.target_bitrate_kbps = 276
                    cq_params.min_bitrate_kbps = 138
                    cq_params.max_bitrate_kbps = 400
                    cq_params.tile_columns = 1

            else:                   #320
                cq_params.target_bitrate_kbps = 150
                cq_params.min_bitrate_kbps = 75
                cq_params.max_bitrate_kbps = 218
                cq_params.tile_columns = 0
            
            if res[1] > 720:    # 1080p
                cq_params.crf = 31
                cq_params.threads = 4
                cq_params.speed = 2

            elif res[1] > 480:  # 720p
                cq_params.crf = 32
                cq_params.threads = 4
                cq_params.speed = 2

            elif res[1] > 360:  # 480p
                cq_params.crf = 33
                cq_params.threads = 2
                cq_params.speed = 1

            elif res[1] > 240:  # 360p
                cq_params.crf = 36
                cq_params.threads = 2
                cq_params.speed = 1

            else:
                cq_params.crf = 37
                cq_params.threads = 1
                cq_params.speed = 1

            print(f'=================='
                  f'\n\tcrf: {cq_params.crf}'
                  f'\n\ttarget_bitrate_kbps: {cq_params.target_bitrate_kbps}'
                  f'\n\tmin_bitrate_kbps: {cq_params.min_bitrate_kbps}'
                  f'\n\tmax_bitrate_kbps: {cq_params.max_bitrate_kbps}'
                  f'\n\tthreads: {cq_params.threads}'
                  f'\n\ttile_columns: {cq_params.tile_columns}'
                  f'\n\tspeed: {cq_params.speed}')

            # One Pass
            CQGoogleExperiment.SubExperiment(self,
                                             cq_params = cq_params,
                                             output_width = res[0], 
                                             output_height = res[1]).run_sub_experiment()

            cq_params.speed_pass2 = cq_params.speed
            cq_params.speed = 4

            # Two Pass
            CQGoogleExperiment.SubExperiment(self,
                                             cq_params=cq_params,
                                             output_width=res[0],
                                             output_height=res[1],
                                             two_pass_encoding = True).run_sub_experiment()