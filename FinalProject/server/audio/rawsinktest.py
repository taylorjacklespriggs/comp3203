from audio.sink.rawsink import RawSink
from audio.source.wavesource import WaveSource

from sys import argv

wsrc = WaveSource(argv[1])

rsnk = RawSink("output")
rsnk.change_state(wsrc.get_num_channels(), wsrc.get_sample_width(), wsrc.get_sample_rate())

while True:
    bts = wsrc.read_frames(256)
    if not len(bts):
        break
    rsnk.write_frames(bts)

rsnk.close()

