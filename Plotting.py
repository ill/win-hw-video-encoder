import plotBytesVsVMAF

#########
# CRF

_1440p_av1_42sec_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/1440p-av1-42sec/1440p-av1-42sec-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='1440p-av1-42sec',
    show_crf=True,
))

badminton_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/badminton/badminton-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='badminton',
    show_crf=True,
))

bipbop_15_270_mono_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGoogleGSunExperiment/bipbop15_270_mono/bipbop15_270_mono-CQGoogleGSunExperiment.csv',
    dims={
        (480, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (160, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
    },
    label='bipbop15_270_mono',
    show_gsun=True,
    show_crf=True,
))

Halo_Montage_1080p_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/Halo_Montage_1080p/Halo_Montage_1080p-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='Halo_Montage_1080p-CRF',
    show_crf=True,
))

Halo_NoMotion_20sec_1080p_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='Halo_NoMotion_20sec_1080p-CRF',
    show_crf=True,
))

ios_native_recorder_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/ios_native_recorder/ios_native_recorder-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='ios_native_recorder-CRF',
    show_crf=True,
))

sonichd_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/sonichd/sonichd-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='SonicHD',
    show_crf=True,
))

steal_a_brainrot_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/steal-a-brainrot/steal-a-brainrot-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='steal-a-brainrot',
    show_crf=True,
))

strongest_battlegrounds_mac_1440_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/strongest-battlegrounds-mac-1440/strongest-battlegrounds-mac-1440-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='strongest-battlegrounds-mac-1440',
    show_crf=True,
))

#########
# CQGSunBruteForceSweep

#########
# CQGoogleGSun

#########
# CQGoogle

def graphsCombo():
    # Define your settings using the classes
    file_structs = [
        #_1440p_av1_42sec_CRF,
        badminton_CRF,
        # bipbop_15_270_mono_CRF,
        # Halo_Montage_1080p_CRF,
        # Halo_NoMotion_20sec_1080p_CRF,
        # ios_native_recorder_CRF,
        # sonichd_CRF,
        # steal_a_brainrot_CRF,
        # strongest_battlegrounds_mac_1440_CRF,








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

        # plotBytesVsVMAF.FileSettings(
        #     csv_file='Out/CQGoogleGSunExperiment/sonichd/sonichd-CQGoogleGSunExperiment.csv',
        #     dims={
        #         (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #         (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
        #     },
        #     label='SonicHD-Gsun',
        #     show_gsun=True,
        #     show_crf=False,
        # ),

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

    file_structs_by_res = [
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/sonichd/sonichd-CQGoogle.csv',
        #     label='SonicHD-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),

        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/1440p-av1-42sec/1440p-av1-42sec-CQGoogle.csv',
        #     label='1440p-av1-42sec-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/badminton/badminton-CQGoogle.csv',
        #     label='badminton-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/bipbop15_270_mono/bipbop15_270_mono-CQGoogle.csv',
        #     label='bipbop15_270_mono-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/Halo_Montage_1080p/Halo_Montage_1080p-CQGoogle.csv',
        #     label='Halo_Montage_1080p-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CQGoogle.csv',
        #     label='Halo_NoMotion_20sec_1080p-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/ios_native_recorder/ios_native_recorder-CQGoogle.csv',
        #     label='ios_native_recorder-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/steal-a-brainrot/steal-a-brainrot-CQGoogle.csv',
        #     label='steal-a-brainrot-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/strongest-battlegrounds-mac-1440/strongest-battlegrounds-mac-1440-CQGoogle.csv',
        #     label='strongest-battlegrounds-mac-1440-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
        #
        # plotBytesVsVMAF.FileSettingsByResolution(
        #     csv_file='Out/CQGoogle/TinyWheelsiPad1920x1440x60xHEVCScreenRecording/TinyWheelsiPad1920x1440x60xHEVCScreenRecording-CQGoogle.csv',
        #     label='TinyWheelsiPad1920x1440x60xHEVCScreenRecording-Google',
        #     enable_1pass=True,
        #     enable_2pass=False,
        # ),
    ]

    plotBytesVsVMAF.plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        file_settings_by_resolution_list=file_structs_by_res,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

def sonichd():
    file_structs = [
        plotBytesVsVMAF.FileSettings(
            csv_file='Out/CRF/sonichd/sonichd-CRF.csv',
            dims={
                (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(27, 63)),
                (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63))
            },
            label='SonicHD',
            show_crf=True,
        ),

        plotBytesVsVMAF.FileSettings(
            csv_file='Out/CQGoogleGSunExperiment/sonichd/sonichd-CQGoogleGSunExperiment.csv',
            dims={
                (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
                (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
                (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
                (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
            },
            label='SonicHD-Gsun',
            show_gsun=True,
            show_crf=False,
        ),
    ]

    file_structs_by_res = [
        plotBytesVsVMAF.FileSettingsByResolution(
            csv_file='Out/CQGoogle/sonichd/sonichd-CQGoogle.csv',
            label='SonicHD-Google',
            enable_1pass=True,
            enable_2pass=False,
        ),
    ]

    plotBytesVsVMAF.plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        file_settings_by_resolution_list=file_structs_by_res,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

def badminton():
    file_structs = [
        plotBytesVsVMAF.FileSettings(
            csv_file='Out/CRF/badminton/badminton-CRF.csv',
            dims={
                (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
                (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(0, 54))
            },
            label='badminton',
            show_crf=True,
        ),
    ]

    file_structs_by_res = [
        plotBytesVsVMAF.FileSettingsByResolution(
            csv_file='Out/CQGoogle/badminton/badminton-CQGoogle.csv',
            label='badminton-Google',
            enable_1pass=True,
            enable_2pass=False,
        ),
    ]

    plotBytesVsVMAF.plot_combined_bd_class_dim(
        file_settings_list=file_structs,
        file_settings_by_resolution_list=file_structs_by_res,
        output_filename='combined_bd_graph.png',
        show_plot=True,
        use_leader_lines=False,
    )

if __name__ == "__main__":
    graphsCombo()

    #sonichd()

    #badminton()