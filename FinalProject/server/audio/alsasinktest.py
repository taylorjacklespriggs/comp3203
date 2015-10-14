from audio.sink.alsasink import AlsaSink
from audio.source.wavesource import WaveSource

from sys import argv

wsrc = WaveSource(argv[1])

asnk = AlsaSink()
asnk.change_state(wsrc.get_num_channels(), wsrc.get_sample_width(), wsrc.get_sample_rate())

while True:
    bts = wsrc.read_frames(256)
    if not len(bts):
        break
    asnk.write_frames(bts)


