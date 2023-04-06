import pygame
import sys
import time
import sysv_ipc
from function_queue import FunctionQueue
from Player import Player
A_TO_B = 1
B_TO_A = 2
IDENTIFIER = 'test_prog.txt'
KEY = 199999
KEY_GEN = 69
NAME = 'B'


class Sysv:
    def __init__(self) -> None:
        # self.key = sysv_ipc.ftok(IDENTIFIER, KEY_GEN)
        self.message_queue = sysv_ipc.MessageQueue(
            KEY, sysv_ipc.IPC_CREAT)
        self.mesg = None

    def send_message(self, message):
        self.message_queue.send(message.encode('utf-8'), type=B_TO_A)

    def recv_message(self):
        self.mesg = self.message_queue.receive(type=A_TO_B)
        self.mesg = self.decode_format()

    def decode_format(self):
        temp = self.mesg.decode('utf-8')
        return dict(tuple(key_value.split('=') for key_value in temp.split(',')))


class Game:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.func_queue = FunctionQueue()

    def RECV_SYS(self, Sysv, player):
        Sysv.recv_message()
        player.rect_position[0] = Sysv.mesg['x']
        player.rect_position[1] = Sysv.mesg['y']

    def event(self, player, Sysv):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.func_queue.enqueue(player.movement('left'))
                    self.func_queue.enqueue(Sysv.send_message(
                        f"x={player.rect_position[0]},y={player.rect_position[1]}"))
                elif event.key == pygame.K_RIGHT:
                    self.func_queue.enqueue(player.movement('right'))
                    self.func_queue.enqueue(Sysv.send_message(
                        f"x={player.rect_position[0]},y={player.rect_position[1]}"))
                elif event.key == pygame.K_UP:
                    self.func_queue.enqueue(player.movement('up'))
                    self.func_queue.enqueue(Sysv.send_message(
                        f"x={player.rect_position[0]},y={player.rect_position[1]}"))
                elif event.key == pygame.K_DOWN:
                    self.func_queue.enqueue(player.movement('down'))
                    self.func_queue.enqueue(Sysv.send_message(
                        f"x={player.rect_position[0]},y={player.rect_position[1]}"))

    def render(self, player):
        self.screen.fill((0, 0, 0))
        player.phuoc_ve(self.screen)

    def run(self, player, Sysv):
        self.func_queue.enqueue(self.RECV_SYS(Sysv, player))
        self.event(player)
        self.func_queue.execute()
        self.render(player)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((800, 600))
game = Game(screen)
player1 = Player(800, 600, (255, 255, 255))
# player2 = Player(800)
sysv = Sysv()
while True:
    game.run(player1, sysv)
