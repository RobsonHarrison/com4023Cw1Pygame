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
        self.sprite = None

    def getRect(self):
        """Get the rectangle representing the entity's position and size"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """Draw the entity on the screen"""
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))

class Invader(Entity):
    """Class representing an invader"""

    def init(self, name, x, y, spriteFile, laserColour, width=40, height=40):
        """Initialise invader  with given properties"""
        super().init(name, x, y, width, height)
        self.laserColour = laserColour

        spritePath = os.path.join(gameDirectory, spriteFile)
        sprite = pygame.image.load(spritePath)
        self.sprite = pygame.transform.scale(sprite, (width, height))

class Defender(Entity):
    """Class representing the defender"""

    def init(self, name, x, y, spriteFile, width=60, speed=5):
        """Initialise defender with given properties"""
        height = int(width * 76 / 90)
        super().init(name, x, y, width, height)

        self.speed = speed
        self.moveLeft = False
        self.moveRight = False
        spritePath = os.path.join(gameDirectory, spriteFile)
        sprite = pygame.image.load(spritePath)
        self.sprite = pygame.transform.scale(sprite, (self.width, self.height))

    def move(self, displayWidth):
        """Move the defender based on movement state"""
        if self.moveLeft and self.x > 0:
            self.x -= self.speed
        if self.moveRight and self.x < displayWidth - self.width:
            self.x += self.speed

    def getLaserStart(self):
        """Get the starting position for a laser fired by the defender (centre of the defender)"""
        return (self.x + self.width // 2, self.y)

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