import sys
sys.path.insert(0, '../FlatEngine/')

import socket
import threading
import server_objects
import client_server_tools

import uuid

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
        while self.allow_work:
            data = self.player_connection.recv(1024)
            decoded_data = int(data.decode("utf-8"))
            self.player.input_queue.put(decoded_data)


class ClientsWaiter(threading.Thread):
    """ Wait for players and add they to world """
    def __init__(self, server_object):
        super().__init__()
        self.server = server_object
        self.allow_to_connect = True

    def run(self):
        while self.allow_to_connect:
            connection, address = self.server.server_socket.accept()
            self.server.connections[address] = connection
            player_object = server_objects.ServerPlayer()
            PlayerService(connection, player_object).start()
            self.server.add_object(player_object)
            self.server.players += 1


class Server(object):
    """ Main class of server """
    def __init__(self, ip, port):
        self.server_objects = {}
        self.connections = {}
        print("Binding socket...", end=" ")
        self.server_socket = socket.socket()
        print("Ok")
        bind_data = (ip, int(port))
        self.server_socket.bind(bind_data)
        self.server_socket.listen(4)
        print("Starting client waiter...", end=" ")
        self.client_waiter = ClientsWaiter(self)
        self.client_waiter.start()
        print("Ok")
        self.players = 0
        self.working = True

    def add_object(self, server_object):
        self.server_objects[uuid.uuid4()] = server_object

    def start_update_loop(self):
        """ Update every server object in main loop and then send object's data to players """
        while self.working:
            self.update_objects()
            json_data = self.generate_data_about_world()
            for address, connection in self.connections.items():
                connection.send(json_data.encode("utf-8"))

    def generate_data_about_world(self):
        """ Generate data from server objects """
        return client_server_tools.server_objects_to_json(self.server_objects)

    def update_objects(self):
        for server_object in self.server_objects:
            server_object.update()

    def stop(self):
        """ Disconnect every player from server, close all connections """
        for address, connection in self.connections.items():
            connection.close()


def init():
    ip = "localhost"  # input("Ip >> ")
    port = 11223  # input("Port >> ")
    global server_obj
    server_obj = Server(ip, port)
    server_objects.server_obj = server_obj

if __name__ == "__main__":
    print("= Standalone server")
    init()
