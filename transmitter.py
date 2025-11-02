import numpy as np
import pyaudio
import time
import os
from dotenv import load_dotenv
from encoding import encode

load_dotenv()

sampling_rate = int(os.getenv("SAMPLING_RATE") or 44100)
duration = float(os.getenv("DURATION") or 0.5)

def bytestring_to_audio(bytestring: str):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sampling_rate,
                    output=True)
    
    for bit in bytestring:
        frequency = 440.0 if int(bit) == 1 else 0

        # Generate sine wave data
        t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
        amplitude = np.sin(2 * np.pi * frequency * t)

        # Convert to 16-bit integer format
        audio_data = (amplitude * 32767).astype(np.int16).tobytes()

        # Play the sound
        stream.write(audio_data)


    # Clean up
    if stream:
        stream.stop_stream()
        stream.close()
        p.terminate()

def transmit(message: str):
    message_bytes = encode(message)
    bytestring_to_audio("10101011"+message_bytes+"11101001" )

transmit("Hello")