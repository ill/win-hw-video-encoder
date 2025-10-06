import CQGoogleExperimentBase

# Based on https://developers.google.com/media/vp9/settings/vod
class CQGoogleExperimentBruteForceSweep(CQGoogleExperimentBase.CQGoogleExperimentBase):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogleBruteForceSweep', input_video_file_name, output_video_file_basename)

    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        cq_params_base = CQGoogleExperimentBase.get_google_cq_params(resolution)

        crf_min = max(0, cq_params_base.crf - 20)
        crf_max = min(63, cq_params_base.crf + 20)
        crf_step = 4

        target_bitrate_min = max(0, cq_params_base.target_bitrate_kbps - 100)
        target_bitrate_max = cq_params_base.target_bitrate_kbps + 100
        target_bitrate_step = 10

        min_bitrate_kbps_min = max(0, cq_params_base.min_bitrate_kbps - 100)
        min_bitrate_kbps_max = cq_params_base.min_bitrate_kbps + 100
        min_bitrate_kbps_step = 50

        max_bitrate_kbps_min = max(0, cq_params_base.max_bitrate_kbps - 100)
        max_bitrate_kbps_max = cq_params_base.max_bitrate_kbps + 100
        max_bitrate_kbps_step = 50

        threads_min = 1
        threads_max = 16
        threads_step = 1

        tile_columns_min = 0
        tile_columns_max = (resolution[1] // 256) + 1
        tile_columns_step = 1

        speed_single_pass_min = 0
        speed_single_pass_max = 5
        speed_single_pass_step = 1

        speed_pass_1_min = 0
        speed_pass_1_max = 5
        speed_pass_1_step = 1

        speed_pass_2_min = 0
        speed_pass_2_max = 5
        speed_pass_2_step = 1

        for crf in range(crf_min, crf_max + crf_step, crf_step):
            for target_bitrate in range(target_bitrate_min, target_bitrate_max + target_bitrate_step, target_bitrate_step):
                for min_bitrate in range(min(min_bitrate_kbps_min, target_bitrate), min(min_bitrate_kbps_max, target_bitrate) + min_bitrate_kbps_step, min_bitrate_kbps_step):
                    for max_bitrate in range(max(max_bitrate_kbps_min, target_bitrate), max(max_bitrate_kbps_max, target_bitrate) + max_bitrate_kbps_step, max_bitrate_kbps_step):
                        for threads in range(threads_min, threads_max + threads_step, threads_step):
                            for tile_columns in range(tile_columns_min, tile_columns_max + tile_columns_step, tile_columns_step):
                                cq_params = CQGoogleExperimentBase.CQExperiment.CQExperiment.SubExperiment.CQParams()

                                cq_params.crf = crf
                                cq_params.target_bitrate = target_bitrate
                                cq_params.min_bitrate = min_bitrate
                                cq_params.max_bitrate = max_bitrate
                                cq_params.threads = threads
                                cq_params.tile_columns = tile_columns

                                for speed_single_pass in range(speed_single_pass_min, speed_single_pass_max + speed_single_pass_step, speed_single_pass_step):
                                    cq_params.speed_single_pass = speed_single_pass

                                    self.run_experiment_on_cq_params_one_pass(resolution, cq_params = cq_params)

                                for speed_pass_1 in range(speed_pass_1_min, speed_pass_1_max + speed_pass_1_step, speed_pass_1_step):
                                    cq_params.speed_pass1 = speed_pass_1

                                    for speed_pass_2 in range(speed_pass_2_min, speed_pass_2_max + speed_pass_2_step, speed_pass_2_step):
                                        cq_params.speed_pass2 = speed_pass_2

                                        self.run_experiment_on_cq_params_two_pass(resolution, cq_params=cq_params)
