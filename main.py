# Rubiks Cube Project
import pygame, sys


from RubiksCube import RubiksCube

pygame.font.init()
def draw_button(screen, text, button_x, button_y):
    button_color = (255, 99, 71)
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 50)
    button_width = 150
    button_height = 75
    button_surface = pygame.Surface((button_width, button_height))
    button_surface.fill(button_color)
    text_surface = font.render(text, True, text_color)
    text_x = (button_width - text_surface.get_width()) // 2
    text_y = (button_height - text_surface.get_height()) // 2
    # Blit the text surface onto the button surface
    button_surface.blit(text_surface, (text_x, text_y))
    button_surface.blit(text_surface, (100, 100))
    b = screen.blit(button_surface, (button_x, button_y))
    return b

background_color = (255, 255, 255)

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Rubiks Cube Solver')

screen.fill(background_color)

cube = RubiksCube(100,100)
print(cube.isSolved())
algo1 = draw_button(screen, "Algorithm 1", 300, 600)
algo2 = draw_button(screen, "Algorithm 2", 50, 600)
scramble = draw_button(screen, "Scramble", 500, 600)

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    cube.draw(screen)
    pygame.display.flip()
pygame.quit()

