import pandas as pd
from os.path import join
import numpy as np
from Open_Amp import amp_model
import torchaudio
import soundfile
import os
import torch


def get_dev_table(save_loc, model_list, save_name, cnd_res=5):
    dev_list = []
    dev_path = []

    for each in model_list:
        name = each.split('/')[-1].split('.')[0]
        model = amp_model.AmpModel(each, ' ')

        if model.cond:
            cond_vals = np.linspace(0, 1, cnd_res) if cnd_res else np.linspace(0.5, 0.5, 1)
            m = [f'{name}_cond-{n:.2f}-out.wav' for n in cond_vals]
            p = [each for n in cond_vals]
        else:
            m = [f'{name}-out.wav']
            p = [each]

        dev_list += m
        dev_path += p

    train_devs = pd.DataFrame({'model': dev_list, 'path': dev_path})
    train_devs.to_csv(join(save_loc, f'{save_name}.csv'))

    return train_devs


def init_dataset(dataset_name, devices, input_data, seg_len, lead_in, seg_starts):
    seg_total = seg_len + lead_in

    os.makedirs(dataset_name, exist_ok=True)

    try:
        x, fs = torchaudio.load(join(dataset_name, 'input.wav'), channels_first=False)
        x = x.reshape(-1, int(seg_total * fs), 1)
        print('Input data found')
    except soundfile.LibsndfileError:
        # Load clean guitar input file
        x, fs = torchaudio.load(input_data, channels_first=False)
        if seg_starts:
            clips = [x[int(n * fs):int((n + seg_total) * fs)] for n in seg_starts]
            x = torch.stack(clips, dim=0)
            print('Input data not found')
        print('Creating new input data')

        torchaudio.save(join(dataset_name, 'input.wav'), x.reshape(-1, 1), fs, channels_first=False)

    print(f'{dataset_name} dataset contains {x.numel()/(fs*60)} minutes of input guitar audio')

    """for dev, path in tqdm(zip(devices.model, devices.path), total=len(devices.model)):
        name = dev.split('/')[-1].rsplit('-out', maxsplit=1)[0]
        if '_cond-' in name:
            name, cond = name.split('_cond-')
            c_v = float(cond)
        else:
            pass

        mod = amp_model.AmpModel(path, amp_name=name)
        cond = mod.cond

        if os.path.isfile(join(dataset_name, dev)):
            y, fs = torchaudio.load(join(dataset_name, dev))
            assert y.reshape(-1, int(seg_total * fs), 1).shape == x.shape
        else:
            with torch.inference_mode():
                y = mod(x, c_v if cond else None)
            torchaudio.save(join(dataset_name, dev), y.reshape(-1, 1), fs, channels_first=False)"""