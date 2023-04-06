from Presentation import GameIO as IO


def getAvailableRoom():
    rooms = []
    response = IO.sendReceiveData("GET_ROOMS", None)

    if response["status"] == "SUCCESS":
        rooms = response["data"]

    return rooms


def createRoom(roomName: str, playerName: str):
    response = IO.sendReceiveData("CREATE_ROOM", (roomName, playerName))
    if response["status"] == "SUCCESS":
        return True
    else:
        return False


def join(roomName: str, playerName: str):
    response = IO.sendReceiveData("JOIN_ROOM", (roomName, playerName))
    if response["status"] == "SUCCESS":
        return True
    else:
        return False


def getPlayers():
    response = IO.sendReceiveData("GET_PLAYERS", None)

    if response["status"] == "SUCCESS":
        return response["data"]

    return None


"""
# The function @getAvailableRoom is used to get the available rooms from network module
# @parameters: {
#   None
# }
#
def getAvailableRoom():
    # call main.c
    # send request to main.c
    # receive rooom list
    pass
    return rooms


def createRoom(roomName: str, hostName: str):
    pass
    # call main.c
    # argv[1] : mode, argv[2] : roomName, argv[3] : playerName


def join(roomName: str, playerName: str):
    pass
    # call main.c


def getPlayers():
    pass
