import json
import server_objects
import client_objects
import ast

__author__ = 'Alexandr'


client_objects_names = {"ServerPlayer": client_objects.Player,
                        "ServerFireball": client_objects.Fireball}


def pack_patch(server_objects_dict):
    res = {}
    for uuid, server_object in server_objects_dict.items():
        res[str(uuid)] = server_object.to_json()
    return json.dumps(res)


def unpack_patch(json_data):
    # print(json_data)
    server_objects_dict = json.loads(json_data)
    res = {}
    for uuid, json_server_objects_dict in server_objects_dict.items():
        object_name, json_server_object = json_server_objects_dict.split(":", maxsplit=1)
        # print(json_server_object)
        res[uuid] = [ast.literal_eval(json_server_object), object_name]
    return res


def get_client_class_from_patch_class_name(class_name):
    return client_objects_names[class_name]
