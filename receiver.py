import numpy as np
import pyaudio
import time
import os
from dotenv import load_dotenv
from encoding import encode
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

load_dotenv()
chunk=1024

sampling_rate = int(os.getenv("SAMPLING_RATE") or 44100)
duration = float(os.getenv("DURATION") or 0.5)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sampling_rate,
                input=True,
                input_device_index=2)

def listen(time):
    frames = []
    for i in range(0, int(sampling_rate / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)
    samples = frames_to_list(frames)
    return samples

def frames_to_list(frames):
    raw_data = b"".join(frames)
    samples = np.frombuffer(raw_data, dtype=np.int16)
    return samples.tolist()

def get_frequencies(samples, sampling_rate):
    # Convert to numpy array (if not already)
    samples = np.array(samples)
    
    # Apply FFT
    spectrum = np.fft.fft(samples)
    
    # Get corresponding frequency bins
    freqs = np.fft.fftfreq(len(samples), d=1/sampling_rate)
    
    # Take only the positive half (mirror of FFT)
    magnitude = np.abs(spectrum[:len(spectrum)//2])
    freqs = freqs[:len(freqs)//2]
    
    return freqs, magnitude


def plot_spectrogram(samples, sampling_rate):
    # Compute spectrogram
    samples = np.array(samples)
    f, t, Sxx = spectrogram(samples, fs=sampling_rate, nperseg=1024, noverlap=512)
    
    # Plot it
    plt.figure(figsize=(10, 5))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.title("Spectrogram")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [s]")
    plt.colorbar(label="Intensity [dB]")
    plt.ylim(0, 1000)  # Limit to human speech range
    plt.show()

a = listen(5)
plot_spectrogram(a, sampling_rate)

stream.stop_stream()
stream.close()
p.terminate()