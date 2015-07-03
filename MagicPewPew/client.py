import sys
sys.path.insert(0, '../FlatEngine/')

from keyboard import *
from screen import *
from screen_elements import ScreenLabel
import client_server_tools

import socket

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
            bytes_json_data = self.connection.recv(1024)
            json_data = bytes_json_data.decode("utf-8")
            server_objects = client_server_tools.json_to_server_objects(json_data)
            self.client.update_client_objects_from_server_objects(server_objects)


class KeyboardControlListener(KeyboardListener):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def on_key_pressed(self, key_code):
        self.connection.send(str(key_code).encode("utf-8"))


class Client(object):
    def __init__(self, ip, port):
        self.client_objects = {}
        self.connection = socket.socket()
        connection_data = (ip, int(port))
        self.connection.connect(connection_data)

        self.keyboard_worker = KeyboardControlListener(self.connection)
        self.keyboard_worker.start()

        self.server_data_processor = ServerDataProcessor(self.connection, self)
        self.server_data_processor.start()

        self.screen = Screen(50, 20)
        self.is_working = True

        self.start_update_loop()

    def start_update_loop(self):
        while self.is_working:
            for client_object in self.client_objects:
                if client_object not in self.screen.screen_objects:
                    self.screen.add_object(client_object)

    def update_client_objects_from_server_objects(self, server_objects_patch):
        for uuid, server_object in server_objects_patch.items():
            if uuid not in self.client_objects:
                self.client_objects = client_server_tools.get_client_class_from_server_class_name(
                    server_object.__class__.__name__)(self.screen)
            client_object = self.client_objects[uuid]
            client_object.update_dict(server_object.__dict__)


def init():
    ip = "localhost"  # input("Sever ip >>")
    port = 11223  # input("Sever port >>")
    client = Client(ip, port)

if __name__ == "__main__":
    init()
