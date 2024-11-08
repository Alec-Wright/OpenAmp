import torch
from os.path import join
from Checkpoints import conf_fxenc
from Utils import fxenc_models


conf = conf_fxenc.main(config_set=1, db_path='')
state_dict = torch.load('Checkpoints/FxEncoder-splendidbreeze23-ep45.pt', map_location='cpu')

model = fxenc_models.FXencoder(conf['encoder_conf'])
model.load_state_dict(state_dict)
model.eval()

# X = [N, C, T]
x = torch.randn(5, 1, 44100)
# out = [N, emb_dim]
out = model(x)
