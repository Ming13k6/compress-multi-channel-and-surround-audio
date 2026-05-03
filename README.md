# 🎧 Multi-Channel Audio Compression System

##  Overview

This project implements a **multi-channel audio compression pipeline** combining:

- PCA (decorrelation)
- MDCT (frequency transform)
- Channel coupling
- Residual prediction
- Quantization + entropy coding (zlib)

The system provides an **interactive Streamlit-based UI**, allowing users to explore the trade-off between compression efficiency and audio quality in real time.

---

##  Objectives

- Reduce redundancy in multi-channel audio
- Achieve efficient compression
- Maintain acceptable reconstruction quality
- Provide an interactive demo for experimentation

---

##  System Pipeline
Input Audio
↓
PCA (optional)
↓
MDCT (per channel)
↓
Channel Coupling (high-frequency)
↓
Residual Prediction
↓
Quantization + zlib Compression
↓
Decompression
↓
IMDCT
↓
Inverse PCA
↓
Reconstructed Audio

---

##  Features

###  Core Compression
- Multi-channel audio support
- PCA-based decorrelation
- MDCT transform (512-point window)
- High-frequency channel coupling
- Temporal residual prediction
- Dead-zone quantization

---

###  Interactive UI (Streamlit)
- Upload `.wav` audio files
- Adjustable compression via **Quality slider**
- Toggle PCA decorrelation
- Fast mode for real-time demo
- A/B playback (original vs compressed)

---

###  Metrics
- **SNR (Signal-to-Noise Ratio)**
- **Compression Ratio**
- **Bitrate (total & per-channel)**

---

###  Visualization
- Waveform comparison
- Spectrogram comparison (optional)

---

## Project Structure
```
compress-multi-channel-and-surround-audio/
│
├── src/
│ ├── app.py
│ ├── main.py
│ ├── audio_io.py
│ ├── mdct.py
│ ├── transform.py
│ ├── coupling.py
│ ├── residual.py
│ ├── compressor.py
│ ├── metrics.py
│ ├── analysis.py
│
├── data/
│ └── test.wav
│
├── output/
│ └── reconstructed.wav
├── README.md
└── requirements.txt
```
##  Installation

1. Prerequisites

Before running the project, make sure the following software is installed on your machine:

Python 3.10 or higher
pip (Python package manager)

To verify your installation, run:
```
python --version
pip --version
```
If pip is not recognized, you can use:
```
python -m pip --version
```
2. Clone or Download the Project

If using Git:
```
git clone <your-repository-link>
cd compress-multi-channel-and-surround-audio
```
If not using Git, download the project as a ZIP file and extract it, then open the project folder.

3. Create a Virtual Environment (Recommended)

It is recommended to create a virtual environment to avoid package conflicts.

On Windows
```
python -m venv venv
venv\Scripts\activate
```
On macOS / Linux
```
python3 -m venv venv
source venv/bin/activate
```
After activation, your terminal should show something like:
(venv)
4. Install Required Dependencies

This project uses the following Python libraries:

numpy
matplotlib
soundfile
streamlit
Preferred method: install from requirements.txt

Make sure the file requirements.txt exists in the project root with the following content:

numpy
matplotlib
soundfile
streamlit

Run:
```
pip install -r requirements.txt
```
If pip does not work directly, use:
```
python -m pip install -r requirements.txt
```
Manual Installation (If Needed)
```
python -m pip install numpy matplotlib soundfile streamlit
```
Verify Installation
```
python -c "import numpy, matplotlib, soundfile, streamlit; print('All dependencies installed successfully!')"
```

## How to run
1. Run the Interactive UI (Recommended)
Make sure your terminal is currently at ...\compress-multi-channel-and-surround-audio

The project provides a Streamlit-based interface for interactive testing.
```
python -m streamlit run src/app.py
```
After running the command, open your browser and go to:

http://localhost:8501
2. Using the UI

Inside the interface:

1, Upload a .wav audio file
2, Adjust parameters:
Duration: select how many seconds to process
Quality slider: controls compression strength
PCA toggle: enable/disable channel decorrelation
Fast mode: speeds up processing (lower accuracy)
3, Click Run Compression
3. Output

After processing, the UI will display:

- Playback (original vs reconstructed)
- Metrics:
SNR (Signal-to-Noise Ratio)
Compression Ratio
Bitrate (total & per-channel)
- Visualizations:
Waveform comparison
Spectrogram (optional)

## Reproducibility

## Expected Results
SNR ≈ 6–10 dB
Compression Ratio ≈ 7–9x
Bitrate significantly reduced
 Evaluation Metrics
1. Signal-to-Noise Ratio (SNR)
SNR = 10 * log10(signal_power / noise_power)

Measures reconstruction quality.

2. Compression Ratio (CR)
CR = original_size / compressed_size

Measures compression efficiency.

3. Bitrate
bitrate = (compressed_size * 8 * sample_rate) / num_samples
 Results & Observations
PCA reduces inter-channel redundancy but has limited impact when channel correlation is low
MDCT enables efficient frequency-domain compression
Channel coupling reduces high-frequency redundancy
Residual prediction helps capture temporal dependencies
 Trade-offs & Limitations
Higher compression → increased noise/artifacts
Dead-zone quantization removes small signals → potential distortion
Coupling may degrade high-frequency details
No psychoacoustic model (unlike MP3/AAC)
MDCT implementation is simplified
 Future Work
Add psychoacoustic masking
Adaptive quantization
Improved residual modeling
Real-time streaming support
GPU acceleration
 Demo

The system demonstrates:

Real-time compression
Audio playback comparison
Interactive parameter tuning
Visualization (waveform + spectrogram)
Author
Phạm Trần Tuấn Minh
Hoàng Lê Minh
 License
This project is for educational purposes.
