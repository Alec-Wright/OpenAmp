from os.path import join
from glob import glob
from Utils import uniamp_models as models

def main(model_conf):

    if model_conf == 100:
        d = {'layer_class': models.GatedTCNLayerFilmConditioned,
                    'channels': 16, 'blocks': 2, 'layers': 8, 'dilation_growth': 2, 'kernel_size': 3, 'cond_pars': 64,
                    'emb_dim': 4, 'emb_reg': False, 'emb_proj': True}
    elif model_conf == 102:
        d = {'layer_class': models.GatedTCNLayerFilmConditioned,
                    'channels': 16, 'blocks': 2, 'layers': 8, 'dilation_growth': 2, 'kernel_size': 3, 'cond_pars': 64,
                    'emb_dim': 8, 'emb_reg': False, 'emb_proj': True}

    return d