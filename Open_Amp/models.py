import torch
import numpy as np


class RNN(torch.nn.Module):

    def __init__(self, cell_type, hidden_size, in_channels=1, out_channels=1, residual_connection=True, os_factor=1.0, num_layers=1):
        super().__init__()
        if cell_type == 'gru':
            self.rec = torch.nn.GRU(input_size=in_channels, hidden_size=hidden_size, batch_first=True, num_layers=num_layers)
        elif (cell_type == 'lstm') or (cell_type == "LSTM"):
            self.rec = torch.nn.LSTM(input_size=in_channels, hidden_size=hidden_size, batch_first=True, num_layers=num_layers)
        elif cell_type == 'rnn':
            self.rec = torch.nn.RNN(hidden_size=hidden_size, input_size=in_channels, batch_first=True, num_layers=num_layers)

        self.linear = torch.nn.Linear(in_features=hidden_size, out_features=out_channels)
        self.residual = residual_connection
        self.state = None

    def forward(self, x):

        states, last_state = self.rec(x, self.state)
        out = self.linear(states)
        if self.residual:
            out += x[..., 0].unsqueeze(-1)

        self.state = last_state
        return out, states

    def reset_state(self):
        self.state = None

    def detach_state(self):
        if type(self.state) is tuple:
            hidden = self.state[0].detach()
            cell = self.state[1].detach()
            self.state = (hidden, cell)
        else:
            self.state = self.state.detach()


def vector_to_tuple(x):
    num_states = x.shape[-1]
    assert ((num_states % 2) == 0)
    return x[..., :num_states // 2], x[..., num_states // 2:]


def tuple_to_vector(t):
    return torch.cat(t, dim=-1)


def lstm_cell_forward(cell_function, x, h):
    hc = cell_function(x, vector_to_tuple(h))
    return tuple_to_vector(hc)


def rnn_cell_forward(cell_function, x, h):
    return cell_function(x, h)