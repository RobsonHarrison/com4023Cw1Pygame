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

class Barrier(Entity):
    """Class representing a barrier"""

    def init(self, name, x, y, spriteFile, width=100, height= 24, maxHealth=3):
        """Initialise barrier with given properties"""
        super().init(name, x, y, width, height)

        self.health = maxHealth
        self.maxHealth = maxHealth

        spritePath = os.path.join(gameDirectory, spriteFile)
        sprite = pygame.image.load(spritePath)
        self.sprite = pygame.transform.scale(sprite, (self.width, self.height))
        self.image = self.sprite.copy()
        self.damageRegions = []

    def takeDamage(self):
        """Reduce barrier health and update damage regions"""
        self.health -= 1

        # Create damage regions
        if not self.isDestroyed():
            for _ in range(random.randint(3, 6)):
                damageX = random.randint(5, self.width - 5)
                damageY = random.randint(2, self.height - 2)
                damageSize = random.randint(4, 10)
                self.damageRegions.append((damageX, damageY, damageSize))

            self.image = self.sprite.copy()

            for damageX, damageY, damageSize in self.damageRegions:
                pygame.draw.circle(self.image, (0,0,0), damageX, damageY, damageSize)

    def isDestroyed(self):
        """Check if the barrier is destroyed"""
        return self.health <= 0

    def draw(self, screen):
        """Draw the barrier on the screen"""
        if not self.isDestroyed():
            screen.blit(self.image, (self.x, self.y))

class Laser:
    """Class representing a laser"""

    def init(self, x, y, speed, colour, width=5, height=10):
        """Initialise laser with given properties"""
        self.x = x
        self.y = y
        self.speed = speed
        self.colour = colour
        self.width = width
        self.height = height

    def move(self):
        """Move the laser"""
        self.y += self.speed

    def getRect(self):
        """Get the rectangle representing the laser's position and size"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """Draw the laser on the screen"""
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
    
    def isOffScreen(self, displayHeight):
        """Check if the laser is off the screen"""
        return self.y < 0 or self.y > displayHeight


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