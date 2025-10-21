import math

import CQExperiment
import Util

class CQGoogleGSunExperiment(CQExperiment.CQExperiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CQGoogleGSunExperiment', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return [
            'gsun',
        ] + super().get_extra_csv_header_columns()

    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        gsuns = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

        one_pass_encoding = True
        two_pass_encoding = True

        print(f'{Util.HEADER}\nSweeping Values Between')
        print(f'\tgsuns: {min(gsuns)} - {max(gsuns)}')
        print(f'\ttarget_bitrates: {Util.get_target_bitrate_kbps(resolution[0], resolution[1], 30, min(gsuns))} - {Util.get_target_bitrate_kbps(resolution[0], resolution[1], 30, max(gsuns))}')

        for gsun in gsuns:
            target_bitrate = Util.get_target_bitrate_kbps(resolution[0], resolution[1], 30, gsun)

            if one_pass_encoding:
                cq_params = CQExperiment.get_google_cq_params(resolution)

                cq_params.target_bitrate_kbps = target_bitrate
                cq_params.min_bitrate_kbps = int(float(target_bitrate) * 0.5)
                cq_params.max_bitrate_kbps = int(float(target_bitrate) * 1.5)
                cq_params.speed_single_pass = 0

                self.run_experiment_on_cq_params_one_pass(gsun=gsun,
                                                          resolution=resolution,
                                                          cq_params=cq_params)

            if two_pass_encoding:
                cq_params = CQExperiment.get_google_cq_params(resolution)

                cq_params.target_bitrate_kbps = target_bitrate
                cq_params.min_bitrate_kbps = int(float(target_bitrate) * 0.5)
                cq_params.max_bitrate_kbps = int(float(target_bitrate) * 1.5)
                cq_params.speed_pass1 = 0
                cq_params.speed_pass2 = 0

                self.run_experiment_on_cq_params_two_pass(gsun=gsun,
                                                          resolution=resolution,
                                                          cq_params=cq_params)

    def run_experiment_on_cq_params_one_pass(self,
                                             gsun: float,
                                             resolution: tuple[int, int],
                                             cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution One Pass: {resolution}'
              f'{str(cq_params)}')

        # One Pass
        CQGoogleGSunExperiment.SubExperiment(self,
                                            gsun=gsun,
                                            cq_params=cq_params,
                                            output_width=resolution[0],
                                            output_height=resolution[1]).run_sub_experiment()

    def run_experiment_on_cq_params_two_pass(self,
                                             gsun: float,
                                             resolution: tuple[int, int],
                                             cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution Two Pass: {resolution}'
              f'{str(cq_params)}')

        # Two Pass
        CQGoogleGSunExperiment.SubExperiment(self,
                                            gsun=gsun,
                                            cq_params=cq_params,
                                            output_width=resolution[0],
                                            output_height=resolution[1],
                                            two_pass_encoding=True).run_sub_experiment()

    def experiment_implementation(self):
        for resolution in self.get_scaled_down_all_resolutions():
            self.run_experiment_on_resolution(resolution)

        #self.run_experiment_on_resolution(resolution=self.scale_down_to_fit(1280, 720))

    class SubExperiment(CQExperiment.CQExperiment.SubExperiment):
        def __init__(self, experiment,
                     gsun: float,
                     cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams,
                     output_width: int = -1,
                     output_height: int = -1,
                     two_pass_encoding: bool = False):
            super().__init__(experiment,
                             cq_params = cq_params,
                             output_width = output_width,
                             output_height = output_height,
                             output_fps = 30,
                             two_pass_encoding = two_pass_encoding)
            self.gsun = gsun

        def get_extra_csv_columns(self):
            return [
                str(self.gsun),
            ] + super().get_extra_csv_columns()