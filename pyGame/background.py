"""
Background Module

Handles animated starfield background shared across all game screens.
"""

import pygame
import random

# ============================================================================
# BACKGROUND ANIMATION
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

def drawStars(screen, backgroundStars):
    """Draw the animated starfield background
    
    Args:
        screen: Pygame surface to draw on
        backgroundStars: List of star dictionaries to draw
    """
    for star in backgroundStars:
        starColour = (star['brightness'], star['brightness'], star['brightness'])
        pygame.draw.circle(screen, starColour, (int(star['x']), int(star['y'])), star['size'])

