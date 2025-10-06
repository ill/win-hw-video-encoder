import CQExperiment
import Util

class CQGSunBruteForceSweep(CQExperiment.CQExperiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGSunBruteForceSweep', input_video_file_name, output_video_file_basename)

    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        crf_min = 0
        crf_max = 63
        crf_step = 4

        gsuns = [1.0, 1.5, 2.0, 2.5, 3.0]

        # Try the original bitrate and 30 fps
        # This is a set so if original bitrate is 30 we're good on a single set element
        framerates = {30, self.input_bitrate}

        min_bitrate_target_ratio_min = 0
        min_bitrate_target_ratio_max = 100
        min_bitrate_target_ratio_step = 10

        max_bitrate_target_ratio_min = 100
        max_bitrate_target_ratio_max = 200
        max_bitrate_target_ratio_step = 10

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
            for fps in framerates:
                for gsun in gsuns:
                    target_bitrate = int(resolution[0] * resolution[1] * float(fps) * gsun * Util.GSUN)

                    for min_bitrate_target_ratio in range(min_bitrate_target_ratio_min, min_bitrate_target_ratio_max, min_bitrate_target_ratio_step):
                        for max_bitrate_target_ratio in range(max_bitrate_target_ratio_min, max_bitrate_target_ratio_max, max_bitrate_target_ratio_step):
                            for threads in range(threads_min, threads_max + threads_step, threads_step):
                                for tile_columns in range(tile_columns_min, tile_columns_max + tile_columns_step,
                                                          tile_columns_step):
                                    cq_params = CQExperiment.CQExperiment.SubExperiment.CQParams()

                                    cq_params.crf = crf
                                    cq_params.target_bitrate = target_bitrate
                                    cq_params.min_bitrate = target_bitrate * min_bitrate_target_ratio
                                    cq_params.max_bitrate = target_bitrate * max_bitrate_target_ratio
                                    cq_params.threads = threads
                                    cq_params.tile_columns = tile_columns

                                    for speed_single_pass in range(speed_single_pass_min,
                                                                   speed_single_pass_max + speed_single_pass_step,
                                                                   speed_single_pass_step):
                                        cq_params.speed_single_pass = speed_single_pass

                                        self.run_experiment_on_cq_params_one_pass(resolution, cq_params=cq_params)

                                    for speed_pass_1 in range(speed_pass_1_min, speed_pass_1_max + speed_pass_1_step,
                                                              speed_pass_1_step):
                                        cq_params.speed_pass1 = speed_pass_1

                                        for speed_pass_2 in range(speed_pass_2_min, speed_pass_2_max + speed_pass_2_step,
                                                                  speed_pass_2_step):
                                            cq_params.speed_pass2 = speed_pass_2

                                            self.run_experiment_on_cq_params_two_pass(resolution, cq_params=cq_params)

    def run_experiment_on_cq_params_one_pass(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'==================\nRunning Resolution One Pass: {resolution}'
              f'{str(cq_params)}')

        # One Pass
        CQExperiment.CQExperiment.SubExperiment(self,
                                                cq_params=cq_params,
                                                output_width=resolution[0],
                                                output_height=resolution[1]).run_sub_experiment()

    def run_experiment_on_cq_params_two_pass(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'==================\nRunning Resolution Two Pass: {resolution}'
              f'{str(cq_params)}')

        # Two Pass
        CQExperiment.CQExperiment.SubExperiment(self,
                                                cq_params=cq_params,
                                                output_width=resolution[0],
                                                output_height=resolution[1],
                                                two_pass_encoding=True).run_sub_experiment()

    def run_experiment(self):
        super().run_experiment()

        for resolution in self.get_scaled_down_all_resolutions():
            self.run_experiment_on_resolution(resolution)