from pytz import NonExistentTimeError
import librosa
import sounddevice as sd
import soundfile as sf

class Model:
    def __init__(self):
        self.recpath = "samples/rec.wav"
        self.record_time = 15
        self.is_recording = False
        self.is_playing = False
        self.y = None
        self.sr = 22050
        self.channels = 1
        self.chunk = 512

    def play(self):
        sd.play(self.y, self.sr)
    
    def stop(self):
        sd.stop()

    def record(self):
        self.y = sd.rec(self.record_time, samplerate=self.sr, channels=self.channels)
        sf.write(self.recpath, self.y, self.sr)

    def updateOsc(self, types, levels):
        pass

    def loadFile(self, filename):
        self.y, self.sr = librosa.load(filename)