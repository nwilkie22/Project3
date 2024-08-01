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

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Rubiks Cube Solver')

screen.fill(background_color)

cube = RubiksCube(100,100)
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

            if event.key == pygame.K_SPACE:
                prime = not prime
                if prime:
                    print("Prime")
                else:
                    print("Not Prime")

            if event.key == pygame.K_u:
                if prime == False:
                    cube.faceTurn("U")
                    print("pressed")
                else:
                    cube.faceTurn("U'")

            if event.key == pygame.K_d:
                if prime == False:
                    cube.faceTurn("D")
                    print("pressed")
                else:
                    cube.faceTurn("D'")

            if event.key == pygame.K_l:
                if prime == False:
                    cube.faceTurn("L")
                    print("pressed")
                else:
                    cube.faceTurn("L'")

            if event.key == pygame.K_r:
                if prime == False:
                    cube.faceTurn("R")
                    print("pressed")
                else:
                    cube.faceTurn("R'")

            if event.key == pygame.K_f:
                if prime == False:
                    cube.faceTurn("F")
                    print("pressed")
                else:
                    cube.faceTurn("F'")

            # for debugging step by step
            if event.key == pygame.K_1:
                cube.cubeRotation("y", 1)

            if event.key == pygame.K_2:
                cube.rotation(0)

            if event.key == pygame.K_3:
                cube.cubeRotation("y", 0)



    screen.fill(background_color)
    cube.draw(screen)
    algo1 = draw_button(screen, "Algorithm 1", 280, 600)
    algo2 = draw_button(screen, "Algorithm 2", 50, 600)
    scramble = draw_button(screen, "Scramble", 510, 600)
    pygame.display.flip()

pygame.quit()