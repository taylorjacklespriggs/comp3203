import sys
import alsaaudio
from audio.sink.audiostreamsink import AudioStreamSink

class AlsaSink(AudioStreamSink):
    def __init__(self, card=None):
        self.__device = alsaaudio.PCM(card=card) if card is not None else alsaaudio.PCM()
        self.__forms = { \
                1: alsaaudio.PCM_FORMAT_S8, \
                2: alsaaudio.PCM_FORMAT_S16_LE, \
                3: alsaaudio.PCM_FORMAT_S24_LE, \
                4: alsaaudio.PCM_FORMAT_S32_LE }
        self.__period_size = 1024
        self.__frame_width = None
    def change_state(self, channels, sample_width, sample_rate):
        self.__device.setrate(sample_rate)
        self.__device.setchannels(channels)
        self.__device.setformat(self.__forms[sample_width])
        self.__device.setperiodsize(self.__period_size)
    def write_frames(self, frames):
        self.__device.write(frames)

