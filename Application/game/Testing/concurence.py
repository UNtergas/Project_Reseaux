import pygame

# Create two surfaces with different colors
surface1 = pygame.Surface((100, 100))
surface1.fill((255, 0, 0))  # Red

surface2 = pygame.Surface((100, 100))
surface2.fill((0, 255, 0))  # Green

# Draw the surfaces to the screen at different positions
screen.blit(surface1, (0, 0))
screen.blit(surface2, (100, 100))
