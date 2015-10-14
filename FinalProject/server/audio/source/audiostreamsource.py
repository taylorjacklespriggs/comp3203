
class AudioStreamSource:
    def get_num_frames(self):
        '''
        Returns the number of audio frames in the stream source
        '''
        raise NotImplementedError('Abstract method: get_num_frames')
    def get_num_stored_bytes(self):
        '''
        Returns the RAM impact of the stream
        '''
        raise NotImplementedError('Abstract method: get_num_stored_bytes')
    def get_num_channels(self):
        '''
        Returns the number of audio channels for the source
        '''
        raise NotImplementedError('Abstract method: get_num_channels')
    def get_sample_width(self):
        '''
        Returns the sample rate of the source in hertz
        '''
        raise NotImplementedError('Abstract method: get_sample_width')
    def get_sample_rate(self):
        '''
        Returns the sample rate of the source in hertz
        '''
        raise NotImplementedError('Abstract method: get_sample_rate')
    def read_frames(self, n):
        '''
        Returns at most the number of frames requested, as bytes
        '''
        raise NotImplementedError('Abstract method: read_frames')

