from os.path import join
from glob import glob


def main(config_set, db_path):
    d = {'devices': glob('Proteus_Tone_Packs/*/*.json')}
    if config_set == 0:
        d['encoder_conf'] = {"channels": [8, 8],
                             "kernels": [3, 3],
                             "strides": [1, 1],
                             "dilation": [1, 1],
                             "bias": True,
                             "norm": "batch",
                             "conv_block": "res",
                             "activation": "relu"}
        d['train_data'] = {'input': join(db_path, 'dist_fx', 'CareerSG', 'CareerSG-DI.wav'),
                           'seg_len': 1.5, 'lead_in': 0.5, 'batch_size': 8, 'num_batches': 16}

    elif config_set == 1:
        d['encoder_conf'] = {"channels": [16, 32, 32, 64, 64, 64],
                             "kernels": [5, 5, 5, 5, 5, 5],
                             "strides": [1, 1, 1, 1, 1, 1],
                             "dilation": [1, 1, 1, 1, 1, 1],
                             "bias": True,
                             "norm": "batch",
                             "conv_block": "res",
                             "activation": "relu"}
        d['train_data'] = {'input': join(db_path, 'dist_fx', 'CareerSG', 'CareerSG-DI.wav'),
                           'seg_len': 0.75, 'lead_in': 0.25, 'batch_size': 128, 'num_batches': 5000}

    return d