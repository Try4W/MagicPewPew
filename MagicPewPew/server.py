import sys
sys.path.insert(0, '../FlatEngine/')

import socket
import threading
import server_objects
import client_server_tools
import time

import uuid
import messager

__author__ = 'Alexandr'

# Life cycle
# - Start and ask for ip&port
# - Wait for client
# - Get pressed keys from clients
# - Process players movement and actions
# - Send data packets to all clients every tick

server_obj = None


class PlayerService(threading.Thread):
    """ Recv data and put keys codes into player object """
    def __init__(self, player_connection, player):
        super().__init__()
        self.player_connection = player_connection
        self.player = player
        self.allow_work = True

    def run(self):
        print("Starting player service")
        while self.allow_work:
            try:
                data = messager.recv_msg(self.player_connection)
            except ConnectionResetError as e:
                print("Some player disconnected")
                self.allow_work = False
                break
            decoded_data = int(data)
            # print("recv/input key: " + data)
            self.player.apply_pressed_key(decoded_data)


class ClientsWaiter(threading.Thread):
    """ Wait for players and add they to world """
    def __init__(self, server_object):
        super().__init__()
        self.server = server_object
        self.allow_to_connect = True

    def run(self):
        while self.allow_to_connect:
            connection, address = self.server.server_socket.accept()
            player_uuid = uuid.uuid4()
            print("New Player: " + str(address) + " uuid:" + str(player_uuid))
            self.server.connections[address] = connection
            player_object = server_objects.ServerPlayer()
            PlayerService(connection, player_object).start()
            print("Adding player object to world...")
            self.server.add_object(player_object, player_uuid)
            print("Updating players counter...")
            self.server.players += 1


class Server(object):
    """ Main class of server """
    def __init__(self, ip, port):
        self.server_objects = {}
        self.connections = {}

        print("Binding socket...")
        self.server_socket = socket.socket()
        bind_data = (ip, int(port))
        self.server_socket.bind(bind_data)
        self.server_socket.listen(4)

        print("Starting client waiter...")
        self.client_waiter = ClientsWaiter(self)
        self.client_waiter.start()

        self.players = 0
        self.working = True

        server_objects.server_obj = self

        self.start_update_loop()
        print("Exit main loop...")

    def add_object(self, server_object, obj_uuid=None):
        if obj_uuid is None:
            obj_uuid = uuid.uuid4()
        self.server_objects[obj_uuid] = server_object

    def remove_object(self, obj_to_remove):
        for iter_uuid in list(self.server_objects.keys()):
            if self.server_objects[iter_uuid] is obj_to_remove:
                print("Remove obj")
                del self.server_objects[iter_uuid]

    def start_update_loop(self):
        """ Update every server object in main loop and then send object's data to players """
        while self.working:
            self.update_objects()
            json_data_to_send = client_server_tools.pack_patch(self.server_objects)
            # print("Send loop... ")
            for address, connection in self.connections.items():
                messager.send_msg(connection, json_data_to_send)
            time.sleep(0.2)

    def update_objects(self):
        for server_object in list(self.server_objects.values()):
            server_object.update()

    def stop(self):
        """ Disconnect every player from server, close all connections """
        for address, connection in self.connections.items():
            connection.close()


def init():
    ip = input("Ip >> ")
    port = input("Port >> ")
    global server_obj
    server_obj = Server(ip, port)

if __name__ == "__main__":
    print("= Standalone server")
    init()
