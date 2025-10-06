import CQExperiment

# Based on https://developers.google.com/media/vp9/settings/vod
def get_google_cq_params(resolution: tuple[int, int]) -> CQExperiment.CQExperiment.SubExperiment.CQParams:
    cq_params = CQExperiment.CQExperiment.SubExperiment.CQParams()

    # Based on https://developers.google.com/media/vp9/settings/vod
    # kinda janky way to figure out settings based on the table
    # This can be improved a lot in many ways if needed, like better interpolation between resolutions to find a more ideal bitrate
    # Or extrapolating beyond resolutions in their table
    # Also I'm not handling things in their tables past 1080p yet

    if resolution[0] > 1280:  # 1920
        cq_params.target_bitrate_kbps = 1800
        cq_params.min_bitrate_kbps = 900
        cq_params.max_bitrate_kbps = 2610
        cq_params.tile_columns = 2

    elif resolution[0] > 640:  # 1280
        cq_params.target_bitrate_kbps = 1024
        cq_params.min_bitrate_kbps = 512
        cq_params.max_bitrate_kbps = 1485
        cq_params.tile_columns = 2

    elif resolution[0] > 320:
        if resolution[1] > 360:  # 640x480
            cq_params.target_bitrate_kbps = 750
            cq_params.min_bitrate_kbps = 375
            cq_params.max_bitrate_kbps = 1088
            cq_params.tile_columns = 1

        else:  # 640x360
            cq_params.target_bitrate_kbps = 276
            cq_params.min_bitrate_kbps = 138
            cq_params.max_bitrate_kbps = 400
            cq_params.tile_columns = 1

    else:  # 320
        cq_params.target_bitrate_kbps = 150
        cq_params.min_bitrate_kbps = 75
        cq_params.max_bitrate_kbps = 218
        cq_params.tile_columns = 0

    if resolution[1] > 720:  # 1080p
        cq_params.crf = 31
        cq_params.threads = 4
        cq_params.speed_single_pass = 2
        cq_params.speed_pass1 = 4
        cq_params.speed_pass2 = 2

    elif resolution[1] > 480:  # 720p
        cq_params.crf = 32
        cq_params.threads = 4
        cq_params.speed_single_pass = 2
        cq_params.speed_pass1 = 4
        cq_params.speed_pass2 = 2

    elif resolution[1] > 360:  # 480p
        cq_params.crf = 33
        cq_params.threads = 2
        cq_params.speed_single_pass = 1
        cq_params.speed_pass1 = 4
        cq_params.speed_pass2 = 1

    elif resolution[1] > 240:  # 360p
        cq_params.crf = 36
        cq_params.threads = 2
        cq_params.speed_single_pass = 1
        cq_params.speed_pass1 = 4
        cq_params.speed_pass2 = 1

    else:
        cq_params.crf = 37
        cq_params.threads = 1
        cq_params.speed_single_pass = 1
        cq_params.speed_pass1 = 4
        cq_params.speed_pass2 = 1

    return cq_params

class CQGoogleExperimentBase(CQExperiment.CQExperiment):
    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        self.run_experiment_on_cq_params(resolution, get_google_cq_params(resolution))

    def run_experiment_on_cq_params(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        self.run_experiment_on_cq_params_one_pass(resolution, cq_params)
        self.run_experiment_on_cq_params_two_pass(resolution, cq_params)

    def run_experiment_on_cq_params_one_pass(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'==================\nRunning Resolution One Pass: {resolution}'
              f'{str(cq_params)}')

        # One Pass
        CQGoogleExperimentBase.SubExperiment(self,
                                             cq_params=cq_params,
                                             output_width=resolution[0],
                                             output_height=resolution[1]).run_sub_experiment()

    def run_experiment_on_cq_params_two_pass(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'==================\nRunning Resolution Two Pass: {resolution}'
              f'{str(cq_params)}')

        # Two Pass
        CQGoogleExperimentBase.SubExperiment(self,
                                             cq_params=cq_params,
                                             output_width=resolution[0],
                                             output_height=resolution[1],
                                             two_pass_encoding=True).run_sub_experiment()

    def run_experiment(self):
        super().run_experiment()

        for resolution in self.get_scaled_down_all_resolutions():
            self.run_experiment_on_resolution(resolution)