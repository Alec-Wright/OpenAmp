import os
import torchaudio
from torch.utils.data import Dataset, DataLoader
import torch
from glob import glob
import pandas as pd
import time
from os.path import join
import Open_Amp.amp_model as amp_model


class OnlineGenerationDataset(Dataset):
    def __init__(self, devices, input, seg_len, lead_in):
        self.input_audio, self.sample_rate = torchaudio.load(input, channels_first=False)
        self.seg_len, self.lead_in = seg_len, lead_in
        self.seg_len_samps, self.lead_in_samps = int(self.seg_len*self.sample_rate), int(self.lead_in*self.sample_rate)
        self.tot_samp = self.seg_len_samps + self.lead_in_samps
        self.devices = devices

        models = []
        for each in devices.iterrows():
            name = each[1].model.split('-out')[0]
            mod = amp_model.AmpModel(model_file=each[1].path, amp_name=name)
            cond = mod.cond
            c_v = float(name.split('_cond-')[1]) if cond else None
            models.append((mod, cond, c_v))

        self.models = tuple(models)

        self.input_segs = (self.input_audio.shape[0] - self.lead_in_samps) // self.seg_len_samps
        self.num_models = len(self.models)
        self.num_segs = self.input_segs*self.num_models

    def __getitem__(self, index):
        with torch.inference_mode():
            audio_seg = index % self.input_segs
            model = index//self.input_segs

            input_audio = self.input_audio[audio_seg*self.seg_len_samps:(audio_seg+1)*self.seg_len_samps + self.lead_in_samps].unsqueeze(0)
            #if self.models[model][1]:
            #    cond = self.models[model][2]*torch.ones(input_audio.shape)
            #    input_audio = torch.cat((input_audio, cond), dim=2)

            c_v = self.models[model][2] if self.models[model][1] else None

            enc = torch.nn.functional.one_hot(torch.tensor(model, dtype=torch.long), self.num_models)
            output = self.models[model][0](input_audio, cond=c_v)

            return input_audio[0, :, 0:1].T, output[0, :, :].T, enc

    def get_model_name(self, mod_num):
        return self.models[mod_num].amp_name

    def get_model(self, mod_num):
        return self.models[mod_num][0:-1]

    def __len__(self):
        return self.num_segs


class LoadingDataset(Dataset):
    def __init__(self, devices, dataset_loc, seg_len, lead_in):
        input_audio, self.sample_rate = torchaudio.load(join(dataset_loc, 'input.wav'), channels_first=False)
        self.seg_len, self.lead_in = seg_len, lead_in
        self.seg_len_samps, self.lead_in_samps = int(self.seg_len*self.sample_rate), int(self.lead_in*self.sample_rate)
        self.tot_samp = self.seg_len_samps + self.lead_in_samps
        self.input_audio = input_audio.reshape(-1, self.tot_samp, 1)
        self.devices = devices
        self.dataset_loc = dataset_loc

        models = []
        for each in devices.iterrows():
            name = each[1].model.split('-out')[0]
            models.append({'name': name, 'id': each[0], 'model_path': each[1].path})

        self.models = tuple(models)

        self.input_segs = self.input_audio.shape[0]
        self.num_models = len(self.models)

    def __getitem__(self, index):
        model = self.models[index]

        try:
            target, fs = torchaudio.load(join(self.dataset_loc, self.models[index]['name']+'-out.wav'), channels_first=False)
            target = target.reshape(-1, self.tot_samp, 1)
            assert target.shape == self.input_audio.shape
        except:
            name = model['name']
            mod = amp_model.AmpModel(model['model_path'], amp_name=name)
            if mod.cond:
                name, cond = name.split('_cond-')
                c_v = float(cond)
            else:
                pass
            with torch.inference_mode():
                target = mod(self.input_audio, c_v if mod.cond else None)
            torchaudio.save(join(self.dataset_loc, self.models[index]['name']+'-out.wav'),
                            target.reshape(-1, 1), self.sample_rate, channels_first=False)

        enc = torch.nn.functional.one_hot(torch.tensor(model['id'], dtype=torch.long), self.num_models)

        return self.input_audio.permute(0, 2, 1), target.permute(0, 2, 1), enc.expand(self.input_audio.shape[0], -1)

    def get_model_name(self, mod_num):
        return self.models[mod_num]['name']

    def get_model(self, mod_num):
        return self.models[mod_num]

    def __len__(self):
        return self.num_models
