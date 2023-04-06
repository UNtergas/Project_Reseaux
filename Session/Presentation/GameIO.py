from IPC import IPC
import json

# Class action is the model of game action. 
# An action is an input from player (user)
class Action:
    def __init__(self, type, buildingRequirement) -> None:
        self.type = type 
        self.buildingRequirement = buildingRequirement

    # Method @execute is used to execute this action (@self) in the @game
    # @parameters: {
    #   @self: The action we want to execute
    #   @game: The game that we want to execute this action in
    # }
    # @return: 0 if successfully insert to table or -1 if not
    def execute(self, game) -> int: 
        # execute @self in @game
        # +++ YOUR CODE HERE +++ #
        pass


# Class IO is the representation of presentation layer.
# It plays the role of processing the output from game (application layer) to network (session layer)
# and processing the input from the network (session layer) to game (application layer)
class IO:
    def __init__(self) -> None:
        self.inputStack = None # The stack used for storing the input from the network (list of Actions)
        self.outputStack = None # The stack used for storing the output from the game (list of Actions)
        self.IPC = IPC()
        
    # Private method @_actionToStr is used to encode an action to a string. It help to transmit in4 in the network
    # @parameters: {
    #   @self: This class (not used)
    #   @action: The action needed to be encoded to transmit in the network
    # }
    # @return: a string (encoding version of action)

    def _actionToStr(self, action: Action) -> str:
        # Encode the action into a json object
        json_data = {"type": action.type, "buildingRequirement": action.buildingRequirement}
        return json.dumps(json_data)
        
    

    # Private method @strToAction is used to decode a string to an action.
    # @parameters: {
    #   @self: This class (not used)
    #   @encodedAction: The string - the encoding version of action
    # }
    # @return: an object of class Action (an action)
    def _strToAction(encodedAction: str) -> Action:
        # Decode the json object into an Action object
        json_data = json.loads(encodedAction)
        type = json_data["type"]
        buildingRequirement=json_data["buildingRequirement"]
        return Action(type,buildingRequirement)

    # Method @sendAction is used to send all action in @self.outputStack to all players (include sender)
    # @parameters: {
    #   @self: This class
    # }
    # @return: 0 if successfully send or -1 if not
    def sendActions(self) -> int:
        # Step 1: Encode all action in @self.outputStack
        # Step 2: Send the encoded message using @self.IPC
        # Step 3: Remove all action in @self.outputStack

        if not self.outputStack:
            return 0

        # Encode all actions in outputStack
        encoded_actions = []
        for action in self.outputStack:
            encoded_actions.append(self._actionToStr(action))

        # Send encoded message using IPC
        message = '\n'.join(encoded_actions)
        self.IPC.sendMessage(message)

        # Remove all actions in outputStack
        self.outputStack = []

        return len(encoded_actions)

        

    # Method @receiveActions is used to receive message from the other players and store in @self.inputStack
    # @parameters: {
    #   @self: This class
    #   @encodedAction: The received message, encoded version of actions.
    # }
    # @return: 0 if successfully receive or -1 if not
    def receiveAction(self, encodedAction: str) -> int:
            # Step 1: Receive all action from @self.IPC
            # Step 2: Decode string message into a list of actions
            # Step 3: push them onto the inputStack
            # +++ YOUR CODE HERE +++ #

        # deu biet viet :V
            

    


    