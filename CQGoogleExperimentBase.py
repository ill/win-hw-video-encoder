import CQExperiment
import Util

class CQGoogleExperimentBase(CQExperiment.CQExperiment):
    def run_experiment_on_resolution(self, resolution: tuple[int, int]):
        self.run_experiment_on_cq_params(resolution, CQExperiment.get_google_cq_params(resolution))

    def run_experiment_on_cq_params(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        self.run_experiment_on_cq_params_one_pass(resolution, cq_params)
        self.run_experiment_on_cq_params_two_pass(resolution, cq_params)

    def run_experiment_on_cq_params_one_pass(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution One Pass: {resolution}'
              f'{str(cq_params)}')

        # One Pass
        CQGoogleExperimentBase.SubExperiment(self,
                                             cq_params=cq_params,
                                             output_width=resolution[0],
                                             output_height=resolution[1]).run_sub_experiment()

    def run_experiment_on_cq_params_two_pass(self, resolution: tuple[int, int], cq_params: CQExperiment.CQExperiment.SubExperiment.CQParams):
        print(f'{Util.HEADER}\nRunning Resolution Two Pass: {resolution}'
              f'{str(cq_params)}')

        # Two Pass
        CQGoogleExperimentBase.SubExperiment(self,
                                             cq_params=cq_params,
                                             output_width=resolution[0],
                                             output_height=resolution[1],
                                             two_pass_encoding=True).run_sub_experiment()

    def experiment_implementation(self):
        for resolution in self.get_scaled_down_all_resolutions():
            self.run_experiment_on_resolution(resolution)