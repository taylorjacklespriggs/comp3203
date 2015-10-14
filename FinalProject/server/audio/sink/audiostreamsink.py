
class AudioStreamSink:
    def change_state(self, channels, sample_width, sample_rate):
        '''
        Changes the state of the sink
        '''
        raise NotImplementedError('Abstract method: change_state')
    def write_frames(self, bts):
        '''
        Writes out the frames
        '''
        raise NotImplementedError('Abstract method: write_frames')

