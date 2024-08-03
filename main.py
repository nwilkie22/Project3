# Rubiks Cube Project
import pygame, sys
import kociemba
from RubiksCube import RubiksCube

pygame.font.init()


def draw_button(screen, text, button_x, button_y):
    button_color = (255, 99, 71)
    text_color = (255, 255, 255)
    font = pygame.font.Font(None, 50)
    button_width = len(text) * 20
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

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Rubiks Cube Solver')

screen.fill(background_color)

cube = RubiksCube(100, 100)
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
                    cube.faceTurn("U")
                else:
                    cube.faceTurn("U'")

            if event.key == pygame.K_d:
                if prime == False:
                    cube.faceTurn("D")
                else:
                    cube.faceTurn("D'")

            if event.key == pygame.K_l:
                if prime == False:
                    cube.faceTurn("L")
                else:
                    cube.faceTurn("L'")

            if event.key == pygame.K_r:
                if prime == False:
                    cube.faceTurn("R")
                else:
                    cube.faceTurn("R'")

            if event.key == pygame.K_f:
                if prime == False:
                    cube.faceTurn("F")
                else:
                    cube.faceTurn("F'")

            if event.key == pygame.K_b:
                if prime == False:
                    cube.faceTurn("B")
                else:
                    cube.faceTurn("B'")

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
            if algo1.collidepoint(mouse_x, mouse_y):
                cube.algo1()

    screen.fill(background_color)
    cube.draw(screen)
    algo1 = draw_button(screen, "Algorithm 1", 280, 600)
    algo2 = draw_button(screen, "Algorithm 2", 50, 600)
    scramble = draw_button(screen, "Scramble", 510, 600)
    pygame.display.flip()

pygame.quit()
