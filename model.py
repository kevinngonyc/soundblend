from pytz import NonExistentTimeError
import librosa
import sounddevice as sd
import soundfile as sf
import statsmodels.api as sm
from scipy import signal
import numpy as np
from hampel import hampel
import pandas as pd
import  matplotlib.pyplot  as plt

class Model:
    def __init__(self):
        self.is_playing = False
        self.y = None
        self.z = None
        self.sr = 22050
        self.channels = 1
        self.chunk = 512
        self.note_freqs = self.getNoteFreqs()
        self.minf = librosa.note_to_hz('C2')
        self.maxf = librosa.note_to_hz('C7')
        self.osc_options = ["saw", "sine", "square", "triangle"]

    def getNoteFreqs(self):
        notes = ["C", "D", "E", "F", "G", "A", "B"]
        note_freqs = []
        for i in range(2, 7):
            for n in notes:
                freq = librosa.note_to_hz(n + str(i))
                note_freqs.append(freq)
        return np.array(note_freqs)

    def play(self):
        if self.z is not None:
            sd.play(self.z, self.sr)
        else:
            sd.play(self.y, self.sr)
    
    def stop(self):
        sd.stop()

    def loadFile(self, filename):
        self.y, self.sr = librosa.load(filename)
        self.z = None

    def acPitchTracking(self):
        pitches = []
        for i in range(self.chunk, len(self.y), self.chunk):
            auto = sm.tsa.acf(self.y[i-self.chunk:i], nlags=self.sr//20)
            peaks = signal.find_peaks(auto, prominence=1)[0]
            pitch = 0
            if len(peaks) > 0:
                lag = peaks[0]
                pitch = self.sr / lag
            if pitch >= self.minf and pitch < self.maxf:
                pitches.append(pitch)
            else:
                pitches.append(0)
        return np.array(pitches)
    
    def quantizePitches(self, pitches):
        pq = [0]
        for pitch in pitches:
            i = (np.abs(self.note_freqs - pitch)).argmin()
            pq.append(self.note_freqs[i])
        return pq

    def getFullPitches(self, pitches):
        pitches_smooth = hampel(pd.Series(pitches), window_size=5, n=3, imputation=True)
        fp =  []
        for pitch in pitches_smooth:
            fp += [pitch] * self.chunk
        return np.array(fp[:len(self.y)])

    def generateOsc(self, pitches_full):
        osc = np.zeros(len(self.y))
        for type, level in zip(self.osc_types, self.osc_levels):
            t = np.linspace(0, len(self.y)//self.sr, len(self.y))
            p = 2 * np.pi * pitches_full * t
            if type == "saw":
                osc += level / 100 * signal.sawtooth(p)
            elif type == "sine":
                osc += level / 100 * np.sin(p)
            elif type == "square":
                osc += level / 100 * signal.square(p)
            elif type == "triangle":
                osc += level / 100 * signal.sawtooth(p, width=0.5)
        return osc

    def vox(self):
        fp = self.getFullPitches(self.quantizePitches(self.acPitchTracking()))
        osc = self.generateOsc(fp)
        _, _, yZxx = signal.stft(self.y)
        _, _, oscZxx = signal.stft(osc)
        _, outx = signal.istft(yZxx * oscZxx)
        self.z = outx / np.max(np.abs(outx))