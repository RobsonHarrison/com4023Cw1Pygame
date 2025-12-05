import pygame
import sys
import random
import os

# Initialise pygame
pygame.init()

# Get the directory of the game script
gameDirectory = os.path.dirname(os.path.abspath(__file__))

# Set up display
displayWidth = 800
displayHeight = 600
fps = 60

# Colours used for background and text
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Doctor Who Space Invasion")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()