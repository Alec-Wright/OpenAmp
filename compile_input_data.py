import soundfile as sf
import numpy as np
import argparse
from os.path import join
from glob import glob
import pandas as pd
import librosa
import matplotlib.pyplot as plt

def clip_check(x):
    x = x/np.max(np.abs(x))
    hist = np.histogram(x, bins=1000)
    #plt.plot(hist[0])
    #plt.show()
    maxxy = np.max(hist[0][5:-5])
    if np.max((hist[0][-5:],  hist[0][0:5])) > 0.5*maxxy:
        return True
    else:
        return False


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output_loc', type=str, default=join('Data', 'Ibanez2820-DI'),
                    help='save location for compiled input data')
parser.add_argument('-i', '--input_loc', type=str,
                    default=join('IDMT-SMT-GUITAR_V2', 'dataset4', 'Ibanez 2820'),
                    help='location to search for input wav files')
parser.add_argument('-cl', '--clip_detect', type=bool, default=True,
                    help='if true, detects clipping and removes samples with clipping')
parser.add_argument('-sd', '--seg_div', type=float, default=1.0)

args = parser.parse_args()

if __name__ == '__main__':

    files = glob(join(args.input_loc,'**', '*.wav'), recursive=True)

    audio_full = []
    for file in files:
        clip, fs = sf.read(file)

        try:
            clip_name = file.split('/')[-1].split('.')[0]
            onset = pd.read_csv(join(file.rsplit('/', maxsplit=2)[0], 'annotation', 'onsets', clip_name + '.csv'),
                               nrows=9, header=None)
            clip = clip[int(onset.iloc[-1, 0] * fs):]
            clip, _ = librosa.effects.trim(clip)

            num_seg = clip.shape[0] // int(args.seg_div * fs)
            clip = clip[:int(args.seg_div * fs)*num_seg]

            if args.clip_detect:
                if clip_check(clip):
                    print(f'clipping detected: {clip_name}')
                else:
                    audio_full.append(clip)
            else:
                audio_full.append(clip)
        except FileNotFoundError:
            print('no file for onsets found, skipping clip')

    audio_full = np.hstack(audio_full)
    sf.write(file=args.output_loc + '.wav', data=audio_full, samplerate=fs)






