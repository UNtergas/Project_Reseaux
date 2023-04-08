import subprocess
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
    
    result = subprocess.run([executablePath+'getAvailableRoom'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8').split('\n')
    result.pop()
    rooms = None
    if result != None:
        rooms = list(map(strToRoomIn4, result))
    
    return rooms

def createRoom(roomName: str, hostName: str):
    process = subprocess.Popen([executablePath+'app', '1', roomName, hostName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Room created!")
    # call main.c
    # argv[1] : mode, argv[2] : roomName, argv[3] : playerName

def join(hostIP: str, playerName: str):
    subprocess.run([executablePath+'app', '2', hostIP, playerName])
    # call main.c

rooms = getAvailableRoom()
print(rooms)




