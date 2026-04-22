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

compress-multi-channel-and-surround-audio/
│
├── src/                         # Source code chính
│   ├── app.py                   # Streamlit UI
│   ├── main.py                  # CLI pipeline (chạy test)
│
│   ├── audio_io.py              # Load / save audio
│   ├── mdct.py                  # MDCT / IMDCT transform
│   ├── transform.py             # PCA decorrelation
│   ├── coupling.py              # Channel coupling + spectrum plot
│   ├── residual.py              # Residual prediction / reconstruction
│   ├── compressor.py            # Quantization + zlib
│   ├── metrics.py               # SNR, bitrate, compression ratio
│   ├── analysis.py              # Correlation + heatmap
│
├── data/                        # Input audio files
│   └── test.wav
│
├── output/                      # Output audio (reconstructed)
│   └── reconstructed.wav
│
├── assets/                  
│   ├── ui_main.png
│   ├── ui_output.png
│   ├── heatmap.png
│   ├── mdct_spectrum.png
│   └── residual_distribution.png
│
├── README.md                   # Project description
└── requirements.txt            # Dependencies
---

##  Installation

### 1. Install Python
```bash
python --version
# Python >= 3.10 recommended
pip install numpy matplotlib soundfile streamlit
```
 How to Run
Run interactive UI:
```bash
cd src
python -m streamlit run app.py
```
then open http://localhost:8501
 Reproducibility
Audio file: WAV (stereo recommended)
Duration: 5 seconds
Quality slider: 0.7
PCA: ON
Fast mode: ON

Expected Results
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
 License
This project is for educational purposes.
