import json
import models
import torch, torchaudio


class AmpModel(torch.nn.Module):
    def __init__(self, model_file, amp_name):
        super().__init__()
        self.model, self.framework, self.model_class, self.cond = Get_Open_Amp_Model(model_file)
        self.amp_name = amp_name

    def forward(self, x, cond=None):
        if self.model_class == 'SimpleRNN':
            if self.cond:
                if cond is not None:
                    x = torch.cat([x, cond * torch.ones(x.shape)], dim=2)
                else:
                    x = torch.cat([x, 0.5 * torch.ones(x.shape)], dim=2)
            else:
                assert cond is None, "Conditioning specified for model with no conditioning parameter"

            out, _ = self.model(x)
            return out

def Get_Open_Amp_Model(filename):
    if filename.endswith('.json'):
        with open(filename, 'r') as f:
            json_data = json.load(f)
        framework, model_class = get_model_class(json_data)

        if framework == 'guitar-ml':
            model = guitar_ml_loader(json_data)
            return model, framework, model_class, True if model.rec.input_size > 1 else False
        elif framework == 'nam':
            raise NotImplementedError('Not implemented yet')
        else:
            raise NotImplementedError(f'unknown framework - {framework}')



    else:
        pass


def get_model_class(data):
    if 'model_data' in data.keys() and data['model_data']['model'] == 'SimpleRNN':
        return 'guitar-ml', 'SimpleRNN'

def guitar_ml_loader(data):
    if data['model_data']['model'] == 'SimpleRNN':
        return RNN_from_state_dict(data)
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

    model_no_gain = AmpModel('test/BlackstarHT40_AmpHighGain.json', 'BlackstarHT40')
    clip, fs = torchaudio.load('test/guitar-in.wav')
    out = model_no_gain(clip.unsqueeze(2))

    torchaudio.save('test/guitar-out.wav', out.squeeze(2).detach(), fs)

    model_gain = AmpModel('test/SLO_Crunch_GainKnob.json', 'SLO_Crunch')

    out = model_gain(clip.unsqueeze(2), 0)
    torchaudio.save('test/guitar-out_lowgain.wav', out.squeeze(2).detach(), fs)

    out = model_gain(clip.unsqueeze(2))
    torchaudio.save('test/guitar-out_midgain.wav', out.squeeze(2).detach(), fs)

    out = model_gain(clip.unsqueeze(2), 1)
    torchaudio.save('test/guitar-out_highgain.wav', out.squeeze(2).detach(), fs)
