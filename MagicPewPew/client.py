import sys
sys.path.insert(0, '../FlatEngine/')

from keyboard import *
from screen import *
from screen_elements import ScreenLabel
import client_server_tools

import socket
import messager

import ctypes

__author__ = 'Alexandr'


# Life cycle
# - Request IP and port
# - Connect to server (if error - print it)
# - Get data packets in loop
# - Unpack json and put it on screen
# - Send pressed keys to server
# - Crash in any of strange situation :D


class ServerDataProcessor(threading.Thread):
    def __init__(self, connection, client):
        super().__init__()
        self.allow_processing = True
        self.connection = connection
        self.client = client

    def run(self):
        while self.allow_processing:
            try:
                json_data = messager.recv_msg(self.connection)
            except Exception as e:
                print(e)
                self.client.stop_client()
                sys.exit(1)
            server_objects = client_server_tools.unpack_patch(json_data)
            self.client.update_client_objects_from_server_objects(server_objects)


class KeyboardControlListener(KeyboardListener):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def on_key_pressed(self, key_code):
        messager.send_msg(self.connection, str(key_code))


class Client(object):
    def __init__(self, ip, port):
        self.client_objects = {}
        self.connection = socket.socket()
        connection_data = (ip, int(port))
        self.connection.connect(connection_data)

        self.keyboard_worker = KeyboardControlListener(self.connection)
        self.keyboard_worker.start()

        self.screen = Screen(50, 20)

        self.server_data_processor = ServerDataProcessor(self.connection, self)
        self.server_data_processor.start()

        self.is_working = True

        self.start_update_loop()

    def stop_client(self):
        self.screen.destroy()
        self.is_working = False
        self.keyboard_worker.allow_listening = False
        self.server_data_processor.allow_processing = False

    def start_update_loop(self):
        while self.is_working:
            self.screen.screen_objects = list(self.client_objects.values())
            # for client_object in list(self.client_objects.values()):
            #     if client_object not in self.screen.screen_objects:
            #         self.screen.add_object(client_object)

    def update_client_objects_from_server_objects(self, patch_objects):
        new_client_objects_dict = {}
        for uuid, patch_dict in patch_objects.items():
            # print(patch_dict)
            if uuid not in self.client_objects:
                self.client_objects[uuid] = client_server_tools.get_client_class_from_patch_class_name(
                    patch_dict[1])(self.screen)
                # print("New object from server")
                # ctypes.windll.user32.MessageBoxW(0, "UUID: " + str(uuid), "New player", 0)
            client_object = self.client_objects[uuid]
            client_object.update_dict(patch_dict[0])
            new_client_objects_dict[uuid] = client_object
        self.client_objects = new_client_objects_dict


def init():
    ip = input("Sever ip >>")
    port = input("Sever port >>")
    client = Client(ip, port)

if __name__ == "__main__":
    init()
