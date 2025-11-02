import numpy as np
import pyaudio
import time
from encoding import encode

SAMPLING_RATE: int = 44100  # samples per second
DURATION: float = 0.5         # seconds


def bytestring_to_audio(bytestring: str):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLING_RATE,
                    output=True)
    
    for bit in bytestring:
        time.sleep(0.1)
        FREQUENCY = 440.0 if int(bit) == 0 else 256.0

        # Generate sine wave data
        t = np.linspace(0, DURATION, int(SAMPLING_RATE * DURATION), endpoint=False)
        amplitude = np.sin(2 * np.pi * FREQUENCY * t)

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
    bytestring_to_audio(message_bytes)

transmit("Hello")