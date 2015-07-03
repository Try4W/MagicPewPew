import sys
sys.path.insert(0, '../ConsoleInputEngine/')

from py_input import getch
import threading


__author__ = 'Alexandr'

key_esc = 27
key_enter = 13

key_w = 119
key_a = 97
key_s = 115
key_d = 100

key_arrow_up = 72
key_arrow_left = 75
key_arrow_right = 77
key_arrow_down = 80

key_space = 32


class KeyboardListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.allow_listening = True

    def run(self):
        while self.allow_listening:
            self.on_key_pressed(ord(getch()))

    def on_key_pressed(self, key_code):
        pass


class _KeyboardDemoListener(KeyboardListener):
    def on_key_pressed(self, key_code):
        if key_code == key_esc:
            sys.exit(0)
        print("Code of key that was pressed: " + str(key_code))


if __name__ == "__main__":
    print("Press any key to get code of it\n"
          "Press ESCAPE to exit\n"
          "Code of ESCAPE-key is " + str(key_esc) + " :)\n"
          "# ----")
    demo_listener = _KeyboardDemoListener()
    demo_listener.start()
