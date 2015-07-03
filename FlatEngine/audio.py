import sys
sys.path.insert(0, '../ConsoleAudioEngine/')

from py_audio import play_audio_sync
import _thread

__author__ = 'Alexandr'

def play_audio_async(path_to_audio_file):
    _thread.start_new_thread(play_audio_sync, path_to_audio_file)

