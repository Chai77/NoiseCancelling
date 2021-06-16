import pyaudio
import numpy as np
import struct
import matplotlib.pyplot as plt
 


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024*4
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recordedFile.wav"
device_index = 2
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True, output=True,
                frames_per_buffer=CHUNK)
print ("recording started")

Recordframes = []

print("Record Time: ", RATE / CHUNK * RECORD_SECONDS)

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    Recordframes.append(data)

data_int = np.array(struct.unpack(str(CHUNK * 2) + 'B', data), dtype='b')[::2]+127
n = len(data_int)

data_hat = np.fft.fft(data_int, n)
PSD = data_hat * np.conj(data_hat) / n

BUFFER_AMOUNT = 100
indices = PSD > BUFFER_AMOUNT

PSD_clean = PSD * indices
data_hat = data_hat * indices

filtered_data = np.fft.ifft(data_hat)
cancelling_data = -1 * filtered_data

final_wave = data_int + cancelling_data

# matplot

t = np.arange(0, 1, 1/n)

print(data_int)

plt.plot(t, final_wave, 'ro')
plt.axis([0, 1, 0, 255])
plt.show()