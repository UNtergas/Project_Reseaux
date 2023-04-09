# This IPC module is use to communicate with network process
import socket
# import sysv_ipc
# from dotenv import load_dotenv
import os

# load_dotenv()

# class IPC assumes the role of interprocess communication


class IPC:
    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket

    def connectToNetwork(self):
        self.socket.connect("127.0.0.1", 12345)

    def sendToSocket(self, message: str) -> int:
        if self.socket != None:
            try:
                self.socket.sendall(("fr:Game "+message).encode('utf-8'))
            except BlockingIOError :
                pass

    def recvFromSocket(self):
        if self.socket != None:
            try:
                data = self.socket.recv(369369)
                if data is not None:
                    return data.decode('utf-8')
                return None
            except BlockingIOError:
                return None
