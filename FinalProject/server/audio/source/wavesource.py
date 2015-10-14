import wave
from audio.source.audiostreamsource import AudioStreamSource

class WaveSource(AudioStreamSource):
    def __init__(self, filename):
        self.__source = wave.open(filename, 'rb')
        self.get_num_frames = lambda: self.__source.getnframes()
        self.get_num_stored_bytes = lambda: 0
        self.get_num_channels = lambda: self.__source.getnchannels()
        self.get_sample_width = lambda: self.__source.getsampwidth()
        self.get_sample_rate = lambda: self.__source.getframerate()
        self.read_frames = lambda n: self.__source.readframes(n)

