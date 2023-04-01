import pygame
import sys
# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Initialize variables to track the drag selection
drag_start = None
drag_end = None
drag_in_progress = False

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Start drag on left mouse button down
            if event.button == 1:
                drag_start = event.pos
                drag_in_progress = True
        elif event.type == pygame.MOUSEMOTION:
            # Update the drag end position
            if drag_in_progress:
                drag_end = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # End the drag on left mouse button up
            if event.button == 1:
                drag_in_progress = False
                drag_start = None
                drag_end = None

    # Draw the screen
    screen.fill((0, 0, 0))

    # Draw the selection rectangle
    if drag_in_progress and drag_start != None and drag_end != None:
        x1, y1 = min(drag_end, drag_start)
        x2, y2 = max(drag_end, drag_start)
        width = x2 - x1
        height = y2 - y1
        pygame.draw.rect(screen, (255, 255, 255), (x1, y1, width, height), 2)
    pygame.display.flip()
