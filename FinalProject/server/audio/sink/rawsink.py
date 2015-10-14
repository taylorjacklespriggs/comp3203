from audio.sink.audiostreamsink import AudioStreamSink

class RawSink(AudioStreamSink):
    def __init__(self, name):
        self.__name = name
        self.__file = open("%s.raw"%name, 'wb+')
    def change_state(self, channels, sample_width, sample_rate):
        f = open("%s.md"%self.__name, 'w+')
        f.write("num_channels %d\nsample_width %d\nsample_rate %d\n"%(channels, sample_width, sample_rate))
        f.close()
    def write_frames(self, frame):
        self.__file.write(frame)
    def close(self):
        self.__file.close()

