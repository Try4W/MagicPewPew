import sys
sys.path.insert(0, '../../FlatEngine/')

from keyboard import *
from screen import *
from screen_elements import ScreenObject
import model_tools

__author__ = 'Alexandr'

# TODO: For why?
player_frames_map = {"UP": model_tools.load_frames("models/player_up.model"),
                     "LEFT": model_tools.load_frames("models/player_left.model"),
                     "RIGHT": model_tools.load_frames("models/player_right.model"),
                     "DOWN": model_tools.load_frames("models/player_down.model")}

class ClientObject(object):
    def update_dict(self, dict_patch):
        for key, value in dict_patch.items():
            setattr(self, key, value)

class Player(ScreenObject, ClientObject):
    def __init__(self, screen):
        super().__init__(screen, ScreenObjectModel(player_frames_map))  # set model


class Fireball(ScreenObject, ClientObject):
    def __init__(self, screen):
        super().__init__(screen, ScreenObjectModel(player_frames_map))  # set model
