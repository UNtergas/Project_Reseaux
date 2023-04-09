import socket
# from const import SERVER_ADDRESS, SERVER_PORT
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 12345
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
    # s.setblocking(0)
    # try:
    time.sleep(1)
    s.connect((SERVER_ADDRESS, SERVER_PORT))
    print('socket connect success')
    s.setblocking(0)
    return s
    # except socket.error:
    #     # # if socket.error.errno == errno.EINPROGRESS:
    #     # #     return None
    #     # # else:
    #     # raise Exception(socket.error.errno)
    #     return None

    # call main.c
    # argv[1] : mode, argv[2] : roomName, argv[3] : playerName


def join(hostIP: str, playerName: str):
    subprocess.run([executablePath+'app', '2', hostIP, playerName])
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    s.connect((SERVER_ADDRESS, SERVER_PORT))
    return s
    # call main.c