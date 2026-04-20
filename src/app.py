import os
import tempfile

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from audio_io import load_audio, save_audio
from compressor import compress_data, decompress_data
from coupling import mdct_coupling
from mdct import mdct, imdct
from metrics import compute_compression_ratio, compute_snr
from residual import compute_residual, reconstruct_from_residual
from transform import pca_decorrelation



# PAGE CONFIG

st.set_page_config(
    page_title="Audio Compression Demo",
    page_icon="🎧",
    layout="wide",
)

st.title("🎧 Multi-Channel Audio Compression System")
st.markdown("Interactive demo for PCA + MDCT + Residual Compression")



# HELPERS

def to_stereo_for_preview(audio: np.ndarray) -> np.ndarray:
    """
    Streamlit audio preview works most reliably with mono/stereo.
    If the signal has >2 channels, keep the first 2 channels for preview.
    """
    if audio.ndim == 1:
        return audio
    if audio.shape[1] == 1:
        return audio[:, 0]
    if audio.shape[1] >= 2:
        return audio[:, :2]
    return audio


def render_spectrogram(signal: np.ndarray, sr: int, title: str):
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.specgram(signal, Fs=sr)
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    plt.close(fig)



# SIDEBAR / CONTROLS

st.sidebar.header("Controls")

duration = st.sidebar.slider("⏱ Audio duration (seconds)", 2, 10, 5)
quality = st.sidebar.slider("🎚 Quality ↔ Compression", 0.0, 1.0, 0.7)
use_pca = st.sidebar.checkbox("🧠 Use PCA", True)
fast_mode = st.sidebar.checkbox("⚡ Fast mode", True)
show_spectrogram = st.sidebar.checkbox("📊 Show spectrogram", True)

# Quality mapping
qbits = int(8 + quality * 8)             # 8 -> 16 bits
deadzone = 10 ** (-2 - 3 * quality)      # 1e-2 -> 1e-5

st.sidebar.markdown("### Current codec settings")
st.sidebar.write(f"**qbits:** {qbits}")
st.sidebar.write(f"**deadzone:** {deadzone:.6f}")

if quality < 0.3:
    st.sidebar.warning("⚡ High Compression Mode")
elif quality < 0.7:
    st.sidebar.info("⚖ Balanced Mode")
else:
    st.sidebar.success("🎧 High Quality Mode")



# FILE UPLOAD

uploaded_file = st.file_uploader("Upload WAV file", type=["wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_in:
        tmp_in.write(uploaded_file.read())
        input_path = tmp_in.name

    data, sr = load_audio(input_path)

    st.subheader("Input Information")
    info_col1, info_col2, info_col3 = st.columns(3)
    info_col1.write(f"**Sample rate:** {sr}")
    info_col2.write(f"**Shape:** {data.shape}")
    info_col3.write(f"**Channels:** {data.shape[1] if data.ndim > 1 else 1}")

    # Trim to selected duration
    max_samples = min(len(data), sr * duration)
    data = data[:max_samples]

    # Optional speed mode for demo responsiveness
    if fast_mode:
        data = data[::2]
        sr = sr // 2

    st.subheader("🎧 Original Audio")
    original_preview = to_stereo_for_preview(data)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_orig:
        sf_path = tmp_orig.name
    save_audio(sf_path, original_preview, sr)
    st.audio(sf_path)

    if st.button("🚀 Run Compression", type="primary"):
        with st.spinner("Processing audio..."):
            
            # PCA / NO PCA
            
            if use_pca:
                transformed, eigvecs, mean = pca_decorrelation(data)
            else:
                transformed = data.copy()
                eigvecs = np.eye(data.shape[1], dtype=np.float32)
                mean = np.zeros(data.shape[1], dtype=np.float32)

            
            # MDCT PER CHANNEL
            
            channels_mdct = []
            scales = []
            max_blocks = 3000  # avoid UI crash for long files

            for ch_idx in range(transformed.shape[1]):
                ch = transformed[:, ch_idx]

                m = np.max(np.abs(ch))
                if m == 0:
                    m = 1.0
                scales.append(m)

                coeffs = mdct(ch / m)
                coeffs = coeffs[:max_blocks]
                channels_mdct.append(coeffs)

            scales = np.array(scales, dtype=np.float32)

            
            # COUPLING
            
            X_coupled, _ = mdct_coupling(channels_mdct, sr)

            
            # RESIDUAL
            
            combined_mdct = np.transpose(X_coupled, (0, 2, 1)).astype(np.float32)
            residual = compute_residual(combined_mdct)

            
            # COMPRESS / DECOMPRESS
            
            compressed, meta = compress_data(
                residual,
                qbits=qbits,
                deadzone=deadzone,
            )

            residual_decoded = decompress_data(compressed, meta)
            reconstructed_res = reconstruct_from_residual(residual_decoded)
            reconstructed_mdct = np.transpose(reconstructed_res, (0, 2, 1))

            
            # IMDCT
            
            channels_time = []
            for ch_idx in range(reconstructed_mdct.shape[2]):
                recon = imdct(reconstructed_mdct[:, :, ch_idx]) * scales[ch_idx]
                channels_time.append(recon)

            combined_time = np.stack(channels_time, axis=1)

            
            # INVERSE PCA
            
            reconstructed = combined_time @ eigvecs.T + mean

            
            # ALIGN + METRICS
            
            min_len = min(len(data), len(reconstructed))
            data_eval = data[:min_len]
            reconstructed_eval = reconstructed[:min_len]

            snr = compute_snr(data_eval, reconstructed_eval)

            original_size = data_eval.nbytes
            compressed_size = len(compressed)
            cr = compute_compression_ratio(original_size, compressed_size)

            bitrate = (compressed_size * 8 * sr) / len(data_eval)
            num_channels = data_eval.shape[1] if data_eval.ndim > 1 else 1
            bitrate_per_channel = bitrate / num_channels

            
            # SAVE RECONSTRUCTED AUDIO
            
            reconstructed_preview = to_stereo_for_preview(reconstructed_eval)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_out:
                out_path = tmp_out.name
            save_audio(out_path, reconstructed_preview, sr)

        st.success("✅ Compression complete")

        
        # METRICS
       
        st.subheader("📊 Metrics")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("SNR (dB)", f"{snr:.2f}")
        m2.metric("Compression Ratio", f"{cr:.2f}")
        m3.metric("Bitrate (kbps)", f"{bitrate / 1000:.1f}")
        m4.metric("Per-channel bitrate (kbps)", f"{bitrate_per_channel / 1000:.1f}")

        
        # PLAYBACK COMPARISON
        
        st.subheader("🎧 Playback Comparison")
        a1, a2 = st.columns(2)

        with a1:
            st.write("**Original**")
            st.audio(sf_path)

        with a2:
            st.write("**Compressed / Reconstructed**")
            st.audio(out_path)

        
        # WAVEFORM COMPARISON
        
        st.subheader("📈 Waveform Comparison")
        wave_col1, wave_col2 = st.columns(2)

        with wave_col1:
            st.write("**Original**")
            st.line_chart(data_eval[:1000, 0])

        with wave_col2:
            st.write("**Reconstructed**")
            st.line_chart(reconstructed_eval[:1000, 0])

        
        # OPTIONAL SPECTROGRAM
        
        if show_spectrogram:
            st.subheader("📊 Spectrogram Comparison")
            spec_col1, spec_col2 = st.columns(2)

            orig_sig = data_eval[:, 0] if data_eval.ndim > 1 else data_eval
            recon_sig = (
                reconstructed_eval[:, 0]
                if reconstructed_eval.ndim > 1
                else reconstructed_eval
            )

            with spec_col1:
                render_spectrogram(orig_sig[:50000], sr, "Original Spectrogram")

            with spec_col2:
                render_spectrogram(recon_sig[:50000], sr, "Reconstructed Spectrogram")