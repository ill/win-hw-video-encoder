import argparse
import subprocess
import SpeedExperiment
import CRFExperiment
import QualityExperiment
import CQGoogleExperiment

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
    #CRFExperiment.CRFExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    #QualityExperiment.QualityExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()

    #CRFExperiment.CRFExperiment('sonichd.mp4', 'sonichd').run_experiment()

    #CRFExperiment.CRFExperiment('zootopia12.mp4', 'zootopia12').run_experiment()

    #CRFExperiment.CRFExperiment('bipbop15_270_mono.mp4', 'bipbop15_270_mono').run_experiment()

    CQGoogleExperiment.CQGoogleExperiment('1440p-av1-42sec.mp4', '1440p-av1-42sec').run_experiment()
    CQGoogleExperiment.CQGoogleExperiment('sonichd.mp4', 'sonichd').run_experiment()

    print('Done.')

if __name__ == '__main__':
    main()
