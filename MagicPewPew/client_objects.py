import sys
sys.path.insert(0, '../../FlatEngine/')

from keyboard import *
from screen import *
from screen_elements import ScreenObject
import model_tools

__author__ = 'Alexandr'

player_frames_map = {"UP": model_tools.load_frames("models/player_up.model"),
                     "LEFT": model_tools.load_frames("models/player_left.model"),
                     "RIGHT": model_tools.load_frames("models/player_right.model"),
                     "DOWN": model_tools.load_frames("models/player_down.model")}

fireball_frames_map = {"DEFAULT": model_tools.load_frames("models/fireball.model")}


class ClientObject(object):
    def update_dict(self, dict_patch):
        for key, value in dict_patch.items():
            setattr(self, key, value)


class Player(ScreenObject, ClientObject):
    def __init__(self, screen):
        super().__init__(screen, ScreenObjectModel(player_frames_map, raw=False))  # set model
        self.model.set_current_frames("UP")
        self.look_direction = 0

    def update(self):
        if self.look_direction == 0:
            self.model.set_current_frames("UP")
        if self.look_direction == 1:
            self.model.set_current_frames("LEFT")
        if self.look_direction == 2:
            self.model.set_current_frames("RIGHT")
        if self.look_direction == 3:
            self.model.set_current_frames("DOWN")


class Fireball(ScreenObject, ClientObject):
    def __init__(self, screen):
        super().__init__(screen, ScreenObjectModel(fireball_frames_map, raw=False))  # set model
        self.model.set_current_frames("DEFAULT")
