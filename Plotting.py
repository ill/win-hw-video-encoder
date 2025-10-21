import plotBytesVsVMAF

#########
# region CRF

_1440p_av1_42sec_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/1440p-av1-42sec/1440p-av1-42sec-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
    },
    label='1440p-av1-42sec',
    show_crf=True,
))

badminton_CRF = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CRF/badminton/badminton-CRF.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
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
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54)),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(3, 54))
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

# endregion

#########
# region CQGoogleGSun

_1440p_av1_42sec_CQGoogleGSun = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGoogleGSunExperiment/1440p-av1-42sec/1440p-av1-42sec-CQGoogleGSunExperiment.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
    },
    label='1440p-av1-42sec-Gsun',
    show_gsun=True,
))

badminton_CQGoogleGSun = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGoogleGSunExperiment/badminton/badminton-CQGoogleGSunExperiment.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
    },
    label='badminton-Gsun',
    show_gsun=True,
))

bipbop_15_270_mono_CQGoogleGSun = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGoogleGSunExperiment/bipbop15_270_mono/bipbop15_270_mono-CQGoogleGSunExperiment.csv',
    dims={
        (480, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (160, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
    },
    label='bipbop15_270_mono-Gsun',
    show_gsun=True,
))

Halo_NoMotion_20sec_1080p_CQGoogleGSun = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGoogleGSunExperiment/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CQGoogleGSunExperiment.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #(1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #(960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #(640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
    },
    label='Halo_NoMotion_20sec_1080p-Gsun',
    show_gsun=True,
))

sonichd_CQGoogleGSun = (
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
))

# endregion

#########
# region CQGSunBruteForceSweep

_1440p_av1_42sec_0CRF_GSUN = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGSunBruteForceSweep/1440p-av1-42sec/1440p-av1-42sec-CQGSunBruteForceSweep.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
    },
    label='1440p-av1-42sec-0CRF-Gsun',
    show_gsun=True,
))

badminton_0CRF_GSUN = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGSunBruteForceSweep/badminton/badminton-CQGSunBruteForceSweep.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
    },
    label='badminton-0CRF-Gsun',
    show_gsun=True,
))

bipbop_15_270_mono_0CRF_GSUN = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGSunBruteForceSweep/bipbop15_270_mono/bipbop15_270_mono-CQGSunBruteForceSweep.csv',
    dims={
        (480, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
        (160, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False, crf_range=(10, 63)),
    },
    label='bipbop15_270_mono-0CRF-Gsun',
    show_gsun=True,
))

Halo_NoMotion_20sec_1080p_0CRF_GSUN = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGSunBruteForceSweep/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CQGSunBruteForceSweep.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #(1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #(960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        #(640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
    },
    label='Halo_NoMotion_20sec_1080p-0CRF-Gsun',
    show_gsun=True,
))

sonichd_0CRF_GSUN = (
plotBytesVsVMAF.FileSettings(
    csv_file='Out/CQGSunBruteForceSweep/sonichd/sonichd-CQGSunBruteForceSweep.csv',
    dims={
        (1920, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (1280, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (960, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False),
        # (640, -1): plotBytesVsVMAF.DimensionSettings(enable_1pass=False)
    },
    label='SonicHD-0CRF-Gsun',
    show_gsun=True,
))

# endregion

#########
# region CQGoogle

_1440p_av1_42sec_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/1440p-av1-42sec/1440p-av1-42sec-CQGoogle.csv',
    label='1440p-av1-42sec-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

badminton_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/badminton/badminton-CQGoogle.csv',
    label='badminton-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

bipbop15_270_mono_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/bipbop15_270_mono/bipbop15_270_mono-CQGoogle.csv',
    label='bipbop15_270_mono-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

Halo_Montage_1080p_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/Halo_Montage_1080p/Halo_Montage_1080p-CQGoogle.csv',
    label='Halo_Montage_1080p-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

Halo_NoMotion_20sec_1080p_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/Halo_NoMotion_20sec_1080p/Halo_NoMotion_20sec_1080p-CQGoogle.csv',
    label='Halo_NoMotion_20sec_1080p-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

ios_native_recorder_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/ios_native_recorder/ios_native_recorder-CQGoogle.csv',
    label='ios_native_recorder-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

sonichd_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/sonichd/sonichd-CQGoogle.csv',
    label='SonicHD-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

steal_a_brainrot_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/steal-a-brainrot/steal-a-brainrot-CQGoogle.csv',
    label='steal-a-brainrot-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

strongest_battlegrounds_mac_1440_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/strongest-battlegrounds-mac-1440/strongest-battlegrounds-mac-1440-CQGoogle.csv',
    label='strongest-battlegrounds-mac-1440-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

TinyWheelsiPad1920x1440x60xHEVCScreenRecording_CQGoogle = (
plotBytesVsVMAF.FileSettingsByResolution(
    csv_file='Out/CQGoogle/TinyWheelsiPad1920x1440x60xHEVCScreenRecording/TinyWheelsiPad1920x1440x60xHEVCScreenRecording-CQGoogle.csv',
    label='TinyWheelsiPad1920x1440x60xHEVCScreenRecording-CQGoogle',
    enable_1pass=False,
    enable_2pass=True,
))

# endregion

def graphsCombo():
    # Define your settings using the classes
    file_structs = [
        #########
        # region CRF

        #_1440p_av1_42sec_CRF,
        #badminton_CRF,
        #bipbop_15_270_mono_CRF,
        #Halo_Montage_1080p_CRF,
        #Halo_NoMotion_20sec_1080p_CRF,
        #ios_native_recorder_CRF,
        sonichd_CRF,
        #steal_a_brainrot_CRF,
        #strongest_battlegrounds_mac_1440_CRF,

        # endregion

        #########
        # region CQGoogleGSun

        #_1440p_av1_42sec_CQGoogleGSun,
        #badminton_CQGoogleGSun,
        #bipbop_15_270_mono_CQGoogleGSun,
        #Halo_NoMotion_20sec_1080p_CQGoogleGSun,
        sonichd_CQGoogleGSun,

        # endregion

        #########
        # region CQGSunBruteForceSweep

        #_1440p_av1_42sec_0CRF_GSUN,
        #badminton_0CRF_GSUN,
        #bipbop_15_270_mono_0CRF_GSUN,
        #Halo_NoMotion_20sec_1080p_0CRF_GSUN,
        sonichd_0CRF_GSUN,

        # endregion
    ]

    file_structs_by_res = [
        #########
        # region CQGoogle

        #_1440p_av1_42sec_CQGoogle,
        #badminton_CQGoogle,
        #bipbop15_270_mono_CQGoogle,
        #Halo_Montage_1080p_CQGoogle,
        #Halo_NoMotion_20sec_1080p_CQGoogle,
        #ios_native_recorder_CQGoogle,
        sonichd_CQGoogle,
        #steal_a_brainrot_CQGoogle,
        #strongest_battlegrounds_mac_1440_CQGoogle,
        #TinyWheelsiPad1920x1440x60xHEVCScreenRecording_CQGoogle,

        # endregion
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
