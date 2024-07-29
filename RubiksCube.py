import pygame
import random

# define colors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
colorList = [BLUE, GREEN, YELLOW, RED, WHITE, ORANGE]

class RubiksCube(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, size = 30):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        # stores all the face objects in this order
        # "left", "front", "right", "back", "up", "down"
        self.faces = []
        self.init_faces()

    def init_faces(self):

        temp_color_list = colorList

        # L -> B faces
        for i in range(4):
            color = temp_color_list.pop()
            # we need to loop this 6 times changing the position as required for the six faces
            face = Face(self.xpos + i * self.size * 3, self.ypos, self.size, color)
            self.faces.append(face)

        # up face
        color = temp_color_list.pop()
        face = Face(self.xpos + self.size * 3, self.ypos - self.size * 3, self.size, color)
        self.faces.append(face)

        # down face
        color = temp_color_list.pop()
        face = Face(self.xpos + self.size * 3, self.ypos + self.size * 3, self.size, color)
        self.faces.append(face)

    def draw(self, screen):
        for face in self.faces:
            face.drawFace(screen)

    def isSolved(self):
        for face in self.faces:
            for square in face.squares:
                test_color = face.squares[0].color
                if square.color != test_color:
                    return False
        return True


class Face(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, size, initial_color):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.initial_color = initial_color
        self.squares = []
        self.init_squares()

    def init_squares(self):
        color = self.initial_color
        for i in range(3):
            for j in range(3):
                # square creation
                square = Square(self.xpos + i * self.size, self.ypos + j * self.size, self.size, self.initial_color)
                self.squares.append(square)

    # draws a 3x3 face
    def drawFace(self, screen):
        for square in self.squares:
            square.drawSquare(screen)

        # draw the outline
        big_rect = pygame.Rect(self.xpos, self.ypos, self.size * 3, self.size * 3)
        pygame.draw.rect(screen, (0, 0, 0), big_rect, 2)

class Square(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.color = color

    def drawSquare(self, screen):

        rect = pygame.Rect(self.xpos, self.ypos, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
