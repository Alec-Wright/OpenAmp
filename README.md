
This is the repository for the paper 'Open-Amp: Synthetic Data Framework for Audio Effect Foundation Models'

Open-Amp is a framework for creating large scale and diverse audio effects data using crowd-sourced audio effects models. This repository shows basic usage of the package for training a universal amplifier model, as described in the paper.


# Download amp models and clean guitar data

Use the following code to download the 'Proteus Tone Packs' collecton of amplifier and effect pedal models.
```
curl -LO https://github.com/GuitarML/ToneLibrary/releases/download/v1.0/Proteus_Tone_Packs.zip <br>
tar -xf Proteus_Tone_Packs.zip <br>
rm Proteus_Tone_Packs.zip <br>
```

Use the following code to download clean input guitar for use during training from the IDMT-SMT-GUITAR dataset
```
curl -LO https://zenodo.org/records/7544110/files/IDMT-SMT-GUITAR_V2.zip <br>
tar -xf IDMT-SMT-GUITAR_V2.zip <br>
rm IDMT-SMT-GUITAR_V2.zip <br>
```

# Environment

install the conda environment from the environment.yaml (you must have the conda package manager installed already)

'''
conda env create -f environment.yaml
conda activate open-amp-demo
'''

# Compile input audio files

This goes through the downloaded clean guitar audio, trims silence and produces a single wav file for each of the guitars, in the 'Data' directory

'''
python compile-input-data.py -o 'Data/Ibanez2820-DI' -i 'IDMT-SMT-GUITAR_V2/dataset4/Ibanez 2820'
python compile-input-data.py -o 'Data/CareerSG-DI' -i 'IDMT-SMT-GUITAR_V2/dataset4/Career SG'
'''

# Run Universal Amp Training

This runs a basic version of training the universal amp model

'''
python train_universal_amp.py
'''


