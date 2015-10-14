from os import path
from pydub import AudioSegment
from audio.source.audiostreamsource import AudioStreamSource

class FileSource(AudioStreamSource):
    def __init__(self, filename, fmt=None):
        if fmt is None:
            _, fmt = path.splitext(filename)
            fmt = fmt[1:]
        fmt = fmt.lower()
        self.__source = AudioSegment.from_file(filename, fmt)
        self.get_num_frames = lambda: self.__source.frame_count
        self.get_num_stored_bytes = lambda: 0
        self.get_num_channels = lambda: self.__source.channels
        self.get_sample_width = lambda: self.__source.sample_width
        self.get_sample_rate = lambda: self.__source.frame_rate
        self.__frame_number = 0
    def read_frames(self, num):
        end = min(self.__frame_number + num, int(self.__source.frame_count()))
        frame = b''.join(self.__source.get_frame(i) for i in range(self.__frame_number, end))
        self.__frame_number = end
        return frame

