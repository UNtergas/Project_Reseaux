import socket
from const import SERVER_ADDRESS, SERVER_PORT
import subprocess
import errno
import time
# from Presentation import GameIO as IO

# The function @getAvailableRoom is used to get the available rooms from network module
# @parameters: {
#   None
# }
#

executablePath = "./../../executable/"


def getAvailableRoom():

    def strToRoomIn4(rawStr: str):
        arr = rawStr.split(": ")
        return {
            "roomName": arr[0],
            "hostIP": arr[1]
        }

    result = subprocess.run(
        [executablePath+'getAvailableRoom'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').split('\n')
    result.pop()
    rooms = None
    if result != None:
        rooms = list(map(strToRoomIn4, result))

    return rooms


def createRoom(roomName: str, hostName: str):
    process = subprocess.Popen([executablePath+'app', '1', roomName,
                               hostName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(1)
    try:
        s.connect(('127.0.0.1', 12345))

    except socket.error.errno:
        pass
    s.setblocking(0)
    return s
    # except socket.error:
    #     # # if socket.error.errno == errno.EINPROGRESS:
    #     # #     return None
    #     # # else:
    #     # raise Exception(socket.error.errno)
    #     return None


def join(hostIP: str, playerName: str):
    subprocess.Popen([executablePath+'app', '2', hostIP, playerName])
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', 12345))
    except socket.error.errno:
        print("ERROR: cannot connect")
    s.setblocking(0)
    return s
