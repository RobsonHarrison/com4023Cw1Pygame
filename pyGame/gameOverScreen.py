"""
Game Over Screen Module

Displays the game over screen with final score and restart option.
"""

import pygame
from background import animateStars, drawStars

# ============================================================================
# SCREEN RENDERING
# ============================================================================

def drawGameOverScreen(screen, displayWidth, displayHeight, backgroundStars, finalScore, victory):
    """Draw the game over screen with final score and restart option
    
    Args:
        screen: Pygame surface to draw on
        displayWidth: Width of the display
        displayHeight: Height of the display
        backgroundStars: List of star dictionaries for background
        finalScore: The player's final score
        victory: True if player won, False if player lost
    """
    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    gold = (255, 215, 0)
    red = (255, 50, 50)
    
    # Fonts
    titleFont = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 48)
    smallFont = pygame.font.Font(None, 32)
    
    screen.fill(black)

    # Animate and draw starfield background
    animateStars(backgroundStars, displayWidth, displayHeight)
    drawStars(screen, backgroundStars)
    
    # Draw title based on victory or defeat
    if victory:
        titleText = titleFont.render("VICTORY!", True, gold)
        messageText = font.render("All Invaders Destroyed!", True, white)
    else:
        titleText = titleFont.render("GAME OVER", True, red)
        messageText = font.render("The Invaders Won", True, white)
    
    titleRect = titleText.get_rect(center=(displayWidth // 2, 150))
    screen.blit(titleText, titleRect)
    
    messageRect = messageText.get_rect(center=(displayWidth // 2, 230))
    screen.blit(messageText, messageRect)
    
    # Draw final score
    scoreText = font.render(f"Final Score: {finalScore}", True, white)
    scoreRect = scoreText.get_rect(center=(displayWidth // 2, 320))
    screen.blit(scoreText, scoreRect)
    
    # Draw restart instructions
    restartText = smallFont.render("Press SPACE to Play Again", True, white)
    restartRect = restartText.get_rect(center=(displayWidth // 2, 420))
    screen.blit(restartText, restartRect)
    
    quitText = smallFont.render("Press ESC to Quit", True, white)
    quitRect = quitText.get_rect(center=(displayWidth // 2, 470))
    screen.blit(quitText, quitRect)

