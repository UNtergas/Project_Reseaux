import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
size = (700, 500)

# Create the window
screen = pygame.display.set_mode(size)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Show the pop-up message
                pygame.messagebox.showinfo(
                    "Message", "This is a pop-up message.")

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
