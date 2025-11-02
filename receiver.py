import numpy as np
import pyaudio
import time
import os
from dotenv import load_dotenv
from encoding import encode

load_dotenv()
chunk=1024

sampling_rate = int(os.getenv("SAMPLING_RATE") or 44100)
duration = float(os.getenv("DURATION") or 0.5)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sampling_rate,
                input=True)

def listen(time):
    data = stream.read(chunk)
