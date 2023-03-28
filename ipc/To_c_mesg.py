import pygame
import sys
import os
import sysv_ipc
import re
import threading
KEY = 190234
PY_TO_C = 2
C_TO_PY = 3


class Posix_Op:
    def __init__(self):
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
        self.message = None

    def send_message(self, message):
        self.message_queue.send(message.encode(), type=PY_TO_C)

    def recv_message(self):
        self.message = self.message_queue.receive(type=C_TO_PY)
        self.message = self.decode_and_clean_message()

    def decode_and_clean_message(self):
        temp_list = list(self.message)
        temp_list[0] = self.message[0].decode(
            sys.getdefaultencoding(), errors='ignore')
        temp_list[0] = temp_list[0].split('\n')[0]
        temp_list[0] = temp_list[0].rstrip('\0')
        temp_list[1] = self.message[1]
        return tuple(temp_list)


class Player:
    def __init__(self, screen_width, screen_height, color) -> None:
        self.rect_width = 50
        self.rect_height = 50
        self.rect_color = color
        self.rect_position = [screen_width/2 - self.rect_width /
                              2, screen_height/2 - self.rect_height/2]

    def draw(self, screen):
        screen.fill((0, 0, 0))

        rect = pygame.Rect(
            self.rect_position[0], self.rect_position[1], self.rect_width, self.rect_height)
        pygame.draw.rect(screen, self.rect_color, rect)
        pygame.display.flip()


class Game:
    def __init__(self, screen_width, screen_height) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))

    def run(self, Sysv, player, player2):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.rect_position[0] -= 15
                    elif event.key == pygame.K_RIGHT:
                        player.rect_position[0] += 15
                    elif event.key == pygame.K_UP:
                        player.rect_position[1] -= 15
                    elif event.key == pygame.K_DOWN:
                        player.rect_position[1] += 15

            Sysv.send_message(
                f"{player.rect_position[0]} {player.rect_position[1]}\n")
            player.draw(self.screen)
            player2.draw(self.screen)

    def handle_input(input, player, Sysv):
        Sysv.recv_message()
        player.rect_position[0] = Sysv.message[0]
        player.rect_position[1] = Sysv.message[1]


pygame.init()

clock = pygame.time.Clock()

game = Game(800, 600)
player1 = Player(game.screen_width, game.screen_height, (255, 255, 255))
player2 = Player(game.screen_width, game.screen_height, (255, 0, 0))
Sysv = Posix_Op()

thread1 = threading.Thread(target=game.handle_input, args=(player2, Sysv))
thread2 = threading.Thread(target=game.run, args=(Sysv, player1, player2))
thread1.start()
thread2.start()

thread1.join()
thread2.join()
# game.run(Sysv, player1, player2)


clock.tick(60)
