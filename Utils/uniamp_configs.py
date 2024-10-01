from os.path import join
from glob import glob
from Utils import uniamp_models as models


def main(config_set):

    d = {'devices': glob('Proteus_Tone_Packs/*/*.json'),
         'cond_res': 5,
         'train_data': {'input': join('Data', 'CareerSG-DI.wav'),
                        'seg_len': 1.0, 'lead_in': 0.5},

         'val_data': {'dataset_name': join('Data', 'val'),
                      'input_data': join('Data', 'Ibanez2820-DI.wav'),
                      'seg_len': 3, 'lead_in': 0.5,
                      'seg_starts': (0, 22, 94, 144, 243, (8*60)+41, (11*60)+16, (18*60) + 48, (19*60)+43, (23*60)+54)
                      }
         }

    if config_set == 0:
        d['t_bs'] = 4
        d['v_bs'] = 4
        d['TCN'] = {'layer_class': models.GatedTCNLayerFilmConditioned,
                    'channels': 8,
                    'blocks': 2,
                    'layers': 2,
                    'dilation_growth': 2,
                    'kernel_size': 3,
                    'cond_pars': 32,
                    'emb_dim': 32}

    elif config_set == 1:
        d['t_bs'] = 16
        d['v_bs'] = 12
        d['TCN'] = {'layer_class': models.GatedTCNLayerFilmConditioned,
                    'channels': 16,
                    'blocks': 2,
                    'layers': 8,
                    'dilation_growth': 2,
                    'kernel_size': 3,
                    'cond_pars': 64,
                    'emb_dim': 64}
    else:
        print('invalid config set')

    return d
