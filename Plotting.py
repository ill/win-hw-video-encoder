import plotBytesVsVMAF

def highGraphs():
    # Define your settings using the classes
    file_structs = [
        plotBytesVsVMAF.FileSettings(
            csv_file='Out/CRF/sonichd/sonichd-CRF.csv',
            dims={
                (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(0, 54))
            },
            label='SonicHD',
            show_crf=True,
        ),
        # plotBytesVsVMAF.FileSettings(
        #     csv_file='Out/CRF/badminton/badminton-CRF.csv',
        #     dims={
        #         (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='badminton',
        #     show_crf=True,
        # ),
        # plotBytesVsVMAF.FileSettings(
        #     csv_file='Out/CRF/1440p-av1-42sec/1440p-av1-42sec-CRF.csv',
        #     dims={
        #         (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='1440p-av1-42sec',
        #     show_crf=True,
        # ),
        # plotBytesVsVMAF.FileSettings(
        #     csv_file='Out/CRF/steal-a-brainrot/steal-a-brainrot-CRF.csv',
        #     dims={
        #         (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(0, 54)),
        #         (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='steal-a-brainrot',
        #     show_crf=True,
        # ),
        # plotBytesVsVMAF.FileSettings(
        #     csv_file='Out/CQGoogleGSunExperiment/bipbop15_270_mono/bipbop15_270_mono-CQGoogleGSunExperiment.csv',
        #     dims={
        #         (480, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (160, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #     },
        #     label='bipbop15_270_mono',
        #     show_gsun=True,
        #     show_crf=True,
        # ),

        plotBytesVsVMAF.FileSettings(
            csv_file='Out/CQGoogleGSunExperiment/sonichd/sonichd-CQGoogleGSunExperiment.csv',
            dims={
                (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
                # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
                # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
                # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
            },
            label='SonicHD-Gsun',
            show_gsun=True,
            show_crf=False,
        ),

        # plotBytesVsVMAF.FileSettings(
        #     csv_file='Out/CQGoogleGSunExperiment/1440p-av1-42sec/1440p-av1-42sec-CQGoogleGSunExperiment.csv',
        #     dims={
        #         (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
        #     },
        #     label='1440p-av1-42sec-Gsun',
        #     show_gsun=True,
        #     show_crf=False,
        # ),

        # plotBytesVsVMAF.FileSettings(
        #     csv_file='Out/CQGoogleGSunExperiment/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CQGoogleGSunExperiment.csv',
        #     dims={
        #         (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
        #     },
        #     label='Halo_NoMotion_20sec_1080p-Gsun',
        #     show_gsun=True,
        # ),
    ]

    plotBytesVsVMAF.plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

def lowMotionGraphs():
    # Define your settings using the classes
    file_structs = [
        plotBytesVsVMAF.FileSettings(
            csv_file='Out--Latest/CRF-Backup/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CRF.csv',
            dims={
                (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(8, 42))
            },
            label='Halo_NoMotion_20sec_1080p'
        )
    ]

    plotBytesVsVMAF.plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        output_filename='combined_low_motion_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

def highGraphs_gsun():
    # Define your settings using the classes
    file_structs = [
        plotBytesVsVMAF.FileSettings(
            csv_file='Out/CQGoogleGSunExperiment/bipbop15_270_mono/bipbop15_270_mono-CQGoogleGSunExperiment.csv',
            dims={
                (480, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (160, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
            },
            label='bipbop15_270_mono'
        ),
        # FileSettings(
        #     csv_file='Out/CRF/badminton/badminton-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='badminton'
        # ),
        # FileSettings(
        #     csv_file='Out/CRF/1440p-av1-42sec/1440p-av1-42sec-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='1440p-av1-42sec'
        # ),
        # FileSettings(
        #     csv_file='Out/CRF/steal-a-brainrot/steal-a-brainrot-CRF.csv',
        #     dims={
        #         (1920, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (1280, -1): DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        #         (960, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54)),
        #         (640, -1): DimensionSettings(enable_1pass=False, crf_range=(0, 54))
        #     },
        #     label='steal-a-brainrot'
        # ),
    ]

    plotBytesVsVMAF.plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

if __name__ == "__main__":
    highGraphs()

    #lowMotionGraphs()

    #sonichdGraphs()