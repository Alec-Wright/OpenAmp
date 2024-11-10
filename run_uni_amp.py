import torch, torchaudio
import pandas as pd
from os.path import join
from Checkpoints.UniFxModel import uniamp_confs
from Utils import uniamp_models


check_dir = join('Checkpoints', 'UniFxModel')
conf = 102
model = 'GiddyDisco113'
ep = 3

# This is the model directory where the checkpoint is saved
model_dir = join(check_dir, f'conf{conf}-UniFx-{model}-ep{ep}.pt')
# This gets the config of the neural network for loading the checkpoint
conf = uniamp_confs.main(model_conf=conf)
# This loads the lookup-table, which contains the indices for each amplifier the model was trained to emulate
df = pd.read_csv(join(check_dir, 'train_index.csv'), index_col=0)


encodings = df.index.values
state_dict = torch.load(model_dir, map_location=torch.device('cpu'))
model = uniamp_models.TCN(**conf, num_emb=df.shape[0])
model.load_state_dict(state_dict)

embeddings = model.emb(torch.tensor(encodings, dtype=torch.long)).detach()

# Pick device id from lookup-table, print device name
device_id = 4
print(df.iloc[device_id].model)
# This is the corresponding device embedding
dev_emb = embeddings[device_id, :]

# Load input file
input_sig, fs = torchaudio.load('Open_Amp/test/guitar-in.wav')
input_sig = input_sig[:, :].unsqueeze(0)

# Process input using device model, save output
output = model.proc_with_emb_id(input_sig, device_id)
torchaudio.save('uniamp_out.wav', output[0, :, :].detach().to(torch.device('cpu')), sample_rate=fs)

print(3)

