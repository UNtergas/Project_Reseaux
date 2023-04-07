import subprocess
from Presentation import GameIO as IO

<<<<<<< yacine

def getAvailableRoom():
    print('getAvailableRoom')
    pass
    rooms = []
    response = IO.sendReceiveData("GET_ROOMS", None)

    if response["status"] == "SUCCESS":
        rooms = response["data"]

    return rooms


def createRoom(roomName: str, playerName: str):
    print('createRoom')
    pass
    response = IO.sendReceiveData("CREATE_ROOM", (roomName, playerName))
    if response["status"] == "SUCCESS":
        return True
    else:
        return False


def join(roomName: str, playerName: str):
    print('Join')
    pass
    response = IO.sendReceiveData("JOIN_ROOM", (roomName, playerName))
    if response["status"] == "SUCCESS":
        return True
    else:
        return False


def getPlayers():
    print("getPlayers")
    pass
    response = IO.sendReceiveData("GET_PLAYERS", None)

    if response["status"] == "SUCCESS":
        return response["data"]

    return None


"""
=======
>>>>>>> main
# The function @getAvailableRoom is used to get the available rooms from network module
# @parameters: {
#   None
# }
#

executablePath = "./../../../../executable/"

def getAvailableRoom():

    def strToRoomIn4(rawStr: str):
        arr = rawStr.split(": ")
        return {
            "roomName": arr[0],
            "hostIP": arr[1]
        }
    
    result = subprocess.run([executablePath+'getAvailableRoom'], stdout=subprocess.PIPE);

    rooms = list(map(strToRoomIn4, result.stdout.decode('utf-8').split('\n')))
    
    return rooms


def createRoom(roomName: str, hostName: str):
    subprocess.run([executablePath+'app', '1', roomName, hostName])
    # call main.c
    # argv[1] : mode, argv[2] : roomName, argv[3] : playerName


def join(roomName: str, playerName: str):
    subprocess.run([executablePath+'app', '2', roomName, playerName])
    # call main.c


def getPlayers():
<<<<<<< yacine
    pass
"""
=======
    pass
>>>>>>> main
