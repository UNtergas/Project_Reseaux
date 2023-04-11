from IPC import IPC
import time
import json
import socket
from World import World
import errno
import re

# Class action is the model of game action.
# An action is an input from player (user)

class Action:
    def __init__(self,func, timestamp, *args,**kwargs):
        self.func = func
        self.timestamp = timestamp
        self.args = args
        self.kwargs = kwargs
# ine 48, in handleEvents
#     self.handleEventsFunc(self, event)
#   File "/home/john/Desktop/Project_Reseaux/Application/game/code/Scenes/Scene_multicreate.py", line 54, in SceneEventHandler
#     self.game.save = Save(self.box["inputbox"].text, socket)
#   File "/home/john/Desktop/Project_Reseaux/Application/game/code/Save.py", line 31, in __init__
#     self.IO = IO(socket=socket)
#   File "/home/john/Desktop/Project_Reseaux/Application/game/code/GameIO.py", line 20, in __init__
#     self.funcStack = FunctionQueue()
# TypeError: FunctionQueue.__init__() missing 1 required positional argument: 'func'

# what is this error?
        

    # def execute(self):
    #     func = self.func
        
    #     func(*self.args,**self.kwargs)


# Class IO is the representation of presentation layer.
# It plays the role of processing the output from game (application layer) to network (session layer)
# and processing the input from the network (session layer) to game (application layer)
class IO:
    def __init__(self, socket: socket.socket) -> None:
        # The stack used for storing the input from the network (list of Actions)
        self.inputStack = []
        # The stack used for storing the output from the game (list of Actions)
        self.outputStack = []
        self.ipc = IPC(socket)
        self.mesg= None
        
    # Private method @_actionToStr is used to encode an action to a string. It help to transmit in4 in the network
    # @parameters: {
    #   @self: This class (not used)
    #   @action: The action needed to be encoded to transmit in the network
    # }
    # @return: a string (encoding version of action)

    # Private method @strToAction is used to decode a string to an action.
    # @parameters: {
    #   @self: This class (not used)
    #   @encodedAction: The string - the encoding version of action
    # }
    # @return: an object of class Action (an action)

    def _tempToStr(self, temp):
        del temp['image']
        return json.dumps(temp)

    def _strToAction(self, game, encodedAction):
        # print("incomingIn4: "+ encodedAction)
        if (encodedAction is not None):
            encodedAction = json.loads(encodedAction)
            type = encodedAction['type'] 
            if encodedAction['temp'] != '': temp = json.loads(encodedAction['temp'])
            timestamp = encodedAction['timestamp']
            match type:
                    case "contruction":
                        return Action(
                                    game.world.construction,timestamp, temp, game.mini_map)
                    case "destruction":
                        return Action(
                            game.world.destruction,timestamp, temp, game.mini_map, game.H_R)
                    case "cheminement":
                        return Action(
                            game.world.cheminement,timestamp, temp, game.mini_map)
                    case "save":
                        return Action(
                            game.game.save.save,timestamp)

    # Method @sendAction is used to send all action in @self.outputStack to all players (include sender)
    # @parameters: {
    #   @self: This class
    # }
    # @return: 0 if successfully send or -1 if not

    def sendActions(self, action: str, temp, timestamp=time.time()) -> int:
        # Step 1: Encode all action in @self.outputStack
        temp = self._tempToStr(temp) if (temp is not None) else None
        action = {"type": action, "temp": temp, "timestamp": timestamp}
        mesg = json.dump(mesg)
        self.outputStack.append(mesg)
        self.ipc.sendToNetwork("PRE:"+mesg+":POST")

    # Method @receiveActions is used to receive message from the other players and store in @self.inputStack
    # @parameters: {
    #   @self: This class
    #   @encodedAction: The received message, encoded version of actions.
    # }
    # @return: 0 if successfully receive or -1 if not
    def listenGameState(self):
        mesg = self.ipc.receiveFromNetwork()
        if mesg:
            if mesg == "!Loaded":
                return True
        return False
    
    
    def listening(self, game):
        mesg = self.ipc.receiveFromNetwork()
        if mesg:
            # print(mesg)
            if not self.mesg:
                self.mesg = mesg
            else:
                self.mesg =  self.mesg+ mesg
            action_syntax =r'PRE:(.*?):POST'
            actionlist=[]
            while True:
                result = self.extract_and_remove_action(action_syntax)
                if result == None:
                    break
                actionlist.append(result)
            # mesg = mesg.split("PRE:")[1:]
            for encodedAction in actionlist:
                # encodedAction = encodedAction[:-5]
                action = self._strToAction(game,encodedAction)
                self.inputStack.append(action)
    def resolving(self):    
        if self.inputStack:
            print(self.inputStack)
            sorted_stack= sorted(self.inputStack, key=lambda x: x.timestamp)
            for action in sorted_stack:
                if isinstance(action,Action):
                    action.func(*action.args,**action.kwargs)
                    self.inputStack.remove(action)



    def extract_and_remove_action(self, action_syntax):
        # Create a regex pattern for the action syntax
        pattern = re.compile(action_syntax)
        # Find all matches of the action syntax in the string
        matches = pattern.search(self.mesg)
        if matches:
            # select 1st action to remove
            action_to_return = matches.group(0)
            # Remove the action from the string
            self.mesg = self.mesg.replace(action_to_return, '', 1)
            action_to_return = action_to_return[4:]
            action_to_return = action_to_return[:-5]
            return action_to_return
        return None

