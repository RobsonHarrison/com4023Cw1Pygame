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

class Entity:
    """Base class for sprite-based game entities (invaders, defenders, barriers)"""
    def init(self, name, x, y, width, height):
        """Initialise common entity properties"""
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = None

    def getRect(self):
        """Get the rectangle representing the entity's position and size"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """Draw the entity on the screen"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))


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