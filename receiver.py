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
                input_device_index=1)

def listen(time):
    frames = []
    print("Listening...")
    for i in range(0, int(sampling_rate / chunk * time)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording done")
    samples = frames_to_array(frames)
    return samples

def frames_to_array(frames):
    raw_data = b"".join(frames)
    samples = np.frombuffer(raw_data, dtype=np.int16)
    return samples.tolist()

def goertzel_power(samples, target_freq, sampling_rate):
    """
    Return the power of target_freq in the given samples using Goertzel.
    """
    n = len(samples)
    k = int(0.5 + (n * target_freq) / sampling_rate)  # nearest bin
    w = 2.0 * np.pi * k / n
    coef = 2.0 * np.cos(w)

    s_prev = 0.0
    s_prev2 = 0.0
    for x in samples:
        s = x + coef * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    # power
    power = s_prev2**2 + s_prev**2 - coef * s_prev * s_prev2
    return power

def decode_frequency(samples, sampling_rate, frequency, threshold=None):
    samples_per_bit = int(sampling_rate * duration)
    num_bits = len(samples) // samples_per_bit
    bits = []
    powers = []
    for i in range(num_bits):
        start = i * samples_per_bit
        end = start + samples_per_bit
        chunk = samples[start:end]

        window = np.hanning(len(chunk))
        chunk = chunk * window

        power = goertzel_power(chunk, frequency, sampling_rate)
        powers.append(power)
    
    if threshold is None:
        mn = np.min(powers)
        mx = np.max(powers)
        threshold = (mn + mx) / 2
    
    for power in powers:
        bit = 1 if power > threshold else 0
        bits.append(bit)
    return bits, powers, threshold

def main(time):
    print(f"Listening {time} seconds...")
    samples = listen(time)

    bits, powers, thr = decode_frequency(samples, sampling_rate, 440.0)

    print("powers:", powers)
    print("auto threshold:", thr)
    print("decoded bits:", bits)

    stream.stop_stream()
    stream.close()
    p.terminate()

main(10)