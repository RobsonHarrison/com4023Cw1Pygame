"""
Doctor Who Space Invasion Game

A Space Invaders-style arcade game featuring Doctor Who characters.
The player controls a Doctor Who hero defending against waves of Doctor Who villains,
using barriers for protection whilst destroying all invaders to win.

Uses Pygame for graphics and game logic.
"""

import pygame
import sys
import random
import os
from startScreen import drawStartScreen
from gameOverScreen import drawGameOverScreen
from background import animateStars, drawStars

# ============================================================================
# INITIALISATION
# ============================================================================

# Initialise pygame
pygame.init()

# Get the directory of the game script for loading assets
gameDirectory = os.path.dirname(os.path.abspath(__file__))

# Display configuration
displayWidth = 800
displayHeight = 600
fps = 60  # Frames per second

# Colour definitions
black = (0, 0, 0)
white = (255, 255, 255)

# ============================================================================
# CLASS DEFINITIONS
# ============================================================================
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
    """Class representing an invader

    Invaders move horizontally across the screen, reversing direction when
    they reach the edge. They fire lasers downward at random intervals.
    """

    def __init__(self, name, x, y, spriteFile, laserColour, laserSpeed, laserWidth, laserHeight, scoreValue, width=40, height=40):
        """Initialise invader with given properties

        Args:
            name: Type of invader (e.g., 'Dalek', 'Cyberman')
            x: Initial x position
            y: Initial y position
            spriteFile: Path to sprite image file
            laserColour: RGB tuple for laser colour
            laserSpeed: Speed of laser (positive = downward)
            laserWidth: Width of laser in pixels
            laserHeight: Height of laser in pixels
            scoreValue: Points awarded for destroying this invader
            width: Width of invader sprite (default: 40)
            height: Height of invader sprite (default: 40)
        """
        super().__init__(name, x, y, width, height)
        self.laserColour = laserColour
        self.laserSpeed = laserSpeed
        self.laserWidth = laserWidth
        self.laserHeight = laserHeight
        self.scoreValue = scoreValue

        spritePath = os.path.join(gameDirectory, spriteFile)
        sprite = pygame.image.load(spritePath)
        self.sprite = pygame.transform.scale(sprite, (width, height))

class Defender(Entity):
    """Class representing the defender

    The defender is controlled by the player using arrow keys to move
    left/right and spacebar to fire lasers upward.
    """

    def __init__(self, name, x, y, spriteFile, laserColour, laserSpeed, laserWidth, laserHeight, width=60, speed=5):
        """Initialise defender with given properties

        Args:
            name: Type of defender (e.g., 'K9')
            x: Initial x position
            y: Initial y position
            spriteFile: Path to sprite image file
            laserColour: RGB tuple for laser colour
            laserSpeed: Speed of laser (negative = upward)
            laserWidth: Width of laser in pixels
            laserHeight: Height of laser in pixels
            width: Width of defender sprite (default: 60)
            speed: Movement speed in pixels per frame (default: 5)
        """
        height = int(width * 76 / 90)  # Maintain K9 sprite aspect ratio
        super().__init__(name, x, y, width, height)

        self.speed = speed
        self.laserColour = laserColour
        self.laserSpeed = laserSpeed
        self.laserWidth = laserWidth
        self.laserHeight = laserHeight
        self.moveLeft = False
        self.moveRight = False
        spritePath = os.path.join(gameDirectory, spriteFile)
        sprite = pygame.image.load(spritePath)
        self.sprite = pygame.transform.scale(sprite, (self.width, self.height))

    def move(self, displayWidth):
        """Move the defender based on movement state

        Args:
            displayWidth: Width of the display to prevent moving off-screen
        """
        if self.moveLeft and self.x > 0:
            self.x -= self.speed
        if self.moveRight and self.x < displayWidth - self.width:
            self.x += self.speed

    def getLaserStart(self):
        """Get the starting position for a laser fired by the defender

        Returns:
            Tuple of (x, y) coordinates at the centre top of the defender
        """
        return (self.x + self.width // 2, self.y)

class Barrier(Entity):
    """Class representing a barrier (sonic screwdriver)

    Barriers provide protection for the defender but can be damaged by lasers
    from both invaders and the defender. They are destroyed after taking
    sufficient damage.
    """

    def __init__(self, name, x, y, spriteFile, width=100, height= 24, maxHealth=3):
        """Initialise barrier with given properties

        Args:
            name: Type of barrier
            x: Initial x position
            y: Initial y position
            spriteFile: Path to sprite image file
            width: Width of barrier sprite (default: 100)
            height: Height of barrier sprite (default: 24)
            maxHealth: Maximum health points (default: 3)
        """
        super().__init__(name, x, y, width, height)

        self.health = maxHealth
        self.maxHealth = maxHealth

        spritePath = os.path.join(gameDirectory, spriteFile)
        sprite = pygame.image.load(spritePath)
        self.sprite = pygame.transform.scale(sprite, (self.width, self.height))
        self.image = self.sprite.copy()
        self.damageRegions = []  # List of (x, y, size) tuples for damage circles

    def takeDamage(self):
        """Reduce barrier health and update damage regions

        Creates random black circles on the barrier sprite to visually
        represent damage. Barrier is destroyed when health reaches 0.
        """
        self.health -= 1

        # Create random damage regions (black circles)
        if not self.isDestroyed():
            for _ in range(random.randint(3, 6)):
                damageX = random.randint(5, self.width - 5)
                damageY = random.randint(2, self.height - 2)
                damageSize = random.randint(4, 10)
                self.damageRegions.append((damageX, damageY, damageSize))

            # Redraw sprite with all accumulated damage
            self.image = self.sprite.copy()

            for damageX, damageY, damageSize in self.damageRegions:
                pygame.draw.circle(self.image, (0,0,0), (damageX, damageY), damageSize)

    def isDestroyed(self):
        """Check if the barrier is destroyed

        Returns:
            True if health is 0 or below, False otherwise
        """
        return self.health <= 0

    def draw(self, screen):
        """Draw the barrier on the screen

        Args:
            screen: Pygame surface to draw on
        """
        if not self.isDestroyed():
            screen.blit(self.image, (self.x, self.y))

class Laser:
    """Class representing a laser projectile

    Lasers are fired by both defenders (upward) and invaders (downward).
    They move vertically and are removed when they go off-screen or hit a target.
    """

    def __init__(self, x, y, speed, colour, width=5, height=10):
        """Initialise laser with given properties

        Args:
            x: Initial x position
            y: Initial y position
            speed: Vertical speed (negative = upward, positive = downward)
            colour: RGB tuple for laser colour
            width: Width of laser rectangle (default: 5)
            height: Height of laser rectangle (default: 10)
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.colour = colour
        self.width = width
        self.height = height

    def move(self):
        """Move the laser vertically based on its speed"""
        self.y += self.speed

    def getRect(self):
        """Get the rectangle representing the laser's position and size

        Returns:
            pygame.Rect object for collision detection
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """Draw the laser on the screen

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def isOffScreen(self, displayHeight):
        """Check if the laser has moved off the screen

        Args:
            displayHeight: Height of the display

        Returns:
            True if laser is above or below the screen, False otherwise
        """
        return self.y < 0 or self.y > displayHeight

# ============================================================================
# GAME CONFIGURATION
# ============================================================================

# Score and lives tracking
score = 0
lives = 3  # Number of lives the player starts with
font = pygame.font.Font(None, 36)

# Game state
gameState = "start"  # Possible values: "start", "playing", "gameover"
victory = False  # Track if player won or lost

# Defender types dictionary - defines properties for each defender type
defenderTypes = {
    "K9": {
        "spriteFile": "assets/sprites/k9.png",
        "speed": 5,
        "height": 60,
        "width": 60,
        "laserColour": (255, 255, 255),
        "laserSpeed": -7,  # Negative = upward
        "laserWidth": 5,
        "laserHeight": 10
    }
}

# Invader types dictionary - defines properties for each invader type
invaderTypes = {
    "Dalek": {
        "spriteFile": "assets/sprites/dalek.png",
        "width": 35,
        "height": 67,
        "laserColour": (255, 0, 0),
        "laserSpeed": 3,  # Positive = downward
        "laserWidth": 4,
        "laserHeight": 8,
        "scoreValue": 15
        },
    "Cyberman": {
        "spriteFile": "assets/sprites/cyberman.png",
        "width": 35,
        "height": 67,
        "laserColour": (0, 0, 255),
        "laserSpeed": 3,  # Positive = downward
        "laserWidth": 4,
        "laserHeight": 8,
        "scoreValue": 5
        },
    "WeepingAngel": {
        "spriteFile": "assets/sprites/weepingAngel.png",
        "width": 35,
        "height": 67,
        "laserColour": (128, 0, 128),
        "laserSpeed": 3,  # Positive = downward
        "laserWidth": 4,
        "laserHeight": 8,
        "scoreValue": 25
        }
}

# Barrier types dictionary - defines properties for each barrier type
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
invaderColumns = 6
invaderSpacing = 65  # Horizontal spacing between invaders
invaderStartX = 100  # Starting x position for grid
invaderStartY = 50   # Starting y position for grid
startInvaderSpeed = 1  # Initial movement speed
invaderDirection = 1  # 1 for right, -1 for left
totalInvaders = invaderRows * invaderColumns  # Total count for speed calculation

# Barrier configuration
barrierY = displayHeight - 200  # Y position for all barriers
barrierSpacing = 180  # Horizontal spacing between barriers

# Invader firing configuration
invaderFireRate = 0.001  # Probability per frame that an invader fires (0.1%)

# ============================================================================
# GAME OBJECT INITIALISATION
# ============================================================================

# Create defender (player character)
# Randomly select defender type from available types (currently only K9)
chosenDefender = random.choice(list(defenderTypes.keys()))
defenderConfig = defenderTypes[chosenDefender]

defender = Defender(
    name = chosenDefender,
    x = displayWidth // 2 - defenderConfig["width"] // 2, # Centre horizontally: screen centre minus half sprite width
    y = displayHeight - 80, # Position 80 pixels from bottom
    spriteFile = defenderConfig["spriteFile"],
    laserColour = defenderConfig["laserColour"],
    laserSpeed = defenderConfig["laserSpeed"],
    laserWidth = defenderConfig["laserWidth"],
    laserHeight = defenderConfig["laserHeight"],
    width = defenderConfig["width"],
    speed = defenderConfig["speed"]
)

defenderLasers = []  # List to store active defender lasers

# Create grid of invaders
invaders = []
for row in range(invaderRows):
    for column in range(invaderColumns):
        # Calculate position in grid
        invaderX = invaderStartX + (column * invaderSpacing)
        invaderY = invaderStartY + (row * 80)  # 80px vertical spacing between rows

        # Randomly select invader type (Dalek or Cyberman)
        chosenInvader = random.choice(list(invaderTypes.keys()))
        invaderConfig = invaderTypes[chosenInvader]

        invader = Invader(
            name = chosenInvader,
            x = invaderX,
            y = invaderY,
            spriteFile = invaderConfig["spriteFile"],
            laserColour = invaderConfig["laserColour"],
            laserSpeed = invaderConfig["laserSpeed"],
            laserWidth = invaderConfig["laserWidth"],
            laserHeight = invaderConfig["laserHeight"],
            scoreValue = invaderConfig["scoreValue"],
            width = invaderConfig["width"],
            height = invaderConfig["height"]
        )
        invaders.append(invader)

invaderLasers = []  # List to store active invader lasers

# Create 4 evenly-spaced barriers across the screen for protection
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

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def moveInvaders():
    """Move invaders horizontally, and when they reach the edge, move them down and reverse direction

    Speed increases as invaders are destroyed (up to a maximum of 3x) to maintain
    game difficulty as the player progresses.
    """
    global invaderDirection

    # Calculate current speed based on remaining invaders
    remainingInvaders = len(invaders)
    if remainingInvaders > 0:
        speedMultiplier = totalInvaders / remainingInvaders
        currentSpeed = min(startInvaderSpeed * speedMultiplier, startInvaderSpeed * 3)
    else:
        currentSpeed = startInvaderSpeed

    # Move all invaders and check if any reached the edge
    reachedEdge = False
    for invader in invaders:
        invader.x += currentSpeed * invaderDirection

        # Check if this invader reached the edge
        if invader.x <= 0 or invader.x >= displayWidth - invader.width:
            reachedEdge = True

    # If edge reached, move all invaders down and reverse direction
    if reachedEdge:
        for invader in invaders:
            invader.y += 10
        invaderDirection *= -1

def checkDefenderLaserCollisions():
    """Check for collisions between defender lasers and invaders/barriers

    When a defender laser hits an invader, both are removed and score increases.
    When a defender laser hits a barrier, the laser is removed and barrier takes damage.
    """
    global score

    # Check for laser-invader collisions
    for laser in defenderLasers:
        for invader in invaders:
            if laser.getRect().colliderect(invader.getRect()):
                defenderLasers.remove(laser)
                score += invader.scoreValue  # Award points based on invader type
                invaders.remove(invader)
                break

    # Check for laser-barrier collisions
    for laser in defenderLasers:
        for barrier in barriers:
            if laser.getRect().colliderect(barrier.getRect()):
                defenderLasers.remove(laser)
                barrier.takeDamage()
                if barrier.isDestroyed():
                    barriers.remove(barrier)
                break

def checkInvaderLaserCollisions():
    """Check for collisions between invader lasers and defender/barriers

    Returns:
        "defender hit" if defender is hit by a laser, None otherwise
    """
    # Check for laser-barrier collisions
    for laser in invaderLasers:
        for barrier in barriers:
            if laser.getRect().colliderect(barrier.getRect()):
                invaderLasers.remove(laser)
                barrier.takeDamage()
                if barrier.isDestroyed():
                    barriers.remove(barrier)
                break

    # Check for laser-defender collisions (game over condition)
    for laser in invaderLasers:
        if laser.getRect().colliderect(defender.getRect()):
            return "defender hit"

    return None

def checkInvaderCollisions():
    """Check for collisions between invaders and defender/barriers

    If invaders reach the defender or barriers, they are destroyed.

    Returns:
        "defender hit" if invader collides with defender, None otherwise
    """
    # Check for invader-barrier collisions
    for invader in invaders:
        for barrier in barriers:
            if invader.getRect().colliderect(barrier.getRect()):
                invaders.remove(invader)
                barrier.takeDamage()
                if barrier.isDestroyed():
                    barriers.remove(barrier)
                break

    # Check for invader-defender collisions (game over condition)
    for invader in invaders:
        if invader.getRect().colliderect(defender.getRect()):
            return "defender hit"

    return None

def checkVictory():
    """Check if the player has won by destroying all invaders

    Returns:
        True if all invaders are destroyed, False otherwise
    """
    if len(invaders) == 0:
        return True
    return False

def respawnDefender():
    """Respawn the defender at the starting position and clear all lasers

    Called when the defender is hit. Resets defender position and clears
    all active lasers from the screen.
    """
    global defender, defenderLasers, invaderLasers

    # Reset defender position to centre bottom
    defender.x = displayWidth // 2 - defender.width // 2
    defender.y = displayHeight - defender.height - 20

    # Clear all lasers from screen
    defenderLasers.clear()
    invaderLasers.clear()

def resetGame():
    """Reset all game state for a new game

    Called when restarting after game over. Reinitialises all game objects,
    score, lives, and invader movement.
    """
    global score, lives, victory, defender, defenderLasers, invaders, invaderLasers, barriers, invaderDirection

    # Reset score and lives
    score = 0
    lives = 3
    victory = False

    # Reset defender
    chosenDefender = random.choice(list(defenderTypes.keys()))
    defenderConfig = defenderTypes[chosenDefender]
    defender = Defender(
        name = chosenDefender,
        x = displayWidth // 2 - defenderConfig["width"] // 2,
        y = displayHeight - 80,
        spriteFile = defenderConfig["spriteFile"],
        laserColour = defenderConfig["laserColour"],
        laserSpeed = defenderConfig["laserSpeed"],
        laserWidth = defenderConfig["laserWidth"],
        laserHeight = defenderConfig["laserHeight"],
        width = defenderConfig["width"],
        speed = defenderConfig["speed"]
    )
    defenderLasers = []

    # Reset invaders
    invaders = []
    for row in range(invaderRows):
        for column in range(invaderColumns):
            invaderX = invaderStartX + (column * invaderSpacing)
            invaderY = invaderStartY + (row * 80)
            chosenInvader = random.choice(list(invaderTypes.keys()))
            invaderConfig = invaderTypes[chosenInvader]
            invader = Invader(
                name = chosenInvader,
                x = invaderX,
                y = invaderY,
                spriteFile = invaderConfig["spriteFile"],
                laserColour = invaderConfig["laserColour"],
                laserSpeed = invaderConfig["laserSpeed"],
                laserWidth = invaderConfig["laserWidth"],
                laserHeight = invaderConfig["laserHeight"],
                scoreValue = invaderConfig["scoreValue"],
                width = invaderConfig["width"],
                height = invaderConfig["height"]
            )
            invaders.append(invader)
    invaderLasers = []
    invaderDirection = 1

    # Reset barriers
    barriers = []
    for i in range(4):
        chosenBarrier = random.choice(list(barrierTypes.keys()))
        barrierConfig = barrierTypes[chosenBarrier]
        barrierX = 100 + (i * barrierSpacing)
        barrier = Barrier(
            name = chosenBarrier,
            x = barrierX,
            y = barrierY,
            spriteFile = barrierConfig["spriteFile"],
            width = barrierConfig["width"],
            height = barrierConfig["height"]
        )
        barriers.append(barrier)

# ============================================================================
# MAIN GAME LOOP
# ============================================================================

# Initialise display and game clock
screen = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Doctor Who Space Invasion")
clock = pygame.time.Clock()

running = True
while running:
    # Event handling - process user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Handle start screen
            if gameState == "start":
                if event.key == pygame.K_SPACE:
                    gameState = "playing"
            # Handle game over screen
            elif gameState == "gameover":
                if event.key == pygame.K_SPACE:
                    # Restart game - reset all game state
                    resetGame()
                    gameState = "playing"
                elif event.key == pygame.K_ESCAPE:
                    running = False
            # Handle gameplay
            elif gameState == "playing":
                # Handle key presses
                if event.key == pygame.K_LEFT:
                    defender.moveLeft = True
                elif event.key == pygame.K_RIGHT:
                    defender.moveRight = True
                elif event.key == pygame.K_SPACE:
                    # Fire defender laser
                    laserX, laserY = defender.getLaserStart()
                    laser = Laser(
                        x=laserX,
                        y=laserY,
                        speed=defender.laserSpeed,
                        colour=defender.laserColour,
                        width=defender.laserWidth,
                        height=defender.laserHeight
                    )
                    defenderLasers.append(laser)
        elif event.type == pygame.KEYUP:
            # Handle key releases (only during gameplay)
            if gameState == "playing":
                if event.key == pygame.K_LEFT:
                    defender.moveLeft = False
                elif event.key == pygame.K_RIGHT:
                    defender.moveRight = False

    # Game logic - only run during gameplay
    if gameState == "playing":
        # Update game state - movement
        defender.move(displayWidth)
        moveInvaders()

        # Move defender lasers
        for laser in defenderLasers:
            laser.move()

        # Remove defender lasers that have gone off screen
        lasersToRemove = []
        for laser in defenderLasers:
            if laser.isOffScreen(displayHeight):
                lasersToRemove.append(laser)

        for laser in lasersToRemove:
            defenderLasers.remove(laser)

        # Invaders randomly fire lasers
        # Adjust fire rate based on remaining invaders to maintain consistent laser frequency
        if len(invaders) > 0:
            adjustedFireRate = invaderFireRate * (totalInvaders / len(invaders))
            adjustedFireRate = min(adjustedFireRate, 0.3)  # Cap at 50% chance per invader per frame
        else:
            adjustedFireRate = invaderFireRate

        for invader in invaders:
            if random.random() < adjustedFireRate:
                laserX = invader.x + invader.width // 2
                laserY = invader.y + invader.height
                laser = Laser(
                    x=laserX,
                    y=laserY,
                    speed=invader.laserSpeed,
                    colour=invader.laserColour,
                    width=invader.laserWidth,
                    height=invader.laserHeight
                )
                invaderLasers.append(laser)

        # Move invader lasers
        for laser in invaderLasers:
            laser.move()

        # Remove invader lasers that have gone off screen
        lasersToRemove = []
        for laser in invaderLasers:
            if laser.isOffScreen(displayHeight):
                lasersToRemove.append(laser)

        for laser in lasersToRemove:
            invaderLasers.remove(laser)

        # Collision detection
        checkDefenderLaserCollisions()

        # Check if defender was hit by invader laser
        laserResult = checkInvaderLaserCollisions()
        if laserResult == "defender hit":
            lives -= 1
            print(f"Defender hit by invader laser! Lives remaining: {lives}")
            if lives > 0:
                respawnDefender()
            else:
                print(f"Game Over! Final Score: {score}")
                victory = False
                gameState = "gameover"
            continue

        # Check if defender was hit by invader
        invaderResult = checkInvaderCollisions()
        if invaderResult == "defender hit":
            lives -= 1
            print(f"Defender hit by invader! Lives remaining: {lives}")
            if lives > 0:
                respawnDefender()
            else:
                print(f"Game Over! Final Score: {score}")
                victory = False
                gameState = "gameover"
            continue

        # Check for victory condition
        if checkVictory():
            print(f"Victory! All invaders destroyed! Final Score: {score}")
            victory = True
            gameState = "gameover"
            continue

    # Rendering - draw based on game state
    if gameState == "start":
        drawStartScreen(screen, displayWidth, displayHeight, backgroundStars, invaderTypes, gameDirectory)
    elif gameState == "playing":
        screen.fill(black)

        # Animate and draw starfield background
        animateStars(backgroundStars, displayWidth, displayHeight)
        drawStars(screen, backgroundStars)

        # Draw game objects
        defender.draw(screen)

        for invader in invaders:
            invader.draw(screen)

        for laser in defenderLasers:
            laser.draw(screen)

        for laser in invaderLasers:
            laser.draw(screen)

        for barrier in barriers:
            barrier.draw(screen)

        # Draw score and lives
        scoreText = font.render(f"Score: {score}", True, white)
        screen.blit(scoreText, (10, 10))

        livesText = font.render(f"Lives: {lives}", True, white)
        screen.blit(livesText, (displayWidth - 150, 10))
    elif gameState == "gameover":
        drawGameOverScreen(screen, displayWidth, displayHeight, backgroundStars, score, victory)

    # Update display and maintain frame rate
    pygame.display.flip()
    clock.tick(fps)

# Clean up and exit
pygame.quit()
sys.exit()
