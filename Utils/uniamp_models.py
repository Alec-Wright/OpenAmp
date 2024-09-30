import torch
from torch import nn






""" layer classes: GatedTCNLayer, FilmTCNLayer, GatedTCNLayerFilmConditioned, 
ConditionedConv1D, GatedTCNLayerFullyConditioned
"""

class TCN(nn.Module):
    def __init__(self, layer_class: type, channels=8, blocks=2, layers=8, dilation_growth=2, kernel_size=3, cond_pars=5,
                 emb_dim=128, num_emb=109, norm_emb=False, emb_reg=False, emb_proj=False):
        super(TCN, self).__init__()
        # Set number of layers  and hidden_size for network layer/s
        self.layers = layers
        self.kernel_size = kernel_size
        self.dilation_growth = dilation_growth
        self.channels = channels
        self.blocks = nn.ModuleList()
        self.norm_emb = norm_emb
        self.emb_reg = emb_reg
        self.emb_proj = emb_proj

        if self.emb_proj:
            self.projector = torch.nn.Sequential(
                torch.nn.Linear(emb_dim, 64),
                torch.nn.ReLU(),
                torch.nn.Linear(64, 128),
                torch.nn.ReLU(),
                torch.nn.Linear(128, cond_pars)
            )

        self.first_conv = nn.Conv1d(in_channels=1, out_channels=channels, kernel_size=1)
        for b in range(blocks):
            self.blocks.append(TCNBlock(layer_class, channels, channels, dilation_growth, kernel_size, layers, cond_pars))
        self.last_conv = nn.Conv1d(in_channels=channels, out_channels=1, kernel_size=1)

        self.emb = nn.Embedding(embedding_dim=emb_dim, num_embeddings=num_emb)

    def forward(self, x, c):
        c = self.emb(torch.argmax(c, dim=1))
        if self.emb_proj:
            c = self.projector(c)
        x = self.first_conv(x)
        skip = 0
        for block in self.blocks:
            x, zn = block(x, c)
            skip += zn
        output = self.last_conv(skip)
        return output

    def proc_with_emb_id(self, x, emb):
        c = self.emb(torch.tensor(emb))
        if len(c.shape) == 1:
            c = c.unsqueeze(0)
        if self.emb_proj:
            c = self.projector(c)
        else:
            c = emb
        x = self.first_conv(x)
        skip = 0
        for block in self.blocks:
            x, zn = block(x, c)
            skip += zn
        output = self.last_conv(skip)
        return output


""" 
Gated convolutional neural net block, applies successive gated convolutional layers to the input, a total of 'layers'
layers are applied, with the filter size 'kernel_size' and the dilation increasing by a factor of 'dilation_growth' for
 each successive layer."""


class TCNBlock(nn.Module):
    def __init__(self, layer_class, chan_input, chan_output, dilation_growth, kernel_size, layers, cond_pars):
        super(TCNBlock, self).__init__()
        self.channels = chan_output
        dilations = [dilation_growth ** lay for lay in range(layers)]
        self.layers = nn.ModuleList()
        for dil in dilations:
            self.layers.append(layer_class(chan_input, chan_output, dil, kernel_size, cond_pars))

    def forward(self, x, c):
        skip = 0
        for layer in self.layers:
            x, zn = layer(x, c)
            skip += zn
        return x, skip

'''
FiLM module -- adapted from https://github.com/csteinmetz1/micro-tcn/blob/main/microtcn/tcn.py
'''
class FiLM(torch.nn.Module):
    def __init__(self,
                 num_features,
                 cond_dim):
        super().__init__()
        self.num_features = num_features
        self.adaptor = torch.nn.Linear(cond_dim, num_features * 2)

    def forward(self, x, cond):
        cond = self.adaptor(cond)
        g, b = torch.chunk(cond, 2, dim=-1)
        g = g.unsqueeze(2)
        b = b.unsqueeze(2)
        x = (x * g) + b

        return x

'''
Bias conditioning
'''
class BiasConditioning(torch.nn.Module):
    def __init__(self,
                 num_features,
                 cond_dim):
        super().__init__()
        self.num_features = num_features
        self.adaptor = nn.Linear(cond_dim, num_features)

    def forward(self, x, cond):
        cond = self.adaptor(cond).unsqueeze(2)
        return x + cond


""" 
Gated convolutional layer, zero pads and then applies a causal convolution to the input. Bias conditioning. """

class GatedTCNLayer(nn.Module):

    def __init__(self, chan_input, chan_output, dilation, kernel_size, cond_pars):
        super(GatedTCNLayer, self).__init__()
        self.channels = chan_output
        self.in_chan = chan_input

        self.conditioned_bias = BiasConditioning(chan_output*2, cond_pars)
        self.conv = nn.Conv1d(in_channels=chan_input, out_channels=chan_output*2, kernel_size=kernel_size, stride=1,
                              padding=0, dilation=dilation, bias=False)

        self.resi_con = nn.Conv1d(in_channels=chan_output, out_channels=chan_output, kernel_size=1, stride=1, padding=0)
        self.zpad = ((kernel_size-1)*dilation, 0)

    '''
        x dims: (batch, channels, time)
        c dims: (batch, channels/features)
    '''
    def forward(self, x, c):
        residual = x
        # Zero pad on the left side, so that y is the same length as x
        y = self.conv(torch.nn.functional.pad(x, self.zpad))
        y = self.conditioned_bias(y, c)
        z = torch.tanh(y[:, 0:self.channels, :]) * torch.sigmoid(y[:, self.channels:, :])
        x = self.resi_con(z) + residual
        return x, z


'''
TCN layer with FiLM -- adapted from https://github.com/csteinmetz1/micro-tcn/blob/main/microtcn/tcn.py
'''
class FilmTCNLayer(nn.Module):
    def __init__(self, chan_input, chan_output, dilation, kernel_size, cond_pars):
        super().__init__()
        self.channels = chan_output
        self.in_chan = chan_input

        self.conv = nn.Conv1d(in_channels=chan_input, out_channels=chan_output, kernel_size=kernel_size, stride=1,
                              padding=0, dilation=dilation)

        self.resi_con = nn.Conv1d(in_channels=chan_output, out_channels=chan_output, kernel_size=1, stride=1, padding=0)
        self.zpad = ((kernel_size-1)*dilation, 0)

        self.film = FiLM(chan_output, cond_pars)
        self.relu = nn.PReLU(chan_output)

    '''
        x dims: (batch, channels, time)
        c dims: (batch, channels/features)
    '''
    def forward(self, x, c):
        residual = x

        y = self.conv(torch.nn.functional.pad(x, self.zpad))
        y = self.film(y, c)
        z = self.relu(y)

        x = self.resi_con(z) + residual
        return x, z


'''
Gated TCN layer with FiLM conditioning
'''
class GatedTCNLayerFilmConditioned(nn.Module):

    def __init__(self, chan_input, chan_output, dilation, kernel_size, cond_pars):
        super().__init__()
        self.channels = chan_output
        self.in_chan = chan_input

        self.conv = nn.Conv1d(in_channels=chan_input, out_channels=chan_output*2, kernel_size=kernel_size, stride=1,
                              padding=0, dilation=dilation)
        self.film = FiLM(num_features=chan_output*2, cond_dim=cond_pars)

        self.resi_con = nn.Conv1d(in_channels=chan_output, out_channels=chan_output, kernel_size=1, stride=1, padding=0)
        self.zpad = ((kernel_size-1)*dilation, 0)

    '''
        x dims: (batch, channels, time)
        c dims: (batch, channels/features)
    '''
    def forward(self, x, c):
        residual = x
        # Zero pad on the left side, so that y is the same length as x
        y = self.conv(torch.nn.functional.pad(x, self.zpad))
        y = self.film(y, c)
        z = torch.tanh(y[:, 0:self.channels, :]) * torch.sigmoid(y[:, self.channels:, :])
        x = self.resi_con(z) + residual
        return x, z


'''
Conv1D module with conditioned kernel weights. No bias.
'''
class ConditionedConv1D(nn.Module):
    def __init__(self, in_channels, out_channels, dilation, kernel_size, cond_pars):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.dilation = dilation
        self.adapter = nn.Linear(in_features=cond_pars, out_features=kernel_size*in_channels*out_channels)

    def forward(self, x, c):
        batch_size = x.shape[0]
        x = torch.reshape(x, (1, self.in_channels*batch_size, x.shape[-1]))
        kernel = self.adapter(c)
        kernel = torch.reshape(kernel, (self.out_channels * batch_size, self.in_channels, self.kernel_size))
        y = nn.functional.conv1d(input=x, weight=kernel, dilation=self.dilation, groups=batch_size)
        return torch.reshape(y, (batch_size, self.out_channels, y.shape[-1]))


""" 
Gated convolutional layer, fully conditioned weights and bias"""

class GatedTCNLayerFullyConditioned(nn.Module):

    def __init__(self, chan_input, chan_output, dilation, kernel_size, cond_pars):
        super(GatedTCNLayerFullyConditioned, self).__init__()
        self.channels = chan_output
        self.in_chan = chan_input

        self.cond_to_kernel = nn.Linear(in_features=cond_pars, out_features=kernel_size)
        self.conv = ConditionedConv1D(in_channels=chan_input, out_channels=chan_output*2, kernel_size=kernel_size, dilation=dilation, cond_pars=cond_pars)
        self.conditioned_bias = BiasConditioning(chan_output*2, cond_pars)
        self.zpad = ((kernel_size - 1) * dilation, 0)

        self.resi_con = nn.Conv1d(in_channels=chan_output, out_channels=chan_output, kernel_size=1, stride=1, padding=0)

    '''
        x dims: (batch, channels, time)
        c dims: (batch, channels/features)
    '''
    def forward(self, x, c):
        residual = x
        x_pad = torch.nn.functional.pad(x, self.zpad)
        y = self.conv(x_pad, c)
        y = self.conditioned_bias(y, c)
        z = torch.tanh(y[:, 0:self.channels, :]) * torch.sigmoid(y[:, self.channels:, :])
        x = self.resi_con(z) + residual
        return x, z