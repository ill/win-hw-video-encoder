import Experiment
import Util


class CRFExperiment(Experiment.Experiment):
    def __init__(self, input_video_file_name, output_video_file_basename):
        super().__init__('CRF', input_video_file_name, output_video_file_basename)

    def get_extra_csv_header_columns(self):
        return ['crf']
    
    def experiment_implementation(self):
        # CRFExperiment.SubExperiment(self,
        #                             crf=0).run_sub_experiment()

        CRFExperiment.SubExperiment(self,
                                    crf=0,
                                    output_width=1920,
                                    output_height=888).run_sub_experiment()

        # for resolution in self.get_scaled_down_all_resolutions():
        #     for crf in Util.inclusive_range(0, 63, 3):
        #         CRFExperiment.SubExperiment(self,
        #                                     crf=crf,
        #                                     output_width=resolution[0],
        #                                     output_height=resolution[1]).run_sub_experiment()
        #
        #         CRFExperiment.SubExperiment(self,
        #                                     crf=crf,
        #                                     output_width=resolution[0],
        #                                     output_height=resolution[1],
        #                                     two_pass_encoding=True).run_sub_experiment()

    class SubExperiment(Experiment.Experiment.SubExperiment):
        def __init__(self,
                     experiment,
                     crf: int = 32,
                     output_width: int = -1,
                     output_height: int = -1,
                     output_fps: int = -1,
                     two_pass_encoding: bool = False):
            super().__init__(experiment,
                             f'crf-{crf}'
                             f'-w-{output_width}'
                             f'-h-{output_height}'
                             f'-fps-{output_fps}'
                             f'-{"2Pass" if two_pass_encoding else "1Pass"}',
                             output_width=output_width,
                             output_height=output_height,
                             output_fps=output_fps,
                             two_pass_encoding=two_pass_encoding)
            self.crf = crf

        def get_extra_ffmpeg_parameters(self):
            return [
                '-crf', str(self.crf),
                '-speed', '0',
                '-quality', 'good',
                '-threads', '16',
                '-tile-columns', str(Util.get_tile_columns(self.output_width))
            ]
        
        def get_extra_csv_columns(self):
            return [
                str(self.crf)
            ]