"""
Start Screen Module

Displays the start screen with game title, instructions, and invader information.
"""

import pygame
import os
import random

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def animateStars(backgroundStars, displayWidth, displayHeight):
    """Animate the starfield background by making stars twinkle and drift

    Args:
        backgroundStars: List of star dictionaries to animate
        displayWidth: Width of the display
        displayHeight: Height of the display
    """
    for star in backgroundStars:
        # Random chance to change brightness (twinkling effect)
        if random.random() < 0.05:  # 5% chance per frame
            star['brightness'] = random.randint(100, 255)

        # Slowly drift stars downwards
        star['y'] += star['size'] * 0.2

        # Wrap stars around when they go off screen
        if star['y'] > displayHeight:
            star['y'] = 0
            star['x'] = random.randint(0, displayWidth)

# ============================================================================
# SCREEN RENDERING
# ============================================================================

def drawStartScreen(screen, displayWidth, displayHeight, backgroundStars, invaderTypes, gameDirectory):
    """Draw the start screen with title, instructions, and invader information

    Args:
        screen: Pygame surface to draw on
        displayWidth: Width of the display
        displayHeight: Height of the display
        backgroundStars: List of star dictionaries for background
        invaderTypes: Dictionary of invader configurations
        gameDirectory: Path to game directory for loading sprites
    """
    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Fonts
    font = pygame.font.Font(None, 36)
    smallFont = pygame.font.Font(None, 28)

    screen.fill(black)

    # Animate and draw starfield background
    animateStars(backgroundStars, displayWidth, displayHeight)
    for star in backgroundStars:
        starColour = (star['brightness'], star['brightness'], star['brightness'])
        pygame.draw.circle(screen, starColour, (int(star['x']), int(star['y'])), star['size'])

    # Load and draw game logo
    logoPath = os.path.join(gameDirectory, "assets/gameLogo.png")
    logo = pygame.image.load(logoPath)
    # Scale logo down from 1024x1024 to 250x250 to fit nicely on screen
    scaledLogo = pygame.transform.scale(logo, (250, 250))
    logoRect = scaledLogo.get_rect(center=(displayWidth // 2, 150))
    screen.blit(scaledLogo, logoRect)

    # Draw invader information header
    invaderHeaderY = 290
    invaderHeaderText = font.render("INVADERS:", True, white)
    invaderHeaderRect = invaderHeaderText.get_rect(center=(displayWidth // 2, invaderHeaderY))
    screen.blit(invaderHeaderText, invaderHeaderRect)

    # Draw each invader type with sprite and score
    invaderInfoY = 330
    invaderSpacing = 55
    xPosition = displayWidth // 2 - 100

    for invaderName, invaderConfig in invaderTypes.items():
        # Load and draw invader sprite
        spritePath = os.path.join(gameDirectory, invaderConfig["spriteFile"])
        sprite = pygame.image.load(spritePath)
        scaledSprite = pygame.transform.scale(sprite, (40, 40))
        screen.blit(scaledSprite, (xPosition, invaderInfoY))

        # Draw invader name and score
        nameText = smallFont.render(f"{invaderName}", True, white)
        screen.blit(nameText, (xPosition + 60, invaderInfoY))

        scoreText = smallFont.render(f"{invaderConfig['scoreValue']} points", True, white)
        screen.blit(scoreText, (xPosition + 60, invaderInfoY + 20))

        invaderInfoY += invaderSpacing

    # Draw start prompt with extra spacing
    startText = font.render("Press SPACE to Start", True, white)
    startRect = startText.get_rect(center=(displayWidth // 2, invaderInfoY + 50))
    screen.blit(startText, startRect)

