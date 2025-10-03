import CQExperiment

# Based on https://developers.google.com/media/vp9/settings/vod
class CQGoogleExperiment(CQExperiment.CQExperiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogle', input_video_file_name, output_video_file_basename)
    
    def run_experiment(self):
        super().run_experiment()

        for res in self.get_scaled_down_all_resolutions():
            print(f'==================\nRunning Resolution: {res}')

            crf = 32

            target_bitrate_kbps = 0
            min_bitrate_kbps = 0
            max_bitrate_kbps = 0

            threads = 1
            tile_columns = 0
            speed = 0

            # kinda janky way to figure out settings based on the table

            if res[0] > 1280:       # 1920
                target_bitrate_kbps = 1800
                min_bitrate_kbps = 900
                max_bitrate_kbps = 2610
                tile_columns = 2

            elif res[0] > 640:      # 1280
                target_bitrate_kbps = 1024
                min_bitrate_kbps = 512
                max_bitrate_kbps = 1485
                tile_columns = 2

            elif res[0] > 320:      
                if res[1] > 360:    # 640x480
                    target_bitrate_kbps = 750
                    min_bitrate_kbps = 375
                    max_bitrate_kbps = 1088
                    tile_columns = 1

                else:               # 640x360
                    target_bitrate_kbps = 276
                    min_bitrate_kbps = 138
                    max_bitrate_kbps = 400
                    tile_columns = 1

            else:                   #320
                target_bitrate_kbps = 150
                min_bitrate_kbps = 75
                max_bitrate_kbps = 218
                tile_columns = 0
            
            if res[1] > 720:    # 1080p
                crf = 31
                threads = 4
                speed = 2

            elif res[1] > 480:  # 720p
                crf = 32
                threads = 4
                speed = 2

            elif res[1] > 360:  # 480p
                crf = 33
                threads = 2
                speed = 1

            elif res[1] > 240:  # 360p
                crf = 36
                threads = 2
                speed = 1

            else:
                crf = 37
                threads = 1
                speed = 1

            print(f'==================\n\tcrf: {crf}'
                  f'\n\ttarget_bitrate_kbps: {target_bitrate_kbps}'
                  f'\n\tmin_bitrate_kbps: {min_bitrate_kbps}'
                  f'\n\tmax_bitrate_kbps: {max_bitrate_kbps}'
                  f'\n\tthreads: {threads}'
                  f'\n\ttile_columns: {tile_columns}'
                  f'\n\tspeed: {speed}')    

            # One Pass
            CQGoogleExperiment.SubExperiment(self, 
                                             crf = crf, 
                                             target_bitrate_kbps = target_bitrate_kbps, 
                                             min_bitrate_kbps = min_bitrate_kbps, 
                                             max_bitrate_kbps = max_bitrate_kbps, 
                                             output_width = res[0], 
                                             output_height = res[1], 
                                             threads = threads, 
                                             tile_columns = tile_columns, 
                                             speed = speed).run_sub_experiment()
            
            # Two Pass
            CQGoogleExperiment.SubExperiment(self, 
                                             crf = crf, 
                                             target_bitrate_kbps = target_bitrate_kbps, 
                                             min_bitrate_kbps = min_bitrate_kbps, 
                                             max_bitrate_kbps = max_bitrate_kbps, 
                                             output_width = res[0], 
                                             output_height = res[1], 
                                             threads = threads, 
                                             tile_columns = tile_columns, 
                                             speed = 4,
                                             speed_2 = speed,
                                             two_pass_encoding = True).run_sub_experiment()