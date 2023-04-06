import subprocess
# from Presentation import IO
# The function @getAvailableRoom is used to get the available rooms from network module
# @parameters: {
#   None
# }
#


def getAvailableRoom():
    # call main.c
    # send request to main.c
    # receive rooom list
    return ['room 1', 'room 2', 'room 3']


def createRoom(roomName: str, hostName: str):
    pass
    result = subprocess.run(['./app', '1 room player'],
                            capture_output=True, text=True)
    # call main.c
    # argv[1] : mode, argv[2] : roomName, argv[3] : playerName


def join(roomName: str, playerName: str):
    pass
    result = subprocess.run(['./app', '1 room player'],
                            capture_output=True, text=True)
    # call main.c


def getPlayers():
    pass

# import subprocess

# Run shell command
# result = subprocess.run(['ls', '-l'], capture_output=True, text=True)

# Print output
# print(result.stdout)
# print(result)
