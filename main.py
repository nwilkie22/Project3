# Rubiks Cube Project
import pygame

background_color = (255, 255, 255)

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Rubiks Cube Solver')

screen.fill(background_color)

pygame.display.update()

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False