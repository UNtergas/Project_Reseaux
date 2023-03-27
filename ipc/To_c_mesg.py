import pygame
import sys
import os
import sysv_ipc
import re
KEY = 190234
PY_TO_C = 2


class Posix_Op:
    def __init__(self):
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
        self.message = None

    def send_message(self, message):
        self.message_queue.send(message.encode(), type=PY_TO_C)


pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Rectangle")

# Set up the rectangle
rect_width = 50
rect_height = 50
rect_color = (255, 255, 255)
rect_position = [screen_width/2 - rect_width /
                 2, screen_height/2 - rect_height/2]

# Set up the clock
clock = pygame.time.Clock()

# Game loop
while True:
    # Handle eventsP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect_position[0] -= 15
            elif event.key == pygame.K_RIGHT:
                rect_position[0] += 15
            elif event.key == pygame.K_UP:
                rect_position[1] -= 15
            elif event.key == pygame.K_DOWN:
                rect_position[1] += 15

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the rectangle
    rect = pygame.Rect(
        rect_position[0], rect_position[1], rect_width, rect_height)
    pygame.draw.rect(screen, rect_color, rect)

    # package for sending
    Sender = Posix_Op()
    Sender.send_message(f"{rect_position[0]} T{rect_position[1]}\n")
    # Update the screen
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)
