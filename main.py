# Rubiks Cube Project
import pygame

from RubiksCube import RubiksCube

background_color = (255, 255, 255)

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Rubiks Cube Solver')

screen.fill(background_color)

cube = RubiksCube(100,100)
print(cube.isSolved())


active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    cube.draw(screen)
    pygame.display.flip()
pygame.quit()