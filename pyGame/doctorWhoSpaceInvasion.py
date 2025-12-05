import pygame
import sys

pygame.init()

displayWidth = 800
displayHeight = 600
fps = 60

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