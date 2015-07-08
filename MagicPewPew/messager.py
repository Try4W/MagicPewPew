import socket
import struct

__author__ = 'Alexandr'


def _send_msg(channel, message):
    try:
        channel.send(struct.pack("i", len(message)) + message.encode("utf-8"))
    except OSError as e:
        print(e)


def _recv_msg(channel):
    try:
        size = struct.unpack("i", channel.recv(struct.calcsize("i")))[0]
        data = ""
        while len(data) < size:
            msg = channel.recv(size - len(data))
            if not msg:
                return None
            data += msg.decode("utf-8")
        return data.strip()
    except OSError as e:
        print(e)


def send_msg(channel, message):
    channel.send(pack_data(message))


def recv_msg(channel):
    message_size = struct.unpack("i", channel.recv(4))[0]  # First four bytes
    return struct.unpack("%is" % message_size, channel.recv(message_size))[0].decode("utf-8")

def pack_data(data):
    data_len = len(data)
    return struct.pack("i%is" % data_len, data_len, data.encode("utf-8"))
