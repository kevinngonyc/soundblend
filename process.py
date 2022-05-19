import pyaudio
import numpy as np
from scipy import signal
from scipy import fft
import matplotlib.pyplot as plt
import time

RATE = 44100
CHUNK = 100
CHANNEL = 1

p = pyaudio.PyAudio()

player = p.open(format=pyaudio.paInt16, channels=CHANNEL, rate=RATE, output=True, frames_per_buffer=CHUNK)
stream = p.open(format=pyaudio.paInt16, channels=CHANNEL, rate=RATE, input=True, frames_per_buffer=CHUNK)

f = 441
t = np.linspace(0, 1, RATE)
saw = signal.sawtooth(2 * np.pi * f * t)
# saw_fft = fft.fft(saw)
chunkt = CHUNK/RATE

prev_time = time.time()
for i in range(int(RATE/CHUNK * 10)): #do this for 10 seconds
    c = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    c_fft = fft.fft(c)

    offset = int(i * CHUNK % (RATE/f))
    saw_chunk = saw[offset:offset+CHUNK]
    saw_fft = fft.fft(saw_chunk)

    out = fft.ifft(saw_fft * c_fft)
    player.write(out, CHUNK)
    # print("NEXT")
    # print(saw[offset])
    # print(saw[offset+CHUNK])
    # player.write(saw[offset:],CHUNK)
    
    

stream.stop_stream()
stream.close()
p.terminate()