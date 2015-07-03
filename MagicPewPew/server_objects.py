import sys
sys.path.insert(0, '../FlatEngine/')

from keyboard import *
import copy
from queue import Queue

__author__ = 'Alexandr'

server_obj = None

class ServerObject(object):
    def __init__(self, size_x, size_y):
        self.pos_x = 0
        self.pos_y = 0
        self.size_x = size_x
        self.size_y = size_y

    def update(self):
        pass

    def update_dict(self, dict_patch):
        for key, value in dict_patch.items():
            setattr(self, key, value)


class ServerPlayer(ServerObject):
    def __init__(self):
        super().__init__(4, 3)
        self.look_direction = 0  # up(0) left(1) right(2) down(3)
        self.input_queue = Queue(1000)

    def update(self):
        for input_key in iter(self.input_queue.get, self.input_queue.qsize()):
            if input_key == key_w:
                self.pos_y += 1
                self.look_direction = 0
                return
            if input_key == key_a:
                self.pos_x -= 1
                self.look_direction = 1
                return
            if input_key == key_d:
                self.pos_x += 1
                self.look_direction = 2
                return
            if input_key == key_s:
                self.pos_y -= 1
                self.look_direction = 3
                return
            if input_key == key_space:
                self.shoot_fireball()
                return

        self.input_queue.task_done()

    def shoot_fireball(self):
        """ Spawn fireball in front of player """
        spawn_pos_x = 0
        spawn_pos_y = 0
        if self.look_direction == 0:
            spawn_pos_x = self.pos_x + 1
            spawn_pos_y = self.pos_y + self.size_y + 2
        if self.look_direction == 1:
            spawn_pos_x = self.pos_x - 2
            spawn_pos_y = self.pos_y + 1
        if self.look_direction == 2:
            spawn_pos_x = self.pos_x + self.size_x + 2
            spawn_pos_y = self.pos_y + 1
        if self.look_direction == 3:
            spawn_pos_x = self.pos_x + 1
            spawn_pos_y = self.pos_y - 2
        server_obj.add_object(ServerFireball(self.look_direction, spawn_pos_x, spawn_pos_y))

    def to_json(self):
        tmp_dict = copy.copy(self.__dict__)
        del tmp_dict["input_queue"]
        return self.__class__.__name__ + ":" + str(tmp_dict)


class ServerFireball(ServerObject):
    def __init__(self, pos_x=0, pos_y=0, fly_direction=0):
        super().__init__(1, 1)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.fly_direction = fly_direction

    def update(self):
        if self.fly_direction == 0:
            self.pos_y += 1
        if self.fly_direction == 1:
            self.pos_x -= 1
        if self.fly_direction == 2:
            self.pos_x += 1
        if self.fly_direction == 3:
            self.pos_y -= 1

        # TODO: Process hits

    def to_json(self):
        tmp_dict = copy.copy(self.__dict__)
        del tmp_dict["fly_direction"]
        return self.__class__.__name__ + ":" + str(tmp_dict)

if __name__ == "__main__":
    a = ServerPlayer()
    b = ServerFireball(0, 0, 0)
    print("# Object -> json test")
    print(a.to_json())
    print(a.to_json())
    print(b.to_json())
    print(b.to_json())

    import client_server_tools
    print("# dict{uuid: obj} -> json test")
    demo_server_object = {"uuid1": a,
                          "uuid2": b}
    server_objects_json_demo = client_server_tools.server_objects_to_json(demo_server_object)
    print(server_objects_json_demo)

    print("# json -> dict(uuid: obj) test")
    server_objects_demo = client_server_tools.json_to_server_objects(server_objects_json_demo)
    print(server_objects_demo)

    # import client_objects
    # print("# server_objects -patch-> client_objects")
    # client_objects_demo = {"uuid1": client_objects.Player(None, None), "uuid2": client_objects.Fireball(0)}
    # client_server_tools.update_client_objects_server_objects(client_objects_demo, server_objects_demo)
    # print(client_objects_demo)
