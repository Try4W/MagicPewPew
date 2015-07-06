import sys

sys.path.insert(0, '../FlatEngine/')

from keyboard import *
import copy
import queue

__author__ = 'Alexandr'

server_obj = None

world_size_x = 50
world_size_y = 20


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

    def apply_pressed_key(self, input_key):
        # print("update/input key: " + str(input_key))
        # if self.pos_x < world_size_x and self.pos_y < world_size_y:
        # if self.pos_x >= 0 and self.pos_x >= 0:
        if input_key == key_w and self.pos_y < world_size_y - self.size_y:
            self.pos_y += 1
            self.look_direction = 0
            return
        if input_key == key_a and self.pos_x > 0:
            self.pos_x -= 1
            self.look_direction = 1
            return
        if input_key == key_d and self.pos_x < world_size_x - self.size_x:
            self.pos_x += 1
            self.look_direction = 2
            return
        if input_key == key_s and self.pos_y > 0:
            self.pos_y -= 1
            self.look_direction = 3
            return
        if input_key == key_space:
            self.shoot_fireball()
            return

    def kill(self):
        print("Object has killed!")
        self.pos_x = 0
        self.pos_y = 0

    def update(self):
        pass

    def shoot_fireball(self):
        """ Spawn fireball in front of player """
        print("spawn fireball")
        spawn_pos_x = 0
        spawn_pos_y = 0
        if self.look_direction == 0:
            print("Shoot up")
            spawn_pos_x = self.pos_x + 1
            spawn_pos_y = self.pos_y + self.size_y + 2
        if self.look_direction == 1:
            print("Shoot at left")
            spawn_pos_x = self.pos_x - 2
            spawn_pos_y = self.pos_y + 1
        if self.look_direction == 2:
            print("Shoot at right")
            spawn_pos_x = self.pos_x + self.size_x + 2
            spawn_pos_y = self.pos_y + 1
        if self.look_direction == 3:
            print("Shoot down")
            spawn_pos_x = self.pos_x + 1
            spawn_pos_y = self.pos_y - 2
        server_obj.add_object(ServerFireball(spawn_pos_x, spawn_pos_y, self.look_direction))

    def to_json(self):
        tmp_dict = copy.copy(self.__dict__)
        # del tmp_dict["input_queue"]
        return self.__class__.__name__ + ":" + str(tmp_dict)


class ServerFireball(ServerObject):
    def __init__(self, pos_x=0, pos_y=0, fly_direction=0):
        super().__init__(1, 1)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.fly_direction = fly_direction

    def update(self):
        if (self.pos_x < world_size_x and self.pos_y < world_size_y) \
                and (self.pos_x >= 0 and self.pos_y >= 0):  # Check is object on the screen
            if self.fly_direction == 0:
                self.pos_y += 1
            elif self.fly_direction == 1:
                self.pos_x -= 1
            elif self.fly_direction == 2:
                self.pos_x += 1
            elif self.fly_direction == 3:
                self.pos_y -= 1
        else:
            server_obj.remove_object(self)

        for other_obj in list(server_obj.server_objects.values()):
            # print("check collision")
            if self.pos_x < other_obj.pos_x + other_obj.size_x and\
                    self.pos_x + self.size_x > other_obj.pos_x and\
                    self.pos_y < other_obj.pos_y + other_obj.size_y and\
                    self.size_y + self.pos_y > other_obj.pos_y:
                if hasattr(other_obj, "kill"):
                    other_obj.kill()

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
    server_objects_json_demo = client_server_tools.pack_patch(demo_server_object)
    print(server_objects_json_demo)

    print("# json -> dict(uuid: obj) test")
    server_objects_demo = client_server_tools.unpack_patch(server_objects_json_demo)
    print(server_objects_demo)

    # import client_objects
    # print("# server_objects -patch-> client_objects")
    # client_objects_demo = {"uuid1": client_objects.Player(None, None), "uuid2": client_objects.Fireball(0)}
    # client_server_tools.update_client_objects_server_objects(client_objects_demo, server_objects_demo)
    # print(client_objects_demo)
