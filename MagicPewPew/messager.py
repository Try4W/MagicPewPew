import socket
import struct

__author__ = 'Someone from the internet'

def send_msg(channel, message):
    try:
        channel.send(struct.pack("i", len(message)) + message.encode("utf-8"))
    except OSError as e:
        print(e)

def recv_msg(channel):
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
