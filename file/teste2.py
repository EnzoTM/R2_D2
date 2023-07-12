import pyaudio
import numpy as np

p = pyaudio.PyAudio()

def play_sine_wave_on_device(device_index, frequency=440.0, duration=1.0):
    volume = 0.5     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*frequency/fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True,
                    output_device_index=device_index)

    # play
    stream.write(volume*samples)

    stream.stop_stream()
    stream.close()

# Now we'll iterate over all output devices and try to play a sine wave
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info["maxOutputChannels"] > 0:
        print(f"Playing sound on device {i}: {device_info['name']}")
        try:
            play_sine_wave_on_device(i)
        except Exception as e:
            print(f"Could not play sound on device {i}, error: {e}")

p.terminate()