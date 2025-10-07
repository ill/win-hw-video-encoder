import math

import CQExperiment
import Util

class CQGSunBruteForceSweep(CQExperiment.CQExperiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGSunBruteForceSweep', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return [
            'gsun',
            'min_bitrate_pct',
            'max_bitrate_pct',
        ] + super().get_extra_csv_header_columns()

    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        crf_from = 29
        crf_to = 36
        crf_step = 1

        gsuns = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75]

        # Try the original bitrate and 30 fps
        # This is a set so if original bitrate is 30 we're good on a single set element
        framerates = {30}#{30, self.input_fps}

        min_bitrate_pct_from = 50
        min_bitrate_pct_to = 50
        min_bitrate_pct_step = -10

        max_bitrate_pct_from = 150
        max_bitrate_pct_to = 150
        max_bitrate_pct_step = -10

        threads_from = 16
        threads_to = 16
        threads_step = -4

        tile_columns_base = math.floor(math.log2(resolution[0] / Util.VP9_TILE_DIM)) if resolution[0] > Util.VP9_TILE_DIM else 0
        tile_columns_from = tile_columns_base
        tile_columns_to = tile_columns_base
        tile_columns_step = -1

        speed_single_pass_from = 0
        speed_single_pass_to = 0
        speed_single_pass_step = 1

        speed_pass_1_from = 0
        speed_pass_1_to = 0
        speed_pass_1_step = 1

        speed_pass_2_from = 0
        speed_pass_2_to = 0
        speed_pass_2_step = 1

        one_pass_encoding = True
        two_pass_encoding = True

        print(f'{Util.HEADER}\nSweeping Values Between')
        print(f'\tcrf: {crf_from} - {crf_to} step: {crf_step}')
        print(f'\tgsuns: {min(gsuns)} - {max(gsuns)}')
        print(f'\tframerates:', end = ' ')
        Util.print_collection(framerates)
        print(f'\ttarget_bitrates: {Util.get_target_bitrate_kbps(resolution[0], resolution[1], min(framerates), min(gsuns))} - {Util.get_target_bitrate_kbps(resolution[0], resolution[1], max(framerates), max(gsuns))}')
        print(f'\tthreads: {threads_from} - {threads_to} step: {threads_step}')
        print(f'\ttile_columns: {tile_columns_from} - {tile_columns_to} step: {tile_columns_step}')

        for crf in Util.inclusive_range(crf_from,
                                        crf_to,
                                        crf_step):
            for fps in framerates:
                for gsun in gsuns:
                    target_bitrate = Util.get_target_bitrate_kbps(resolution[0], resolution[1], fps, gsun)

                    for min_bitrate_pct in Util.inclusive_range(min_bitrate_pct_from,
                                                                min_bitrate_pct_to,
                                                                min_bitrate_pct_step):
                        for max_bitrate_pct in Util.inclusive_range(max_bitrate_pct_from,
                                                                    max_bitrate_pct_to,
                                                                    max_bitrate_pct_step):
                            for threads in Util.inclusive_range(threads_from,
                                                                threads_to,
                                                                threads_step):
                                for tile_columns in Util.inclusive_range(tile_columns_from,
                                                                         tile_columns_to,
                                                                         tile_columns_step):

                                    if one_pass_encoding:
                                        for speed_single_pass in Util.inclusive_range(speed_single_pass_from,
                                                                                      speed_single_pass_to,
                                                                                      speed_single_pass_step):
                                            cq_params = CQExperiment.CQExperiment.SubExperiment.CQParams()

                                            cq_params.crf = crf
                                            cq_params.target_bitrate_kbps = target_bitrate
                                            cq_params.min_bitrate_kbps = int(target_bitrate * (min_bitrate_pct / 100))
                                            cq_params.max_bitrate_kbps = int(target_bitrate * (max_bitrate_pct / 100))
                                            cq_params.threads = threads
                                            cq_params.tile_columns = tile_columns

                                            cq_params.speed_single_pass = speed_single_pass

                                            self.run_experiment_on_cq_params_one_pass(gsun=gsun,
                                                                                      min_bitrate_pct=min_bitrate_pct,
                                                                                      max_bitrate_pct=max_bitrate_pct,
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
                                                cq_params.target_bitrate_kbps = target_bitrate
                                                cq_params.min_bitrate_kbps = int(target_bitrate * (min_bitrate_pct / 100))
                                                cq_params.max_bitrate_kbps = int(target_bitrate * (max_bitrate_pct / 100))
                                                cq_params.threads = threads
                                                cq_params.tile_columns = tile_columns

                                                cq_params.speed_pass1 = speed_pass_1
                                                cq_params.speed_pass2 = speed_pass_2

                                                self.run_experiment_on_cq_params_two_pass(gsun=gsun,
                                                                                          min_bitrate_pct=min_bitrate_pct,
                                                                                          max_bitrate_pct=max_bitrate_pct,
                                                                                          resolution=resolution,
                                                                                          fps=fps,
                                                                                          cq_params=cq_params)

    def run_experiment_on_cq_params_one_pass(self,
                                             gsun: float,
                                             min_bitrate_pct: int,
                                             max_bitrate_pct: int,
                                             resolution: tuple[int, int],
                                             fps: int,
                                             cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution One Pass: {resolution}'
              f'{str(cq_params)}')

        # One Pass
        CQGSunBruteForceSweep.SubExperiment(self,
                                            gsun=gsun,
                                            min_bitrate_pct=min_bitrate_pct,
                                            max_bitrate_pct=max_bitrate_pct,
                                            cq_params=cq_params,
                                            output_width=resolution[0],
                                            output_height=resolution[1],
                                            output_fps=fps).run_sub_experiment()

    def run_experiment_on_cq_params_two_pass(self,
                                             gsun: float,
                                             min_bitrate_pct: int,
                                             max_bitrate_pct: int,
                                             resolution: tuple[int, int],
                                             fps: int,
                                             cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution Two Pass: {resolution}'
              f'{str(cq_params)}')

        # Two Pass
        CQGSunBruteForceSweep.SubExperiment(self,
                                            gsun=gsun,
                                            min_bitrate_pct=min_bitrate_pct,
                                            max_bitrate_pct=max_bitrate_pct,
                                            cq_params=cq_params,
                                            output_width=resolution[0],
                                            output_height=resolution[1],
                                            output_fps=fps,
                                            two_pass_encoding=True).run_sub_experiment()

    def run_experiment(self):
        super().run_experiment()

        for resolution in self.get_scaled_down_all_resolutions():
            self.run_experiment_on_resolution(resolution)

    class SubExperiment(CQExperiment.CQExperiment.SubExperiment):
        def __init__(self, experiment,
                     gsun: float,
                     min_bitrate_pct: int,
                     max_bitrate_pct: int,
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
            self.gsun = gsun
            self.min_bitrate_pct = min_bitrate_pct
            self.max_bitrate_pct = max_bitrate_pct

        def get_extra_csv_columns(self):
            return [
                str(self.gsun),
                str(self.min_bitrate_pct),
                str(self.max_bitrate_pct),
            ] + super().get_extra_csv_columns()