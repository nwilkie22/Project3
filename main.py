# Rubiks Cube Project
import pygame, sys


from RubiksCube import RubiksCube

pygame.font.init()
def draw_button(screen, text, button_x, button_y):
    button_color = (255, 99, 71)
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 50)
    button_width = len(text)*20
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

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

        # temp code for testing rotationsr
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                cube.sliceMove("S", 0)
                print("pressed")
            if event.key == pygame.K_e:
                cube.sliceMove("E", 0)
                print("pressed")

    screen.fill(background_color)
    cube.draw(screen)
    algo1 = draw_button(screen, "Algorithm 1", 280, 600)
    algo2 = draw_button(screen, "Algorithm 2", 50, 600)
    scramble = draw_button(screen, "Scramble", 510, 600)
    pygame.display.flip()
cube.printfaces()
pygame.quit()