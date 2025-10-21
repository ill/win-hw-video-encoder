import argparse
import subprocess
import SpeedExperiment
import CRFExperiment
import QualityExperiment
import CQGoogleExperiment
import CQGoogleExperimentBruteForceSweep
import CQGSunBruteForceSweep
import CQGoogleGSunExperiment

def parse_args():
    parser = argparse.ArgumentParser(description="Video transcode automation script.")
    parser.add_argument('--sso', type=bool, default=False, help='Use AWS SSO to login before uploading to S3')
    return parser.parse_args()

def main():
    args = parse_args()

    if (args.sso):
        aws_sso_cmd = ['aws', 'sso', 'login', '--profile', 'test-audiovisual']
        result = subprocess.run(aws_sso_cmd)
        if result.returncode != 0:
            print('AWS SSO login failed. Will use existing AWS tokens in the environment.')
        
    #SpeedExperiment.SpeedExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    #QualityExperiment.QualityExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()

    #CRFExperiment.CRFExperiment('zootopia12.mp4', 'zootopia12').run_experiment()

    # CRFExperiment.CRFExperiment('bipbop15_270_mono.mp4', 'bipbop15_270_mono').run_experiment()
    # CRFExperiment.CRFExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    # CRFExperiment.CRFExperiment('sonichd.mp4', 'sonichd').run_experiment()
    # CRFExperiment.CRFExperiment('badminton.mp4', 'badminton').run_experiment()
    #CRFExperiment.CRFExperiment('ios_native_recorder.mp4', 'ios_native_recorder').run_experiment()
    # CRFExperiment.CRFExperiment('steal-a-brainrot.mp4', 'steal-a-brainrot').run_experiment()
    # CRFExperiment.CRFExperiment('Halo_NoMotion_20sec_1080p.mp4', 'Halo_NoMotion_20sec_1080p').run_experiment()
    # CRFExperiment.CRFExperiment('Halo_Montage_1080p.mp4', 'Halo_Montage_1080p').run_experiment()
    #CRFExperiment.CRFExperiment('strongest-battlegrounds-mac-1440.mov', 'strongest-battlegrounds-mac-1440').run_experiment()
    #CRFExperiment.CRFExperiment('TinyWheelsiPad1920x1440x60xHEVCScreenRecording.mp4', 'TinyWheelsiPad1920x1440x60xHEVCScreenRecording').run_experiment()

    # CQGoogleExperiment.CQGoogleExperiment('bipbop15_270_mono.mp4', 'bipbop15_270_mono').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('sonichd.mp4', 'sonichd').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('badminton.mp4', 'badminton').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('ios_native_recorder.mp4', 'ios_native_recorder').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('steal-a-brainrot.mp4', 'steal-a-brainrot').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('Halo_NoMotion_20sec_1080p.mp4', 'Halo_NoMotion_20sec_1080p').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('Halo_Montage_1080p.mp4', 'Halo_Montage_1080p').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('strongest-battlegrounds-mac-1440.mov', 'strongest-battlegrounds-mac-1440').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('TinyWheelsiPad1920x1440x60xHEVCScreenRecording.mp4', 'TinyWheelsiPad1920x1440x60xHEVCScreenRecording').run_experiment()

    # CQGoogleExperiment.CQGoogleExperiment('bipbop15_270_mono.mp4', 'bipbop15_270_mono').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    # CQGoogleExperiment.CQGoogleExperiment('sonichd.mp4', 'sonichd').run_experiment()

    #CQGoogleExperimentBruteForceSweep.CQGoogleExperimentBruteForceSweep('bipbop15_270_mono.mp4', 'bipbop15_270_mono').run_experiment()

    # CQGSunBruteForceSweep.CQGSunBruteForceSweep('bipbop15_270_mono.mp4', 'bipbop15_270_mono').run_experiment()
    # CQGSunBruteForceSweep.CQGSunBruteForceSweep('Halo_NoMotion_20sec_1080p.mp4', 'Halo_NoMotion_20sec_1080p').run_experiment()
    # CQGSunBruteForceSweep.CQGSunBruteForceSweep('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    # CQGSunBruteForceSweep.CQGSunBruteForceSweep('sonichd.mp4', 'sonichd').run_experiment()
    # CQGSunBruteForceSweep.CQGSunBruteForceSweep('badminton.mp4', 'badminton').run_experiment()

    #CQGoogleGSunExperiment.CQGoogleGSunExperiment('bipbop15_270_mono.mp4', 'bipbop15_270_mono').run_experiment()
    #CQGoogleGSunExperiment.CQGoogleGSunExperiment('sonichd.mp4', 'sonichd').run_experiment()
    CQGoogleGSunExperiment.CQGoogleGSunExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    CQGoogleGSunExperiment.CQGoogleGSunExperiment('badminton.mp4', 'badminton').run_experiment()
    CQGoogleGSunExperiment.CQGoogleGSunExperiment('steal-a-brainrot.mp4', 'steal-a-brainrot').run_experiment()
    CQGoogleGSunExperiment.CQGoogleGSunExperiment('Halo_Montage_1080p.mp4', 'Halo_Montage_1080p').run_experiment()
    CQGoogleGSunExperiment.CQGoogleGSunExperiment('Halo_NoMotion_20sec_1080p.mp4', 'Halo_NoMotion_20sec_1080p').run_experiment()
    CQGoogleGSunExperiment.CQGoogleGSunExperiment('strongest-battlegrounds-mac-1440.mov', 'strongest-battlegrounds-mac-1440').run_experiment()
    CQGoogleGSunExperiment.CQGoogleGSunExperiment('TinyWheelsiPad1920x1440x60xHEVCScreenRecording.mp4', 'TinyWheelsiPad1920x1440x60xHEVCScreenRecording').run_experiment()

    print('Done.')

if __name__ == '__main__':
    main()
