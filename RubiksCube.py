import pygame
import random

# define colors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
colorList = [BLUE, GREEN, YELLOW, ORANGE, WHITE, RED]

# define adjacent faces
adjacent_faces = {
    0: [4, 1, 5, 3],  # Left face: Up, Front, Down, Back
    1: [4, 0, 5, 2],  # Front face: Up, Left, Down, Right
    2: [4, 3, 5, 1],  # Right face: Up, Back, Down, Front
    3: [4, 2, 5, 0],  # Back face: Up, Right, Down, Left
    4: [3, 2, 1, 0],  # Up face: Back, Right, Front, Left
    5: [1, 2, 3, 0]  # Down face: Front, Right, Back, Left
}

# define face indices
face_indices = {
    "Left": 0,
    "Front": 1,
    "Right": 2,
    "Back": 3,
    "Up": 4,
    "Down": 5
}

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

        print(self.faces)


    def recalculate_faces(self):
        # L -> B
        for i in range(4):
            self.faces[i].xpos = self.xpos + i * self.size * 3
            self.faces[i].ypos = self.ypos

        # up
        self.faces[4].xpos = self.xpos + self.size * 3
        self.faces[4].ypos = self.ypos - self.size * 3

        # down
        self.faces[5].xpos = self.xpos + self.size * 3
        self.faces[5].ypos = self.ypos + self.size * 3

        for face in self.faces:
            face.recalculate_squares()

    def draw(self, screen):
        for face in self.faces:
            face.drawFace(screen)

    def cubeRotation(self, rotation_type, direction):
        if rotation_type == "x":  # Rotating around the x-axis
            if direction == 0:  # X
                new_order = [self.faces[0], self.faces[5], self.faces[2], self.faces[4],
                             self.faces[1], self.faces[3]]
            elif direction == 1:  # X'
                new_order = [self.faces[0], self.faces[4], self.faces[2], self.faces[5],
                             self.faces[3], self.faces[1]]
            else:
                raise ValueError("Invalid direction")

        elif rotation_type == "y":  # Rotating around the y-axis
            if direction == 0:  # Y
                new_order = [1, 2, 3, 0, 4, 5]
            elif direction == 1:  # Y'
                new_order = [3, 0, 1, 2, 4, 5]
            else:
                raise ValueError("Invalid direction.")

        elif rotation_type == "z":  # Rotating around the z-axis
            if direction == 0:  # Z
                new_order = [5, 1, 4, 3, 0, 2]
            elif direction == 1:  # Z'
                new_order = [4, 1, 5, 3, 2, 0]
            else:
                raise ValueError("Invalid direction.")

        else:
            raise ValueError("Invalid rotation type.")

        self.faces = new_order

        self.recalculate_faces()

    def squareSwap(self, colors_to_move, squares_to_move_to):
        temp = [squares_to_move_to[0].color, squares_to_move_to[1].color, squares_to_move_to[2].color]
        for i in range(3):
            squares_to_move_to[i].color = colors_to_move[i]
        return temp

    def rotateSquares(self, face, direction):
        # 0: clockwise 1: counter-clockwise
        if direction == 0:
            new_order = [face.squares[2], face.squares[5], face.squares[8], face.squares[1],
                         face.squares[4], face.squares[7], face.squares[0], face.squares[3],
                         face.squares[6]]
        elif direction == 1:
            new_order = [face.squares[6], face.squares[3], face.squares[0], face.squares[7],
                         face.squares[4], face.squares[1], face.squares[8], face.squares[5],
                         face.squares[2]]
        else:
            raise ValueError("Invalid direction.")
            
        face.squares = new_order
        self.recalculate_faces

    def faceTurn(self, direction):

        current_face = self.faces[1]

        side_face = self.faces[2]
        colors_to_move = [side_face.squares[0].color, side_face.squares[1].color, side_face.squares[2].color]

        # part 1
        if direction == 0:
            self.rotateSquares(current_face, 0)
            next_face = self.faces[5]
        elif direction == 1:
            next_face = self.faces[4]
            self.rotateSquares(current_face, 1)
        else:
            raise ValueError("Invalid direction.")

        if direction == 0:
            squares_to_move_to = [next_face.squares[0], next_face.squares[3], next_face.squares[6]]
        if direction == 1:
            squares_to_move_to = [next_face.squares[2], next_face.squares[5], next_face.squares[8]]
        colors_to_move = self.squareSwap(colors_to_move, squares_to_move_to)

        # part 2
        next_face = self.faces[0]
        squares_to_move_to = [next_face.squares[6], next_face.squares[7], next_face.squares[8]]
        colors_to_move = self.squareSwap(colors_to_move, squares_to_move_to)

        # part 3
        if direction == 0:
            next_face = self.faces[4]
        else:
            next_face = self.faces[5]

        if direction == 0:
            squares_to_move_to = [next_face.squares[2], next_face.squares[5], next_face.squares[8]]
        if direction == 1:
            squares_to_move_to = [next_face.squares[0], next_face.squares[3], next_face.squares[6]]
        colors_to_move = self.squareSwap(colors_to_move, squares_to_move_to)

        # part 4
        next_face = self.faces[2]
        squares_to_move_to = [next_face.squares[0], next_face.squares[1], next_face.squares[2]]
        self.squareSwap(colors_to_move, squares_to_move_to)

        # ensure that colors are updated correctly
        self.recalculate_faces()

    # def faceRotate(self, move):
        # if(move == "U"):
        #     self.cubeRotation("x", 1)
        #     self.faceTurn(0)
        #     self.cubeRotation("x", 0)

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
                square = Square(self.xpos + j * self.size, self.ypos + i * self.size, self.size, self.initial_color)
                self.squares.append(square)

    def recalculate_squares(self):
        count = 0
        for square in self.squares:
            # print("Square: " + str(count) + " xpos: " + str(square.xpos), " count // 3: " + str(count // 3) + " calculated xpos: " + str(self.xpos + (count // 3) * self.size))
            square.xpos = self.xpos + (count // 3) * self.size
            square.ypos = self.ypos + (count % 3) * self.size
            count += 1

    # draws a 3x3 face
    def drawFace(self, screen):
        top_left_x = self.squares[0].xpos
        top_left_y = self.squares[0].ypos

        for square in self.squares:
            square.drawSquare(screen)

        # draw the outline
        big_rect = pygame.Rect(top_left_x, top_left_y, self.size * 3, self.size * 3)
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

    def recolor(self, color):
        self.color = color