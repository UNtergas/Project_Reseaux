import pygame

# Initialize Pygame
pygame.init()

# Create a Pygame window
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Create a Surface for the mini map
mini_map_size = (200, 150)
mini_map = pygame.Surface(mini_map_size)

# Load the map image
map_image = pygame.image.load("Testing/europe.png")

# Draw the map image onto the mini map Surface
mini_map.blit(map_image, (0, 0))

# Scale the map image down to create the mini map effect
mini_map = pygame.transform.scale(mini_map, (200, 150))

# Update the Pygame window to display the mini map
pygame.display.update()

going = True
while going:
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False


pygame.quit()
