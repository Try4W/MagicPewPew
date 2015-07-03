__author__ = 'Alexandr'


class _PlayAudio(object):
    """Play single audio file"""
    def __init__(self):
        try:
            self.impl = _PlayAudioWindows()
        except ImportError:
            self.impl = _PlayAudioUnix()

    def __call__(self, file_path):
        return self.impl(file_path)


class _PlayAudioWindows(object):
    def __init__(self):  # Check import
        import winsound
        import sys

    def __call__(self, file_path):
        import winsound
        import sys
        import _thread
        winsound.PlaySound(file_path, winsound.SND_FILENAME)

class _PlayAudioUnix(object):  # MAGIC. Need test
    def __init__(self):
        import wave
        import ossaudiodev

    def __call__(self, file_path):
        from wave import open as wave_open
        from ossaudiodev import open as oss_open
        s = wave_open(file_path,'rb')
        (nc, sw, fr, nf, comptype, compname) = s.getparams()
        dsp = oss_open('/dev/dsp','w')
        try:
            from ossaudiodev import AFMT_S16_NE
        except ImportError:
            if byteorder == "little":
                AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
            else:
                AFMT_S16_NE = ossaudiodev.AFMT_S16_BE
        dsp.setparameters(AFMT_S16_NE, nc, fr)
        data = s.readframes(nf)
        s.close()
        dsp.write(data)
        dsp.close()

play_audio_sync = _PlayAudio()

if __name__ == "__main__":
    print("Play test.wav...")
    play_audio_sync("test.wav")
    print("End of audio file")
