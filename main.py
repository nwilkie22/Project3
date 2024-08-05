# Rubiks Cube Project
import pygame, sys
import kociemba
from RubiksCube import RubiksCube

pygame.font.init()


def draw_button(screen, text, button_x, button_y):
    button_color = (255, 99, 71)
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 50)
    button_width = len(text) * 25
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


def draw_text(surface, text, font, color, pos):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    b = surface.blit(text_surface, text_rect)
    return b

def draw():
    screen.fill(background_color)
    cube.draw(screen)
    draw_button(screen, "Kociemba", 250, 600)
    draw_button(screen, "Other", 50, 600)
    draw_button(screen, "Scramble", 510, 600)
    draw_text(screen, title_text, big_font, text_color_black, (400, 30))
    draw_text(screen, text, font, text_color_black, (185, 520))
    draw_text(screen, alg_log_text, font, text_color_black, (185, 180))
    pygame.display.flip()


background_color = (255, 255, 255)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Rubiks Cube Solver')

# setup move log text vars
font = pygame.font.Font(None, 50)
big_font = pygame.font.Font(None, 75)
text_color_black = (0, 0, 0)
text = ""
title_text = "Rubiks Cube Solver"
alg_log_text = ""

screen.fill(background_color)

cube = RubiksCube(50, 300)
print(cube.isSolved())
active = True
prime = False

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

        # temp code for testing rotations
        # Press key for rotation, press space to switch from prime to not prime
        if event.type == pygame.KEYDOWN:
            alg_log_text = ""
            # Prime toggle
            if event.key == pygame.K_SPACE:
                prime = not prime
                if prime:
                    print("Prime")
                else:
                    print("Not Prime")
            # Basic moves
            if event.key == pygame.K_u:
                if prime == False:
                    text = cube.faceTurn("U")
                else:
                    text = cube.faceTurn("U'")

            if event.key == pygame.K_d:
                if prime == False:
                    text = cube.faceTurn("D")
                else:
                    text = cube.faceTurn("D'")

            if event.key == pygame.K_l:
                if prime == False:
                    text = cube.faceTurn("L")
                else:
                    text = cube.faceTurn("L'")

            if event.key == pygame.K_r:
                if prime == False:
                    text = cube.faceTurn("R")
                else:
                    text = cube.faceTurn("R'")

            if event.key == pygame.K_f:
                if prime == False:
                    text = cube.faceTurn("F")
                else:
                    text = cube.faceTurn("F'")

            if event.key == pygame.K_b:
                if prime == False:
                    text = cube.faceTurn("B")
                else:
                    text = cube.faceTurn("B'")

            if event.key == pygame.K_x:
                if prime == False:
                    cube.cubeRotation("x", 0)
                else:
                    cube.cubeRotation("x", 1)
            if event.key == pygame.K_y:
                if prime == False:
                    cube.cubeRotation("y", 0)
                else:
                    cube.cubeRotation("y", 1)
            if event.key == pygame.K_z:
                if prime == False:
                    cube.cubeRotation("z", 0)
                else:
                    cube.cubeRotation("z'", 1)
            if event.key == pygame.K_k:
                if prime == False:
                    cube.rotation(0)
                else:
                    cube.rotation(1)
            if event.key == pygame.K_o:
                cube.percentSolved()

            # Slice moves
            if event.key == pygame.K_s:
                cube.faceTurn("S")
            if event.key == pygame.K_m:
                cube.faceTurn("M")
            if event.key == pygame.K_e:
                cube.faceTurn("E")
            if event.key == pygame.K_p:
                cube.solve_cube(screen)
                print(cube.solve_cube(screen))
            check = cube.stringify()
            print(check)
            # Wide moves
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Buttons
            mouse_x, mouse_y = event.pos
            if scramble.collidepoint(mouse_x, mouse_y):
                cube.scramble()
                alg_log_text = "Scrambled"
            if kociemba.collidepoint(mouse_x, mouse_y):
                alg_log_text = "Running Kociemba"
                draw()
                cube.solve_cube(screen)
            if other.collidepoint(mouse_x, mouse_y):
                alg_log_text = "Running Other"
                draw()
                cube.algo1("white_cross", screen)
        if cube.isSolved():
            alg_log_text = "Solved"

    screen.fill(background_color)
    cube.draw(screen)
    kociemba = draw_button(screen, "Kociemba", 250, 600)
    other = draw_button(screen, "Other", 50, 600)
    scramble = draw_button(screen, "Scramble", 510, 600)
    title = draw_text(screen, title_text, big_font, text_color_black, (400, 30))
    move_log = draw_text(screen, text, font, text_color_black, (185, 520))
    alg_log = draw_text(screen, alg_log_text, font, text_color_black, (185, 180))
    pygame.display.flip()

pygame.quit()
