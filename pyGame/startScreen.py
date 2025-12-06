"""
Start Screen Module

Displays the start screen with game title, instructions, and invader information.
"""

import pygame
import os
from background import animateStars, drawStars

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
    drawStars(screen, backgroundStars)

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

