# This IPC module is use to communicate with network process

import sysv_ipc
# from dotenv import load_dotenv
import os

# load_dotenv()

# class IPC assumes the role of interprocess communication
KEY = 199999


class IPC:
    def __init__(self) -> None:
        # self.key = os.getenv("IPC_KEY")

        self.messageQueue = sysv_ipc.MessageQueue(self.key, sysv_ipc.IPC_CREAT)
        self.mesg = None
        self.type_send = random()
        self.type_get = random()
    # The function @sendToNetwork is used to send a message to the network process

    def sendToNetwork(self, message: str) -> int:
        # +++ YOUR CODE HERE +++ #
        try:
            self.message_queue.send(message.encode(
                'utf-8'), block=False, type=self.type_send)
        except sysv_ipc.BusyError:
            pass

    # The function @receiveFromNetwork is used to receive a message from the network process
    def receiveFromNetwork(self,IO):
        # +++ YOUR CODE HERE +++ #
        try:
            self.mesg, mesg_type = self.message_queue.receive(
                block=False, type=self.type_get)
            self.mesg = self.decode_format()
        except sysv_ipc.BusyError:
            return False

    def decode_format(self):
        temp = self.mesg.decode('utf-8')
        return dict(tuple(key_value.split('=') for key_value in temp.split(',')))
