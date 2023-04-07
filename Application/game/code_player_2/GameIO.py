from IPC import IPC
import time
import json
from World import World
# Class action is the model of game action.
# An action is an input from player (user)


# Class IO is the representation of presentation layer.
# It plays the role of processing the output from game (application layer) to network (session layer)
# and processing the input from the network (session layer) to game (application layer)
class IO:
    def __init__(self) -> None:
        # The stack used for storing the input from the network (list of Actions)
        self.inputStack = None
        # The stack used for storing the output from the game (list of Actions)
        self.outputStack = None
        self.funcStack = FunctionQueue()
        self.ipc = IPC()
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

    def _strToAction(self, game, function_queue):
        recvmesg = self.receiveAction()
        if (recvmesg is not None):
            for encodedAction in recvmesg.split("\n"):
                encodedAction = json.loads(encodedAction)
                type = encodedAction['type']
                temp = json.loads(encodedAction['temp'])
                timestamp = encodedAction['timestamp']
                match type:
                    case "contruction":
                        function_queue.enqueue(
                            game.world.construction, timestamp, temp, game.mini_map)
                        # game.world.construction(temp, game.mini_map)
                    case "destruction":
                        function_queue.enqueue(
                            game.world.destruction, timestamp, temp, game.mini_map, game.H_R)
                    case "cheminement":
                        function_queue.enqueue(
                            game.world.cheminement, timestamp, temp, game.mini_map)

        # Decode the json object into an Action object
        # +++ YOUR CODE HERE +++ #

    # Method @sendAction is used to send all action in @self.outputStack to all players (include sender)
    # @parameters: {
    #   @self: This class
    # }
    # @return: 0 if successfully send or -1 if not

    def sendActions(self, action: str, temp, timestamp=time.time()) -> int:
        # Step 1: Encode all action in @self.outputStack
        temp = self._tempToStr(temp)
        mesg = {"type": action, "temp": temp, "timestamp": timestamp}
        self.ipc.sendToNetwork(json.dumps(mesg))

        # Step 2: Send the encoded message using @self.IPC
        # Step 3: Remove all action in @self.outputStack
        # +++ YOUR CODE HERE +++ #
        # pass

    # Method @receiveActions is used to receive message from the other players and store in @self.inputStack
    # @parameters: {
    #   @self: This class
    #   @encodedAction: The received message, encoded version of actions.
    # }
    # @return: 0 if successfully receive or -1 if not
    def receiveAction(self):
        if (self.ipc.receiveFromNetwork()):
            return self.ipc.mesg
        return None

        # Step 1: Receive all action from @self.IPC
        # Step 2: Decode string message into a list of actions
        # Step 3: push them onto the inputStack
        # +++ YOUR CODE HERE +++ #


class FunctionQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, func, timestamp=None, *args, **kwargs):
        if timestamp is None:
            timestamp = time.time()
        self.queue.append((timestamp, func, args, kwargs))

    def execute(self):
        self.queue.sort()
        for timestamp, func, args, kwargs in self.queue:
            if func != None:
                func(*args, **kwargs)
                self.queue.remove((timestamp, func, args, kwargs))
