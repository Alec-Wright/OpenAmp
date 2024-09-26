from os.path import join
from glob import glob
from Utils import models

def main(config_set, db_path):

    d = {'devices': glob('Proteus_Tone_Packs/*/*.json'),
         'cond_res': 5,
         'train_data': {'input': join(db_path, 'Data', 'CareerSG-DI.wav'),
                        'seg_len': 1.0, 'lead_in': 0.5},

         'val_data': {'dataset_name': join(db_path, 'Data', 'val'),
                      'input_data': join(db_path, 'Data', 'Ibanez2820-DI.wav'),
                      'seg_len': 3, 'lead_in': 0.5,
                      'seg_starts': (0, 12, 24, 36, 48, 63, 72, 84, 96, 108, 120, 132),
                      'overwrite': False},

         'test_data': {'dataset_name': join(db_path, 'Data', 'test'),
                       'input_data': join(db_path, 'Data', 'Ibanez2820-DI.wav'),
                       'seg_len': 3, 'lead_in': 0.5,
                       'seg_starts': (0, 12, 24, 36, 48, 63, 72, 84, 96, 108, 120, 132),
                       'overwrite': False}}

    if config_set == 0:
        d['t_bs'] = 4,
        d['v_bs'] = 4,
        d['TCN'] = {'layer_class': models.GatedTCNLayerFilmConditioned,
                    'channels': 8,
                    'blocks': 2,
                    'layers': 2,
                    'dilation_growth': 2,
                    'kernel_size': 3,
                    'cond_pars': 32,
                    'emb_dim': 32}

    elif config_set == 1:
        d['t_bs'] = 16,
        d['v_bs'] = 12,
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