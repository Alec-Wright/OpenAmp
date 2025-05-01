import copy
import json
import os
from Open_Amp import models
import torch, torchaudio
from nam.models.wavenet import WaveNet
from typing import Dict
import numpy as np
from tqdm import tqdm


class AmpModel(torch.nn.Module):
    def __init__(self, model_file, amp_name, new_cfg=None):
        super().__init__()
        if new_cfg is None:
            self.model, self.framework, self.model_class, self.cond = Get_Open_Amp_Model(model_file)
        else:
            self.model_class = new_cfg['architecture']
            if self.model_class == 'SimpleRNN':
                self.model = models.RNN(**new_cfg['config'])
                self.framework = 'guitar-ml'
            elif self.model_class == 'WaveNet':
                self.model = WaveNet(new_cfg['config']['layers'],
                                     new_cfg['config']['head'],
                                     new_cfg['config']['head_scale'], sample_rate=44100)
                self.framework = 'nam'
            else:
                NotImplementedError('Unknown model class')
            self.cond = False


        self.amp_name = amp_name

    def export(self, dir, name=None, to_append=None):
        if name is None:
            name = self.amp_name

        if to_append is not None:
            name += to_append

        if self.framework == 'guitar-ml':

            filename = os.path.join(dir, name + '.json')
            state_dict = self.model.state_dict()
            for k, v in state_dict.items():
                state_dict[k] = v.cpu().numpy().tolist()

            state_dict['lin.bias'] = state_dict.pop('linear.bias')
            state_dict['lin.weight'] = state_dict.pop('linear.weight')

            json_dict = {"model_data": {"model": "SimpleRNN",
                                        "input_size": self.model.rec.input_size,
                                        "skip": 1,
                                        "output_size": 1,
                                        "unit_type": "LSTM",
                                        "num_layers": 1,
                                        "hidden_size": self.model.rec.hidden_size,
                                        "bias_fl": True},
                         "state_dict": state_dict}


            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json_dict, f, ensure_ascii=False, indent=2)

        elif self.framework == 'nam':
            model_float32 = copy.deepcopy(self.model)
            model_float32 = model_float32.to(torch.float)
            model_float32.export(outdir=dir, basename=name)
            del model_float32
        return

    def forward(self, x, cond=None):
        '''

        :param x: dims (batch, time, channels)
        :param cond: scalar
        :return:
        '''
        if self.model_class == 'SimpleRNN':
            if self.cond:
                if cond is not None:
                    x = torch.cat([x, cond * torch.ones(x.shape)], dim=2)
                else:
                    x = torch.cat([x, 0.5 * torch.ones(x.shape)], dim=2)
            else:
                assert cond is None, "Conditioning specified for model with no conditioning parameter"

            out, _ = self.model(x)
        elif self.model_class == 'WaveNet':
            if x.ndim == 3:
                x = x.squeeze()
            if x.shape[-1] < x.shape[0]:
                x = x.permute(1, 0)

            out = self.model(x).squeeze().unsqueeze(-1)
        else:
            if x.ndim == 3:
                x = x.squeeze()
            out = self.model(x).squeeze().unsqueeze(-1)

        return out

    def forward_frames(self, x, frame_size, warmup=None):
        if x.ndim == 3:
            x = x.squeeze()
        if x.shape[-1] < x.shape[0]:
            x = x.permute(1, 0)
        num_samples = x.shape[-1]
        num_frames = int(np.floor(num_samples / frame_size))
        y = []

        if self.model_class == 'SimpleRNN':
            for n in tqdm(range(num_frames)):
                start = frame_size * n
                end = frame_size * (n + 1)
                y.append(self.forward(x[:, start:end].unsqueeze(-1)).squeeze(-1))

        elif self.model_class == 'WaveNet':
            if warmup is None:
                warmup = frame_size
            x = torch.concatenate((torch.zeros(1, warmup), x), dim=-1)
            for n in tqdm(range(num_frames)):
                x_frame = x[:, n*frame_size:(n+1)*frame_size+warmup]
                y_frame = self.forward(x_frame).detach()
                y.append(y_frame[-frame_size:].T)

        y = torch.cat(y, dim=-1)
        return y

def Get_Open_Amp_Model(filename):
    if filename.endswith('.json') or filename.endswith('.nam'):
        with open(filename, 'r') as f:
            json_data = json.load(f)
        framework, model_class = get_model_class(json_data)

        if framework == 'guitar-ml':
            model = guitar_ml_loader(json_data)
            return model, framework, model_class, True if model.rec.input_size > 1 else False
        elif framework == 'nam':
            model = nam_loader(json_data)
            return model, framework, model_class, False     # TODO: update for conditioned models
        else:
            raise NotImplementedError(f'unknown framework - {framework}')



    else:
        pass


def get_model_class(data):
    if 'model_data' in data.keys() and data['model_data']['model'] == 'SimpleRNN':
        return 'guitar-ml', 'SimpleRNN'
    elif 'config' in data.keys() and data['architecture'] == 'WaveNet':
        return 'nam', 'WaveNet'
    else:
        raise NotImplementedError('Not implemented yet')

def guitar_ml_loader(data):
    if data['model_data']['model'] == 'SimpleRNN':
        return RNN_from_state_dict(data)
    else:
        raise NotImplementedError('Not implemented yet')


def nam_loader(data):
    if data['architecture'] == 'WaveNet':

        if 'sample_rate' in data:
            fs = data['sample_rate']
        else:
            fs = 48000

        model = WaveNet(data['config']['layers'],
                        data['config']['head'],
                        data['config']['head_scale'], sample_rate=fs)
        model.import_weights(data['weights'])
        return model
    else:
        raise NotImplementedError('Not implemented yet')


def RNN_from_state_dict(json_data: dict):

    model_data = json_data["model_data"]

    model = models.RNN(cell_type=model_data["unit_type"],
                       in_channels=model_data["input_size"],
                       out_channels=model_data["output_size"],
                       hidden_size=model_data["hidden_size"],
                       residual_connection=bool(model_data["skip"]))

    state_dict = {}
    for key, value in json_data["state_dict"].items():
        state_dict[key.replace("lin", "linear")] = torch.tensor(value)

    model.load_state_dict(state_dict)
    return model


if __name__ == "__main__":

    clip, fs = torchaudio.load('test/guitar-in.wav')

    model_no_gain = AmpModel('test/BlackstarHT40_AmpHighGain.json', 'BlackstarHT40')
    out = model_no_gain(clip.unsqueeze(2))
    torchaudio.save('test/guitar-out.wav', out.squeeze(2).detach(), fs)

    model_nam = AmpModel('../NAM/Vox AC15/Vox AC15CH Crystal Clean TB.nam', 'Vox AC15')
    out = model_nam(clip.unsqueeze(2))
    torchaudio.save('test/guitar-out.wav', out.T.detach(), fs)

    model_gain = AmpModel('test/SLO_Crunch_GainKnob.json', 'SLO_Crunch')

    out = model_gain(clip.unsqueeze(2), 0)
    torchaudio.save('test/guitar-out_lowgain.wav', out.squeeze(2).detach(), fs)

    out = model_gain(clip.unsqueeze(2))
    torchaudio.save('test/guitar-out_midgain.wav', out.squeeze(2).detach(), fs)

    out = model_gain(clip.unsqueeze(2), 1)
    torchaudio.save('test/guitar-out_highgain.wav', out.squeeze(2).detach(), fs)
