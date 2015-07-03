import sys
sys.path.insert(0, '../FlatEngine/')

from keyboard import *
from audio import play_audio_async
from model_tools import generate_frames_from_string
from screen import *
from screen_elements import ScreenLabel
import types
import time

__author__ = 'Alexandr'


class KeyboardControlListener(KeyboardListener):
    def on_key_pressed(self, key_code):
        if key_code == key_w:
            player.pos_y += 1
            player_model.set_current_frames("UP")
        if key_code == key_a:
            player.pos_x -= 1
            player_model.set_current_frames("LEFT")
        if key_code == key_d:
            player.pos_x += 1
            player_model.set_current_frames("RIGHT")
        if key_code == key_s:
            player.pos_y -= 1
            player_model.set_current_frames("DOWN")

world_size_x = 50
world_size_y = 20

screen = Screen(world_size_x, world_size_y)

player_frames_map = {"UP": "demo_models/player_up.model",
                     "LEFT": "demo_models/player_left.model",
                     "RIGHT": "demo_models/player_right.model",
                     "DOWN": "demo_models/player_down.model"}
player_model = ScreenObjectModel(player_frames_map)
player_model.set_current_frames("UP")

player = ScreenObject(screen, player_model)
screen.add_object(player)

fps_counter = ScreenLabel(screen, lambda: "FPS: " + str(screen.screen_renderer.fps))
fps_counter.pos_y = world_size_y - 1
screen.add_object(fps_counter)

keyboard_listener = KeyboardControlListener()
keyboard_listener.start()
