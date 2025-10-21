import math

import CQExperiment
import Util

class CQGSunBounded(CQExperiment.CQExperiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGSunBounded', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return [
            'upper_gsun',
        ] + super().get_extra_csv_header_columns()

    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        crf_from = 32
        crf_to = 35
        crf_step = 1

        upper_gsuns = [3.0, 4.0, 5.0]

        # Try the original bitrate and 30 fps
        # This is a set so if original bitrate is 30 we're good on a single set element
        framerates = {30}#{30, self.input_fps}

        tile_columns_base = Util.get_tile_columns(resolution[0])

        speed_single_pass_from = 0
        speed_single_pass_to = 0
        speed_single_pass_step = 1

        speed_pass_1_from = 0
        speed_pass_1_to = 0
        speed_pass_1_step = 1

        speed_pass_2_from = 0
        speed_pass_2_to = 0
        speed_pass_2_step = 1

        one_pass_encoding = False
        two_pass_encoding = True

        print(f'{Util.HEADER}\nSweeping Values Between')
        print(f'\tcrf: {crf_from} - {crf_to} step: {crf_step}')

        for crf in Util.inclusive_range(crf_from,
                                        crf_to,
                                        crf_step):
            for fps in framerates:
                for upper_gsun in upper_gsuns:
                    upper_bitrate = Util.get_target_bitrate_kbps(resolution[0], resolution[1], fps, upper_gsun)

                    if one_pass_encoding:
                        for speed_single_pass in Util.inclusive_range(speed_single_pass_from,
                                                                      speed_single_pass_to,
                                                                      speed_single_pass_step):
                            cq_params = CQExperiment.CQExperiment.SubExperiment.CQParams()

                            cq_params.crf = crf
                            cq_params.target_bitrate_kbps = -1
                            cq_params.min_bitrate_kbps = -1
                            cq_params.max_bitrate_kbps = upper_bitrate
                            cq_params.threads = 16
                            cq_params.tile_columns = tile_columns_base

                            cq_params.speed_single_pass = speed_single_pass

                            self.run_experiment_on_cq_params_one_pass(upper_gsun=upper_gsun,
                                                                      resolution=resolution,
                                                                      fps=fps,
                                                                      cq_params=cq_params)

                    if two_pass_encoding:
                        for speed_pass_1 in Util.inclusive_range(speed_pass_1_from,
                                                                 speed_pass_1_to,
                                                                 speed_pass_1_step):
                            for speed_pass_2 in Util.inclusive_range(speed_pass_2_from,
                                                                     speed_pass_2_to,
                                                                     speed_pass_2_step):
                                cq_params = CQExperiment.CQExperiment.SubExperiment.CQParams()

                                cq_params.crf = crf
                                cq_params.target_bitrate_kbps = -1
                                cq_params.min_bitrate_kbps = -1
                                cq_params.max_bitrate_kbps = upper_bitrate
                                cq_params.threads = 16
                                cq_params.tile_columns = tile_columns_base

                                cq_params.speed_pass1 = speed_pass_1
                                cq_params.speed_pass2 = speed_pass_2

                                self.run_experiment_on_cq_params_two_pass(upper_gsun=upper_gsun,
                                                                          resolution=resolution,
                                                                          fps=fps,
                                                                          cq_params=cq_params)

    def run_experiment_on_cq_params_one_pass(self,
                                             upper_gsun: float,
                                             resolution: tuple[int, int],
                                             fps: int,
                                             cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution One Pass: {resolution}'
              f'{str(cq_params)}')

        # One Pass
        CQGSunBounded.SubExperiment(self,
                                    upper_gsun=upper_gsun,
                                    cq_params=cq_params,
                                    output_width=resolution[0],
                                    output_height=resolution[1],
                                    output_fps=fps).run_sub_experiment()

    def run_experiment_on_cq_params_two_pass(self,
                                             upper_gsun: float,
                                             resolution: tuple[int, int],
                                             fps: int,
                                             cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution Two Pass: {resolution}'
              f'{str(cq_params)}')

        # Two Pass
        CQGSunBounded.SubExperiment(self,
                                    upper_gsun=upper_gsun,
                                    cq_params=cq_params,
                                    output_width=resolution[0],
                                    output_height=resolution[1],
                                    output_fps=fps,
                                    two_pass_encoding=True).run_sub_experiment()

    def experiment_implementation(self):
        for resolution in self.get_scaled_down_to_fit_resolutions([
            Util.RES_1080p,
            Util.RES_720p
        ]):
            self.run_experiment_on_resolution(resolution)

        #self.run_experiment_on_resolution(resolution=self.scale_down_to_fit(1280, 720))

    class SubExperiment(CQExperiment.CQExperiment.SubExperiment):
        def __init__(self, experiment,
                     upper_gsun: float,
                     cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams,
                     output_width: int = -1,
                     output_height: int = -1,
                     output_fps: int = -1,
                     two_pass_encoding: bool = False):
            super().__init__(experiment,
                             cq_params = cq_params,
                             output_width = output_width,
                             output_height = output_height,
                             output_fps = output_fps,
                             two_pass_encoding = two_pass_encoding)
            self.upper_gsun = upper_gsun

        def get_extra_csv_columns(self):
            return [
                str(self.upper_gsun),
            ] + super().get_extra_csv_columns()