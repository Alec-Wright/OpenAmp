---
layout: splash
classes:
  - wide
---

<style>
        /* Flexbox container to align images side by side */
        .image-container {
            display: flex;
            justify-content: space-between; /* Adjust spacing between images */
        }
        
        /* Style for each figure element */
        figure {
            text-align: center;
            margin: 0 50px; /* Add some space between the images */
        }
        
        /* Ensure images are responsive */
        img {
            max-width: 100%; /* Makes sure the image doesn't overflow */
            height: auto;
        }
        
        /* Optional: Add caption styling */
        figcaption {
            font-style: italic;
            font-size: 0.75em;
            margin-top: 5px;
            text-align: center;
        }
        
        .table-container {
            width: 100%;
            overflow-x: auto; /* Adds horizontal scrollbar if content exceeds width */
        }
        
        table {
            width: 100%; /* Optional: Adjusts table width to fit container */
            border-collapse: collapse;
        }
        
        th, td {
            text-align: center;
        }
        
        td {
            background-color: white;
        }
        
        audio {
            width: 12em;
        }
        
        .image-container {
            display: flex;
            justify-content: space-between; /* Adjust spacing between images */
        }
        
        /* Ensure images are responsive */
        img {
            max-width: 100%; /* Makes sure the image doesn't overflow */
            height: auto;
        }
        
        h2 {
            font-size: 1.7em;
            text-align: center;
        }
        
        h3 {
            font-size: 1.4em;
            text-align: left;
        }
        
        h4 {
            text-align: left;
            font-size: 1.1em
        }
        
        h5 {
            text-align: left;
            font-size: 1.0em
        }
        
        body {
          font-size: 0.9em;
        }

</style>

## Open-Amp: Synthetic Data Framework for Audio Effect Foundation Models
<div style="text-align: center; font-size: 1.0em">
    <p style="font-size: 1.1em">
    Alec Wright<sup>1</sup>, Alistair Carson<sup>1</sup>,  and Lauri Juvela<sup>2</sup>
    </p>
    <i>
        <sup>1</sup><a href="https://www.acoustics.ed.ac.uk/" target="_blank" rel="noopener noreferrer">Acoustics and Audio Group</a>, University of Edinburgh, Edinburgh, UK<br>
        <sup>2</sup> Department of Information and Communications Engineering (DICE), Aalto University, Espoo, Finland <br>
    </i>
<br>
    <a href="" 
        class="btn btn--primary btn--large"
        target="_blank" rel="noopener noreferrer">
    🗞️ Paper
    </a>
    <a href="https://github.com/Alec-Wright/OpenAmp" 
        class="btn btn--primary btn--large"
        target="_blank" rel="noopener noreferrer">
    </> Code
    </a>
</div>
### Abstract
This paper introduces Open-Amp, a synthetic data framework for generating large-scale and diverse audio effects data. Audio effects are relevant to many musical audio processing and Music Information Retrieval (MIR) tasks, such as modelling of analog audio effects, automatic mixing, tone matching and transcription. Existing audio effects datasets are limited in scope, usually including relatively few audio effects processors and a limited amount of input audio signals. Our proposed framework overcomes these issues, by crowdsourcing neural network emulations of guitar amplifiers and effects, created by users of open-source audio effects emulation software. This allows users of Open-Amp complete control over the input signals to be processed by the effects models, as well as providing high-quality emulations of hundreds of devices. Open-Amp can render audio online during training, allowing great flexibility in data augmentation. Our experiments show that using Open-Amp to train a guitar effects encoder achieves new state-of-the-art results on multiple guitar effects classification tasks. Furthermore, we train a one-to-many guitar effects model using Open-Amp, and  use it to emulate unseen analog effects via manipulation of it's learned latent space, indicating transferability to analog guitar effects data.


### One-to-many audio effect emulation
In the paper we proposed using the OpenAmp dataset to train a one-to-many guitar effect emulation model. 
We used a temporal convolutional network (TCN) architecture and conditioned it on a learnable look-up table of embeddings. The model learns 
one embedding vector per (virtual) amp or pedal in the OpenAmp dataset, so at inference we can render a specific guitar tone by selecting the 
relevant embedding from the look-up table and processing audio through the TCN. This also allows us to enrol unseen analog devices into the pre-trained one-to-many 
model by learning a new embedding within the existing space. In this demo we show audio examples of:

- [OpenAmp devices seen during training](#1-openamp-devices-seen-during-training)
- [Unseen analog devices](#2-egfxset-devices----enrolled-into-pre-trained-model-using-unseen-data)


#### 1. OpenAmp devices seen during training
The tables below contain audio examples from 5 virtual devices within the OpenAmp dataset (seen during training):
- [EffectrodeBlackbirdClean (PedalPack4)](#11-effectrodeblackbirdclean-pedalpack4)
- [ZenDrive_BlackMagic_DriveKnob (PedalPack2)](#12-zendrive_blackmagic_driveknob-pedalpack2)
- [Bogner_EcstasyBlue_GainKnob_cond-0.25 (PedalPack2)](#13-bogner_ecstasyblue_gainknob_cond-025-pedalpack2)
- [Colombo_Plexi_Knob_cond-0.50 (PedalPack2)](#14-colombo_plexi_knob_cond-050-pedalpack2)
- [SoundCity50_ThroneTorcher_DIRECT (AmpPack2)](#15-soundcity50_thronetorcher_direct-amppack2)

For each device we can compare rendered audio output outputs from the proposed one-to-many models (Emb-16, Emb-64 and Emb-64), 
a baseline 1-to-1 TCN model, and the target tone rendered from the OpenAmp set. 
NB the 5 devices were selected (and ordered below) based on the minimum, 25th percentile, median, 75th percentile and maximum test loss of the Emb-64 model to show the spread 
of modeling capabilities. The test losses are shown in Table III in the paper.

Clean input signals (unseen during training) used to render the examples:
<div class="table-container">
<table>
  <thead>
    <tr>
      <th>Clip 1</th>
      <th>Clip 2</th>
      <th>Clip 3</th>
      <th>Clip 4</th>
    </tr>
    <tr>
      <td><audio controls><source src="audio/input/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/input/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/input/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/input/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
</thead>
</table>
</div>

##### 1.1 EffectrodeBlackbirdClean (PedalPack4)
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1"> Model </th>
      <th>Clip 1</th>
      <th>Clip 2</th>
      <th>Clip 3</th>
      <th>Clip 4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/target/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/target/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/target/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/target/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/base/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/base/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/base/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/base/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb16/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb16/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb16/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb16/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb64/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb64/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb64/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb64/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb256/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb256/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb256/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/EffectrodeBlackbirdClean/Emb256/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>

##### 1.2 ZenDrive_BlackMagic_DriveKnob (PedalPack2)
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1"> Model </th>
      <th>Clip 1</th>
      <th>Clip 2</th>
      <th>Clip 3</th>
      <th>Clip 4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/target/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/target/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/target/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/target/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/base/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/base/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/base/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/base/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb16/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb16/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb16/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb16/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb64/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb64/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb64/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb64/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb256/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb256/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb256/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/ZenDrive_BlackMagic_DriveKnob_cond-0.25/Emb256/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>

##### 1.3 Bogner_EcstasyBlue_GainKnob_cond-0.25 (PedalPack2)
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1"> Model </th>
      <th>Clip 1</th>
      <th>Clip 2</th>
      <th>Clip 3</th>
      <th>Clip 4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/target/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/target/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/target/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/target/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/base/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/base/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/base/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/base/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb16/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb16/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb16/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb16/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb64/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb64/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb64/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb64/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb256/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb256/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb256/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Bogner_EcstasyBlue_GainKnob_cond-0.25/Emb256/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>

##### 1.4 Colombo_Plexi_Knob_cond-0.50 (PedalPack2)
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1"> Model </th>
      <th>Clip 1</th>
      <th>Clip 2</th>
      <th>Clip 3</th>
      <th>Clip 4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/target/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/target/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/target/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/target/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/base/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/base/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/base/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/base/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb16/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb16/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb16/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb16/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb64/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb64/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb64/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb64/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb256/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb256/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb256/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/Colombo_Plexi_Knob_cond-0.50/Emb256/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>

##### 1.5 SoundCity50_ThroneTorcher_DIRECT (AmpPack2)
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1"> Model </th>
      <th>Clip 1</th>
      <th>Clip 2</th>
      <th>Clip 3</th>
      <th>Clip 4</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/target/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/target/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/target/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/target/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/base/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/base/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/base/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/base/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb16/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb16/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb16/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb16/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb64/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb64/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb64/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb64/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb256/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb256/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb256/clip_4.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/SoundCity50_ThroneTorcher_DIRECT/Emb256/clip_6.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>

#### 2. EGFxSet devices -- enrolled into pre-trained model using unseen data
In [Section 2](#2-egfxset-devices--enrolled-into-pre-trained-model-using-unseen-data) we explore the task of enrolling unseen analog effects into 
the learned embedding space of the foundation one-to-many model. Here we used data from the [EGFxSet](https://egfxset.github.io/) dataset. 
This consists of ~1 hour of single guitar notes processed through various analog effects devices. 
In our experiments we froze all parameters in the pre-trained foundation model and learned a new embedding for three analog effects pedals (unseen during training):
- [Ibanez TubeScreamer Mini](#21-ibanez-tubescreamer-mini)
- [Proco RAT](#22-proco-rat)
- [Boss Blues Driver BD-2](#23-boss-blues-driver-bd-2)

<br>
<div class="image-container">
<figure style="width:10%">
    <img src="img/291825-71P1LHdAiGL._SL1500___30597.jpg" alt="TSMini">
    <figcaption style="font-size: 0.5em">Image source: <a href="https://www.andertons.co.uk/ibanez-tube-screamer-mini-overdrive-pedal/" target="_blank" rel="noopener noreferrer">https://www.andertons.co.uk/ibanez-tube-screamer-mini-overdrive-pedal/</a></figcaption>
</figure>
<figure style="width:20%">
    <img src="img/procorat.jpg" alt="RAT">
    <figcaption style="font-size: 0.5em">Image source: <a href="https://www.gear4music.com/Guitar-and-Bass/Pro-Co-RAT-2-Distortion/CDA" target="_blank" rel="noopener noreferrer">https://www.gear4music.com/Guitar-and-Bass/Pro-Co-RAT-2-Distortion/CDA</a></figcaption>
</figure>
<figure style="width:10%">
    <img src="img/26822-BOSSBD2__28872.jpg" alt="BD2">
    <figcaption style="font-size: 0.5em">Image source: <a href="https://www.andertons.co.uk/boss-bd-2-blues-driver-pedal" target="_blank" rel="noopener noreferrer">https://www.andertons.co.uk/boss-bd-2-blues-driver-pedal</a></figcaption>
</figure>
</div>
<br>
Input signals (unseen during training) used to render the examples<sup>*</sup>:
<table>
  <thead>
    <tr>
      <th colspan="4" style="border-right: 1px solid gray">Note 1</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 2</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 3</th>
      <th colspan="4">Note 4</th>
    </tr>
</thead>
<tbody>
    <tr>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/input/clip_0.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/input/clip_1.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/input/clip_2.wav" type="audio/wav"></audio></td>
      <td colspan="4"><audio controls><source src="audio/TubeScreamer/input/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
</tbody>
</table>
<sup>*</sup>NB these are different to that of [Section 1](#1-openamp-devices-seen-during-training) to allow comparison with the target tone in the EGFxSet.

##### 2.1 Ibanez TubeScreamer Mini
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1" style="  background: white"></th>
      <th colspan="4" style="border-right: 1px solid gray">Note 1</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 2</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 3</th>
      <th colspan="4">Note 4</th>
    </tr>
    <tr>
      <th colspan="1"></th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4">Train data length</th>
    </tr>
    <tr>
      <th>Model</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th>~3 s (0.1%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/target/clip_0.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/target/clip_1.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/target/clip_2.wav" type="audio/wav"></audio></td>
      <td colspan="4"><audio controls><source src="audio/TubeScreamer/target/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/base/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/base/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/base/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/base/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/16/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/16/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/16/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/16/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/64/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/64/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/64/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/64/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/256/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/256/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/TubeScreamer/256/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/TubeScreamer/256/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>

##### 2.2 Proco RAT
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1" style="  background: white"></th>
      <th colspan="4" style="border-right: 1px solid gray">Note 1</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 2</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 3</th>
      <th colspan="4">Note 4</th>
    </tr>
    <tr>
      <th colspan="1"></th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4">Train data length</th>
    </tr>
    <tr>
      <th>Model</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th>~3 s (0.1%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/target/clip_0.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/target/clip_1.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/target/clip_2.wav" type="audio/wav"></audio></td>
      <td colspan="4"><audio controls><source src="audio/RAT/target/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/RAT/base/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/base/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/base/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/base/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/base/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/RAT/16/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/16/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/16/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/16/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/16/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/RAT/64/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/64/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/64/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/64/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/64/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/RAT/256/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/256/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/256/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/RAT/256/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/RAT/256/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>

##### 2.3 Boss Blues Driver BD-2
<div class="table-container">
<table>
  <thead>
    <tr>
      <th colspan="1" style="  background: white"></th>
      <th colspan="4" style="border-right: 1px solid gray">Note 1</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 2</th>
      <th colspan="4" style="border-right: 1px solid gray">Note 3</th>
      <th colspan="4">Note 4</th>
    </tr>
    <tr>
      <th colspan="1"></th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4" style="border-right: 1px solid gray">Train data length</th>
      <th colspan="4">Train data length</th>
    </tr>
    <tr>
      <th>Model</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th style="border-right: 1px solid gray">~3 s (0.1%)</th>
      <th>~50 min. (100%)</th>
      <th>~5 min. (10%)</th>
      <th>~30 s (1%) </th>
      <th>~3 s (0.1%)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" style=" font-weight: bold">TARGET </td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/target/clip_0.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/target/clip_1.wav" type="audio/wav"></audio></td>
      <td colspan="4" style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/target/clip_2.wav" type="audio/wav"></audio></td>
      <td colspan="4"><audio controls><source src="audio/BluesDriver/target/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Baseline 1-to-1</td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/base/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/base/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/base/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/base/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 16</td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/16/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/16/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/16/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/16/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 64</td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/64/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/64/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/64/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/64/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
    <tr>
      <td>Emb 256</td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=1.0/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.1/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.01/clip_0.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/256/data_length=0.001/clip_0.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=1.0/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.1/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.01/clip_1.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/256/data_length=0.001/clip_1.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=1.0/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.1/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.01/clip_2.wav" type="audio/wav"></audio></td>
      <td style="border-right: 1px solid gray"><audio controls><source src="audio/BluesDriver/256/data_length=0.001/clip_2.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=1.0/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.1/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.01/clip_3.wav" type="audio/wav"></audio></td>
      <td><audio controls><source src="audio/BluesDriver/256/data_length=0.001/clip_3.wav" type="audio/wav"></audio></td>
    </tr>
  </tbody>
</table>
</div>