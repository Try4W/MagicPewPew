import sys
sys.path.insert(0, '../FlatEngine/')
from keyboard import *
from screen_elements import ScreenLabel
from screen import Screen, ScreenObject, ScreenObjectModel
import info_screen

import client
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

__author__ = 'Alexandr'

keyboard_listener = None
screen = None
selected_button_id = None


class KeyboardControlListener(KeyboardListener):
    def on_key_pressed(self, key_code):
        if key_code == key_w:
            update_selected_button(True)
        if key_code == key_s:
            update_selected_button(False)
        if key_code == key_enter:
            if selected_button_id == -1:  # Host game
                Popen([executable, 'server.py'], creationflags=CREATE_NEW_CONSOLE)
            if selected_button_id == 0:  # Connect to
                Popen([executable, 'client.py'], creationflags=CREATE_NEW_CONSOLE)
            if selected_button_id == 1:  # Show screen with info
                destroy()
                info_screen.show()
            if selected_button_id == 2:  # Exit
                destroy()


def update_selected_button(up):
    min_button_id = -1
    max_button_id = 2
    global selected_button_id
    if selected_button_id == min_button_id and up or selected_button_id == max_button_id and not up:
        return
    if up:
        selected_button_id -= 1
    else:
        selected_button_id += 1


def get_button_string(button_id):
    if button_id == -1:
        if selected_button_id == -1:
            return "= Host ="
        return "Host"
    if button_id == 0:
        if selected_button_id == 0:
            return "= Connect to ="
        return "Connect to"
    if button_id == 1:
        if selected_button_id == 1:
            return "= Info ="
        return "Info"
    if button_id == 2:
        if selected_button_id == 2:
            return "= Exit Game ="
        return "Exit Game"


def show():
    world_size_x = 50
    world_size_y = 20

    global screen
    screen = Screen(world_size_x, world_size_y)
    global selected_button_id
    selected_button_id = 0

    logo_frames_map = {"DEFAULT": "models/logo.model"}
    logo_model = ScreenObjectModel(logo_frames_map)
    logo_model.set_current_frames("DEFAULT")
    logo_model.center_hor = True
    logo = ScreenObject(screen, logo_model)
    logo.pos_y = 10
    screen.add_object(logo)

    host_game_button = ScreenLabel(screen, lambda: get_button_string(-1))
    host_game_button.model.center_hor = True
    host_game_button.pos_y = 8
    screen.add_object(host_game_button)

    connect_to_button = ScreenLabel(screen, lambda: get_button_string(0))
    connect_to_button.model.center_hor = True
    connect_to_button.pos_y = 7
    screen.add_object(connect_to_button)

    exit_game_button = ScreenLabel(screen, lambda: get_button_string(1))
    exit_game_button.model.center_hor = True
    exit_game_button.pos_y = 6
    screen.add_object(exit_game_button)

    exit_game_button = ScreenLabel(screen, lambda: get_button_string(2))
    exit_game_button.model.center_hor = True
    exit_game_button.pos_y = 5
    screen.add_object(exit_game_button)

    global keyboard_listener
    keyboard_listener = KeyboardControlListener()
    keyboard_listener.start()


def destroy():
    screen.destroy()
    keyboard_listener.allow_listening = False


if __name__ == "__main__":
    show()
