# This IPC module is use to communicate with network process

import sysv_ipc
from dotenv import load_dotenv
import os

load_dotenv()

# class IPC assumes the role of interprocess communication
class IPC:
    def __init__(self) -> None:
          self.key = os.getenv("IPC_KEY")
          self.messageQueue = sysv_ipc.MessageQueue(self.key, sysv_ipc.IPC_CREAT)
          
    # The function @sendToNetwork is used to send a message to the network process 
    def sendToNetwork(self, message: str) -> int:
        # +++ YOUR CODE HERE +++ #
        pass

    # The function @receiveFromNetwork is used to receive a message from the network process
    def receiveFromNetwork(self,IO):
        # +++ YOUR CODE HERE +++ #
        #IO.inputStack.append(str)
        pass

    def processMessage(self):
        pass
