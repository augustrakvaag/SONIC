import sounddevice as sd
print(sd.query_devices())
sd.rec(int(3 * 44100), samplerate=44100, channels=1)