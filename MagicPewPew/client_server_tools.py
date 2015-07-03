import json
import server_objects
import client_objects

__author__ = 'Alexandr'


server_objects_names = {"ServerPlayer": server_objects.ServerPlayer,
                        "ServerFireball": server_objects.ServerFireball}


client_objects_names = {"ServerPlayer": client_objects.Player,
                        "ServerFireball": client_objects.Fireball}


def server_objects_to_json(server_objects_dict):
    res = {}
    for uuid, server_object in server_objects_dict.items():
        res[uuid] = server_object.to_json()
    return json.dumps(res)


def json_to_server_objects(json_data):
    server_objects_dict = json.loads(json_data)
    res = {}
    for uuid, json_server_objects_dict in server_objects_dict.items():
        object_name, json_server_object = json_server_objects_dict.split(":", maxsplit=1)
        server_object = get_server_class_from_name(object_name)()
        server_object.update_dict(server_object.__dict__)
        res[uuid] = server_object
    return res


def get_server_class_from_name(class_name):
    return server_objects_names[class_name]


def get_client_class_from_server_class_name(class_name):
    return client_objects_names[class_name]
