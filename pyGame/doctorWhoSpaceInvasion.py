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

# Define Classes
class Entity:
    """Base class for sprite-based game entities (invaders, defenders, barriers)"""
    def __init__(self, name, x, y, width, height):
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

    def __init__(self, name, x, y, spriteFile, laserColour, width=40, height=40):
        """Initialise invader  with given properties"""
        super().__init__(name, x, y, width, height)
        self.laserColour = laserColour

        spritePath = os.path.join(gameDirectory, spriteFile)
        sprite = pygame.image.load(spritePath)
        self.sprite = pygame.transform.scale(sprite, (width, height))

class Defender(Entity):
    """Class representing the defender"""

    def __init__(self, name, x, y, spriteFile, width=60, speed=5):
        """Initialise defender with given properties"""
        height = int(width * 76 / 90)
        super().__init__(name, x, y, width, height)

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

    def __init__(self, name, x, y, spriteFile, width=100, height= 24, maxHealth=3):
        """Initialise barrier with given properties"""
        super().__init__(name, x, y, width, height)

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

    def __init__(self, x, y, speed, colour, width=5, height=10):
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

#  Game Configuration

score = 0
font = pygame.font.Font(None, 36)

# Defender types dictionary
defenderTypes = {
    "K9": {
        "spriteFile": "assets/sprites/k9.png",
        "speed": 5,
        "height": 60,
        "width": 60,
    }
}

#  Invader types dictionary
invaderTypes = {
    "Dalek": { 
        "spriteFile": "assets/sprites/dalek.png",
        "laserColour": (255, 0, 0),
        "width": 35, 
        "height": 67
        },
    "Cyberman": {
        "spriteFile": "assets/sprites/cyberman.png",
        "laserColour": (255, 0, 0),
        "width": 35, 
        "height": 67
        }
}

barrierTypes = {
    "Barrier": {
        "spriteFile": "assets/sprites/sonic.png",
        "health": 3,
        "width": 100,
        "height": 24,
    }
}

# Invader grid configuration
invaderRows = 3
invaderColumns = 10
invaderSpacing = 65
invaderStartX = 100
invaderStartY = 50
startInvaderSpeed = 1
invaderDirection = 1 # 1 for right, -1 for left
totalInvaders = invaderRows * invaderColumns

# Barrier configuration
barrierY = displayHeight - 200
barrierSpacing = 180

# Laser configuration
defenderLaserSpeed = -7  # Negative = upward
defenderLaserWidth = 5
defenderLaserHeight = 10
invaderLaserSpeed = 3  # Positive = downward
invaderLaserWidth = 4
invaderLaserHeight = 8
invaderFireRate = 0.0010

# Create player

# Randomly select defender type from available types
chosenDefender = random.choice(list(defenderTypes.keys()))
defenderConfig = defenderTypes[chosenDefender]

defender = Defender(
    name = chosenDefender,
    x = displayWidth // 2 - defenderConfig["width"] // 2, # Center horizontally: screen center minus half sprite width
    y = displayHeight - 80, # Position 80 pixels from bottom
    spriteFile = defenderConfig["spriteFile"],
    width = defenderConfig["width"],
    speed = defenderConfig["speed"]
)

defenderLasers = []

# Create grid of invaders
invaders = []
for row in range(invaderRows):
    for column in range(invaderColumns):
        # Calculate position in grid
        invaderX = invaderStartX + (column * invaderSpacing)
        invaderY = invaderStartY + (row * 80)  # 80px vertical spacing between rows

        chosenInvader = random.choice(list(invaderTypes.keys()))
        invaderConfig = invaderTypes[chosenInvader]

        invader = Invader(
            name = chosenInvader,
            x = invaderX,
            y = invaderY,
            spriteFile = invaderConfig["spriteFile"],
            laserColour = invaderConfig["laserColour"],
            width = invaderConfig["width"],
            height = invaderConfig["height"]
        )
        invaders.append(invader)

invaderLasers = []

# Create 4 evenly-spaced barriers across the screen
barriers = []
for i in range(4):
    chosenBarrier = random.choice(list(barrierTypes.keys()))
    barrierConfig = barrierTypes[chosenBarrier]

    barrierX = 100 + (i * barrierSpacing)  # Start at x=100, space by 180px
    barrier = Barrier(
        name = chosenBarrier,
        x = barrierX,
        y = barrierY,
        spriteFile = barrierConfig["spriteFile"],
        width = barrierConfig["width"],
        height = barrierConfig["height"],
        maxHealth = barrierConfig["health"]
    )
    barriers.append(barrier)

# Create starfield background
backgroundStars = []
for i in range(100):
    starX = random.randint(0, displayWidth)
    starY = random.randint(0, displayHeight)
    starSize = random.randint(1, 3)
    starBrightness = random.randint(100, 255)
    backgroundStars.append({
        "x": starX,
        "y": starY,
        "size": starSize,
        "brightness": starBrightness
    })

#  Helper Functions

def moveInvaders():
    """Move invaders horizontally, and when they reach the edge, move them down and reverse direction
    Speed increases as invaders are destroyed (up to a maximum of 5x)
    """
    global invaderDirection

    remainingInvaders = len(invaders)
    if remainingInvaders > 0:
        speedMultiplier = totalInvaders / remainingInvaders
        currentSpeed = min(startInvaderSpeed * speedMultiplier,startInvaderSpeed * 5)
    else:
        currentSpeed = startInvaderSpeed

    reachedEdge = False
    for invader in invaders:
        invader.x += currentSpeed * invaderDirection

        # Check if this invader reached the edge
        if invader.x <= 0 or invader.x >= displayWidth - invader.width:
            reachedEdge = True

    if reachedEdge:
        for invader in invaders:
            invader.y += 10
        invaderDirection *= -1

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
