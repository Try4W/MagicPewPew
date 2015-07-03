import sys
sys.path.insert(0, '../FlatEngine/')
from keyboard import *
from screen_elements import ScreenLabel
from screen import Screen, ScreenObject, ScreenObjectModel
import menu_screen

__author__ = 'Alexandr'

keyboard_listener = None
screen = None


class KeyboardControlListener(KeyboardListener):
    def on_key_pressed(self, key_code):
        if key_code == key_enter:
            destroy()
            menu_screen.show()


def show():
    world_size_x = 50
    world_size_y = 20

    global screen
    screen = Screen(world_size_x, world_size_y)

    screen_title = ScreenLabel(screen, lambda: "* Info *")
    screen_title.model.center_hor = True
    screen_title.pos_y = 15
    screen.add_object(screen_title)

    author_label = ScreenLabel(screen, lambda: "Author: Alexandr aka Try4W")
    author_label.model.center_hor = True
    author_label.pos_y = 12
    screen.add_object(author_label)

    email_label = ScreenLabel(screen, lambda: "Email: alexandr2levin@gmail.com")
    email_label.model.center_hor = True
    email_label.pos_y = 11
    screen.add_object(email_label)

    help_to_exit = ScreenLabel(screen, lambda: "Press enter to return")
    help_to_exit.model.center_hor = True
    help_to_exit.pos_y = 8
    screen.add_object(help_to_exit)

    global keyboard_listener
    keyboard_listener = KeyboardControlListener()
    keyboard_listener.start()


def destroy():
    screen.destroy()
    keyboard_listener.allow_listening = False
