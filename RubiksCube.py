import pygame
import kociemba
import random
import time

# define colors
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
colorList = [YELLOW, WHITE, BLUE, RED, GREEN, ORANGE]

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

MOVE_REVERSALS = {
    "U": "U'",
    "U'": "U",
    "D": "D'",
    "D'": "D",
    "L": "L'",
    "L'": "L",
    "R": "R'",
    "R'": "R",
    "F": "F'",
    "F'": "F",
    "B": "B'",
    "B'": "B",
}


def kociemba_solver(cube):
    # Convert the cube state to a string format that kociemba can solve
    cube_state = cube.stringify()
    solution = kociemba.solve(cube_state)
    solution_steps = solution.split()
    return solution_steps


class RubiksCube(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, size=30):
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

        # self.faces[4].squares[2].recolor(RED)
        # self.faces[0].squares[1].recolor(RED)
        # self.faces[1].squares[1].recolor(RED)
        # self.faces[2].squares[1].recolor(RED)
        # self.faces[3].squares[1].recolor(RED)

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
        # does not move any squares in relation to each other
        # just changes which face is at the front
        # 3 rotation types: x: R direction, y: U direction, and z: F direction
        # 2 directions: 0: Normal Direction, 1: Prime Direction
        # initial order: 0, 1, 2, 3, 4, 5

        # rotation types
        if rotation_type == "x":  # Rotating around the x-axis
            if direction == 0:  # X
                new_order = [0, 5, 2, 4, 1, 3]
            elif direction == 1:  # X'
                new_order = [0, 4, 2, 5, 3, 1]
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

        # reorder the "faces" array to reflect the rotation
        new_faces = []
        for num in new_order:
            new_faces.append(self.faces[num])
        self.faces = new_faces

        if rotation_type == "x":
            if direction == 0:
                rotations = [(0, 1), (2, 0), (3, 1), (3, 1), (5, 1), (5, 1)]
                for current_face, orientation in rotations:
                    self.faceRotate(self.faces[current_face], orientation)
            if direction == 1:
                rotations = [(0, 0), (2, 1), (3, 1), (3, 1), (4, 1), (4, 1)]
                for current_face, orientation in rotations:
                    self.faceRotate(self.faces[current_face], orientation)
        if rotation_type == "y":
            if direction == 0:
                rotations = [(4, 0), (5, 1)]
                for current_face, orientation in rotations:
                    self.faceRotate(self.faces[current_face], orientation)
            if direction == 1:
                rotations = [(4, 1), (5, 0)]
                for current_face, orientation in rotations:
                    self.faceRotate(self.faces[current_face], orientation)
        if rotation_type == "z":
            if direction == 0:
                rotations = [(0, 1), (2, 0), (4, 0), (5, 0), (1, 0), (3, 1)]
                for current_face, orientation in rotations:
                    self.faceRotate(self.faces[current_face], orientation)
            if direction == 1:
                rotations = [(0, 1), (2, 1), (4, 1), (5, 1)]
                for current_face, orientation in rotations:
                    self.faceRotate(self.faces[current_face], orientation)

        self.recalculate_faces()

    def squareSwap(self, colors_to_move, squares_to_move_to, swapped):
        temp = [squares_to_move_to[0].color, squares_to_move_to[1].color, squares_to_move_to[2].color]
        for i in range(3):
            squares_to_move_to[i].color = colors_to_move[i]
        if swapped:
            temp2 = squares_to_move_to[0].color
            squares_to_move_to[0].color = squares_to_move_to[2].color
            squares_to_move_to[2].color = temp2
        return temp

    def faceRotate(self, face, direction):
        # 0: clockwise 1: counter-clockwise
        if direction == 0:
            new_order = [2, 5, 8, 1, 4, 7, 0, 3, 6]
        elif direction == 1:
            new_order = [6, 3, 0, 7, 4, 1, 8, 5, 2]
        else:
            raise ValueError("Invalid direction.")

        new_squares = []

        for num in new_order:
            new_squares.append(face.squares[num])

        face.squares = new_squares

    def rotation(self, direction):

        current_face = self.faces[1]
        if direction == 0:
            self.faceRotate(current_face, 0)
        elif direction == 1:
            self.faceRotate(current_face, 1)
        else:
            raise ValueError("Invalid direction")

        side_face = self.faces[2]
        colors_to_move = [side_face.squares[0].color, side_face.squares[1].color, side_face.squares[2].color]
        if direction == 0:
            next_face = self.faces[5]
            move_to = [next_face.squares[0], next_face.squares[3], next_face.squares[6]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[2]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[0]
            colors_to_move = temp

            next_face = self.faces[0]
            move_to = [next_face.squares[6], next_face.squares[7], next_face.squares[8]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[0]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[2]
            colors_to_move = temp

            next_face = self.faces[4]
            move_to = [next_face.squares[2], next_face.squares[5], next_face.squares[8]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[2]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[0]
            colors_to_move = temp

            next_face = self.faces[2]
            move_to = [next_face.squares[0], next_face.squares[1], next_face.squares[2]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[0]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[2]

        if direction == 1:
            next_face = self.faces[4]
            move_to = [next_face.squares[2], next_face.squares[5], next_face.squares[8]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[0]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[2]
            colors_to_move = temp

            next_face = self.faces[0]
            move_to = [next_face.squares[6], next_face.squares[7], next_face.squares[8]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[2]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[0]
            colors_to_move = temp

            next_face = self.faces[5]
            move_to = [next_face.squares[0], next_face.squares[3], next_face.squares[6]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[0]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[2]
            colors_to_move = temp

            next_face = self.faces[2]
            move_to = [next_face.squares[0], next_face.squares[1], next_face.squares[2]]
            temp = [move_to[0].color, move_to[1].color, move_to[2].color]
            move_to[0].color = colors_to_move[2]
            move_to[1].color = colors_to_move[1]
            move_to[2].color = colors_to_move[0]

        self.recalculate_faces()

    def faceTurn(self, rotation_type):
        if rotation_type == "U":
            self.cubeRotation("x", 1)
            self.rotation(0)
            self.cubeRotation("x", 0)

        elif rotation_type == "U'":
            self.cubeRotation("x", 1)
            self.rotation(1)
            self.cubeRotation("x", 0)
        elif rotation_type == "U2":
            self.cubeRotation("x", 1)
            self.rotation(0)
            self.rotation(0)
            self.cubeRotation("x", 0)

        elif rotation_type == "D":
            self.cubeRotation("x", 0)
            self.rotation(0)
            self.cubeRotation("x", 1)
        elif rotation_type == "D'":
            self.cubeRotation("x", 0)
            self.rotation(1)
            self.cubeRotation("x", 1)
        elif rotation_type == "D2":
            self.cubeRotation("x", 0)
            self.rotation(0)
            self.rotation(0)
            self.cubeRotation("x", 1)

        elif rotation_type == "L":
            self.cubeRotation("y", 1)
            self.rotation(0)
            self.cubeRotation("y", 0)
        elif rotation_type == "L'":
            self.cubeRotation("y", 1)
            self.rotation(1)
            self.cubeRotation("y", 0)
        elif rotation_type == "L2":
            self.cubeRotation("y", 1)
            self.rotation(0)
            self.rotation(0)
            self.cubeRotation("y", 0)

        elif rotation_type == "R":
            self.cubeRotation("y", 0)
            self.rotation(0)
            self.cubeRotation("y", 1)
        elif rotation_type == "R'":
            self.cubeRotation("y", 0)
            self.rotation(1)
            self.cubeRotation("y", 1)
        elif rotation_type == "R2":
            self.cubeRotation("y", 0)
            self.rotation(0)
            self.rotation(0)
            self.cubeRotation("y", 1)

        elif rotation_type == "F":
            self.rotation(0)
        elif rotation_type == "F'":
            self.rotation(1)
        elif rotation_type == "F2":
            self.rotation(0)
            self.rotation(0)
        elif rotation_type == "B":
            self.cubeRotation("x", 1)
            self.cubeRotation("x", 1)
            self.rotation(0)
            self.cubeRotation("x", 0)
            self.cubeRotation("x", 0)
        elif rotation_type == "B'":
            self.cubeRotation("x", 1)
            self.cubeRotation("x", 1)
            self.rotation(1)
            self.cubeRotation("x", 0)
            self.cubeRotation("x", 0)
        elif rotation_type == "B2":
            self.cubeRotation("x", 1)
            self.cubeRotation("x", 1)
            self.rotation(0)
            self.rotation(0)
            self.cubeRotation("x", 0)
            self.cubeRotation("x", 0)
        if rotation_type == "S":
            self.faceTurn("F'")
            self.faceTurn("B")
            self.cubeRotation("z", 0)
        if rotation_type == "M":
            self.faceTurn("L'")
            self.faceTurn("R")
            self.cubeRotation("x", 1)
        if rotation_type == "E":
            self.faceTurn("D'")
            self.faceTurn("U")
            self.cubeRotation("y", 1)

        return rotation_type

    # HELPER FUNCTIONS
    def printfaces(self):
        for face in self.faces:
            print(face.squares[0].color)

    def isSolved(self):
        for face in self.faces:
            for square in face.squares:
                test_color = face.squares[0].color
                if square.color != test_color:
                    return False
        return True

    def scramble(self):
        possible_moves = ["U", "U'", "D", "D'", "L", "L'", "R", "R'", "F", "F'", "B", "B'"]
        for i in range(random.randint(200, 500)):
            random_element = random.choice(possible_moves)
            self.faceTurn(random_element)

    def stringify(self):
        position_order = [
            # Up
            (4, 0), (4, 3), (4, 6),
            (4, 1), (4, 4), (4, 7),
            (4, 2), (4, 5), (4, 8),
            # Left
            (2, 0), (2, 3), (2, 6),
            (2, 1), (2, 4), (2, 7),
            (2, 2), (2, 5), (2, 8),
            # Front
            (1, 0), (1, 3), (1, 6),
            (1, 1), (1, 4), (1, 7),
            (1, 2), (1, 5), (1, 8),
            # Right
            (5, 0), (5, 3), (5, 6),
            (5, 1), (5, 4), (5, 7),
            (5, 2), (5, 5), (5, 8),
            # Back
            (0, 0), (0, 3), (0, 6),
            (0, 1), (0, 4), (0, 7),
            (0, 2), (0, 5), (0, 8),
            # Down
            (3, 0), (3, 3), (3, 6),
            (3, 1), (3, 4), (3, 7),
            (3, 2), (3, 5), (3, 8),
        ]
        color_map = {
            (0, 255, 0): "F",  # Green
            (0, 0, 255): "B",  # Blue
            (255, 255, 0): "D",  # Yellow
            (255, 0, 0): "R",  # Red
            (255, 128, 0): "L",  # Orange
            (255, 255, 255): "U"  # White
        }
        cube = ""
        for face_idx, square_idx in position_order:
            face = self.faces[face_idx]
            square = face.squares[square_idx]
            cube += color_map[square.color]
        return cube

    def solve_cube(self, screen):
        solution_steps = kociemba_solver(self)
        for step in solution_steps:
            print(step)
            self.faceTurn(step)
            self.draw(screen)
            pygame.display.flip()
            pygame.time.wait(500)
            if (self.stringify() == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"):
                break

    def percentSolved(self):
        total = 0.0

        for face in self.faces:
            middle_color = face.squares[4].color
            unsolved_count = sum(1 for square in face.squares if square.color != middle_color)
            face_percentage = unsolved_count / 9
            total += face_percentage

        average_percentage = total / 9
        return 1 - average_percentage

    def whiteCross(self):
        count = 0.0
        arr = [1, 3, 5, 7]
        for i in arr:
            if self.faces[4].squares[i].color == WHITE:
                count += 1.0
        if self.faces[0].squares[3].color == ORANGE:
            count += 1.0
        if self.faces[1].squares[3].color == GREEN:
            count += 1.0
        if self.faces[2].squares[3].color == RED:
            count += 1.0
        if self.faces[3].squares[3].color == BLUE:
            count += 1.0
        return count / 8

    def reverse_move(self, move):
        result = MOVE_REVERSALS[move]
        return result

    def generate_random_sequence(self, length):
        possible_moves = ["U", "D", "L", "R", "F", "B", "U'", "D'", "L'", "R'", "F'", "B'"]
        return [random.choice(possible_moves) for _ in range(length)]

    def sequence(self, sequence):
        for move in sequence:
            self.faceTurn(move)

    def best_sequence(self, sequence, screen):
        for move in sequence:
            self.draw(screen)
            pygame.display.flip()
            pygame.time.wait(100)
            self.faceTurn(move)

    def reverse_sequence(self, sequence):
        # Apply the moves in reverse order to undo the sequence
        for move in reversed(sequence):
            self.faceTurn(self.reverse_move(move))

    def algo1(self, screen):
        self.solve_white_cross(screen)
        self.solve_white_corners(screen)
        self.second_layer(screen)
        self.yellow_cross(screen)

    def solve_white_cross(self, screen):
        percent_solved = self.whiteCross()
        count = 1
        max_attempts = 2000  # max attempt number

        while percent_solved < 1.0:
            time.sleep(1)
            print("Round: " + str(count) + " percent_solved: " + str(percent_solved))

            attempt_count = 0
            best_percent = percent_solved
            best_sequence = None

            while attempt_count < max_attempts:
                # max random sequence length
                sequence_length = random.randint(1, 20)
                sequence = self.generate_random_sequence(sequence_length)

                self.sequence(sequence)
                new_percent = self.whiteCross()

                if new_percent > best_percent:
                    best_percent = new_percent
                    best_sequence = sequence

                self.reverse_sequence(sequence)

                attempt_count += 1

            if best_sequence:
                print(best_sequence)
                # Apply the best sequence found
                self.best_sequence(best_sequence, screen)
                percent_solved = best_percent
                print("Best sequence applied with improved percent_solved: " + str(percent_solved))
            else:
                print("No improvement found in this round.")

            count += 1

        if percent_solved >= 1.0:
            print("Solved")
        else:
            print("Failed")

    def solve_white_corners(self, screen):
        def update_cube():
            self.draw(screen)
            pygame.display.flip()
            pygame.time.wait(100)

        def corner_alg():
            self.faceTurn("R'")
            update_cube()
            self.faceTurn("D'")
            update_cube()
            self.faceTurn("R")
            update_cube()
            self.faceTurn("D")
            update_cube()

        def corner_fix_alg():
            self.faceTurn("D'")
            update_cube()
            self.faceTurn("R'")
            update_cube()
            self.faceTurn("D")
            update_cube()
            self.faceTurn("R")
            update_cube()


        def white_face_create():
            print("Moving White Squares to the Top")
            count = 0
            count2 = 0
            count3 = 0
            while (self.faces[4].squares[0].color != WHITE or self.faces[4].squares[2].color != WHITE or
                   self.faces[4].squares[6].color != WHITE or self.faces[4].squares[8].color != WHITE) and (count3 < 3):
                while(self.faces[4].squares[8].color == WHITE and count2 < 4):
                    self.cubeRotation("y",0)
                    update_cube()
                    count2 += 1
                count2 = 0
                if self.faces[2].squares[2].color == WHITE:
                    if self.faces[4].squares[8].color != WHITE:
                        corner_alg()
                if self.faces[5].squares[6].color == WHITE:
                    if self.faces[4].squares[8].color != WHITE:
                        for _ in range(3):
                            corner_alg()
                if self.faces[1].squares[8].color == WHITE:
                    if self.faces[4].squares[8].color != WHITE:
                        for _ in range(5):
                            corner_alg()
                if count < 4:
                    self.faceTurn("D")
                    count += 1
                else:
                    self.cubeRotation("y",0)
                    count = 0
                update_cube()
                count3 += 1


        def white_corner_fix():
            print("Fixing Corners")
            count4 = 0
            while count4 < 3:
                count5 = 0
                while self.faces[4].squares[8].color != WHITE and count5 < 4:
                    self.cubeRotation("y", 0)
                    update_cube()
                    count5 += 1
                if (self.faces[1].squares[6].color != self.faces[1].squares[3].color) and self.faces[4].squares[8].color == WHITE:
                    corner_alg()
                    if self.faces[2].squares[2].color != self.faces[2].squares[4].color:
                        self.faceTurn("D")
                        update_cube()
                        self.cubeRotation("y", 0)
                    elif self.faces[3].squares[2].color != self.faces[3].squares[4].color:
                        self.faceTurn("D")
                        update_cube()
                        self.cubeRotation("y", 0)
                        self.cubeRotation("y", 0)
                    elif self.faces[0].squares[2].color != self.faces[0].squares[4].color:
                        self.faceTurn("D")
                        update_cube()
                        self.cubeRotation("y", 0)
                        self.cubeRotation("y", 0)
                        self.cubeRotation("y", 0)
                    corner_fix_alg()
                if self.faces[1].squares[6].color == self.faces[1].squares[3].color:
                    self.cubeRotation("y", 0)
                    update_cube()
                count4 += 1
                '''
                if self.faces[1].squares[8].color != self.faces[1].squares[4].color:
                    self.faceTurn("D")
                    update_cube()
                if self.faces[2].squares[8].color != self.faces[2].squares[4].color:
                    self.faceTurn("D")
                    update_cube()
                if self.faces[3].squares[8].color != self.faces[3].squares[4].color:
                    self.faceTurn("D")
                    update_cube()
                if self.faces[0].squares[8].color != self.faces[0].squares[4].color:
                    self.faceTurn("D")
                    update_cube()
                print("while loop 2")
                while self.faces[2].squares[2].color != WHITE:
                    self.cubeRotation("y",0)
                    update_cube()
                corner_fix_alg()
                '''

        def get_unstuck1():
            print("Get Unstuck Top Left")
            self.faceTurn("F")
            update_cube()
            self.faceTurn("D")
            update_cube()
            self.faceTurn("F'")
            update_cube()

        # UNSTUCK2 IS NOT TESTED
        def get_unstuck2():
            print("Get Unstuck Top Right")
            self.faceTurn("R'")
            update_cube()
            self.faceTurn("D")
            update_cube()
            self.faceTurn("R")
            update_cube()

        def is_solved():
            solved = True
            if self.faces[4].squares[0].color != WHITE:
                solved = False
            if self.faces[4].squares[2].color != WHITE:
                solved = False
            if self.faces[4].squares[6].color != WHITE:
                solved = False
            if self.faces[4].squares[8].color != WHITE:
                solved = False
            if (self.faces[0].squares[0].color or self.faces[0].squares[6].color) != self.faces[0].squares[3].color:
                solved = False
            if (self.faces[1].squares[0].color or self.faces[1].squares[6].color) != self.faces[1].squares[3].color:
                solved = False
            if (self.faces[2].squares[0].color or self.faces[2].squares[6].color) != self.faces[2].squares[3].color:
                solved = False
            if (self.faces[3].squares[0].color or self.faces[3].squares[6].color) != self.faces[3].squares[3].color:
                solved = False
            return solved

        #white_face_create()

        time.sleep(1)
        while not is_solved():
            print("White Corners Starting")
            white_face_create()
            white_corner_fix()
            if self.faces[2].squares[0].color == WHITE:
                get_unstuck1()
            if self.faces[1].squares[6].color == WHITE:
                get_unstuck2()
        print("White Corners Complete")










                    # lances code in case this ends up being better
        '''
        cube_state = self.stringify()
        white_corners = {0, 2, 6, 8}
        for corner in white_corners:
            if cube_state[corner] == "U" and not cube_state[36] == "L" or not cube_state[45] == "B":
                print()
            while corner == 0:
                if cube_state[0] == "U":
                    if cube_state[36] != "L":
                        self.faceTurn("B")
                        self.faceTurn("D")
                        self.faceTurn("B'")
                        self.faceTurn("D'")
                        cube_state = self.stringify()
                        print(cube_state)
                        print("Wrong Corner")
                    else:
                        print("Solved")
                        break
                else:
                    if (cube_state[36] == "U" and cube_state[47] == "L") or (cube_state[47] == "U" and cube_state[0] == "L"):
                        self.cubeRotation("y", 0)
                        self.cubeRotation("y", 0)
                        self.faceTurn("R'")
                        self.faceTurn("D")
                        self.faceTurn("R")
                        self.faceTurn("D'")
                        self.faceTurn("R'")
                        self.faceTurn("D")
                        self.faceTurn("R")
                        self.cubeRotation("y", 0)
                        self.cubeRotation("y", 0)
                        cube_state = self.stringify()
                        print("Rotate Corner")
                    else:
                        if (cube_state[33] == "U" and cube_state[53] == "L") or (cube_state[42] == "U" and cube_state[33] == "L") or (cube_state[53] == "U" and cube_state[42] == "L"):
                            self.cubeRotation("y", 0)
                            self.cubeRotation("y", 0)
                            self.faceTurn("R'")
                            self.faceTurn("D'")
                            self.faceTurn("R")
                            self.faceTurn("D")
                            self.cubeRotation("y", 0)
                            self.cubeRotation("y", 0)
                            cube_state = self.stringify()
                            print("Place Corner")
                        else:
                            self.faceTurn("D")
                            cube_state = self.stringify()
                            print("Find Corner")
  
        '''
    def second_layer(self, screen):
        self.cubeRotation("x", 0)
        self.cubeRotation("x", 0)
        def update_cube():
            self.draw(screen)
            pygame.display.flip()
            pygame.time.wait(100)

        def is_solved():
            solved = True
            if (self.faces[0].squares[1].color or self.faces[0].squares[7].color) != self.faces[0].squares[4].color:
                solved = False
            if (self.faces[1].squares[1].color or self.faces[0].squares[7].color) != self.faces[1].squares[4].color:
                solved = False
            if (self.faces[2].squares[1].color or self.faces[2].squares[7].color) != self.faces[2].squares[4].color:
                solved = False
            if (self.faces[3].squares[1].color or self.faces[3].squares[7].color) != self.faces[3].squares[4].color:
                solved = False
            return solved

        def left_alg():
            self.faceTurn("U'")
            update_cube()
            self.faceTurn("L'")
            update_cube()
            self.faceTurn("U")
            update_cube()
            self.faceTurn("L")
            update_cube()
            self.faceTurn("U")
            update_cube()
            self.faceTurn("F")
            update_cube()
            self.faceTurn("U'")
            update_cube()
            self.faceTurn("F'")
            update_cube()

        def right_alg():
            self.faceTurn("U")
            update_cube()
            self.faceTurn("R")
            update_cube()
            self.faceTurn("U'")
            update_cube()
            self.faceTurn("R'")
            update_cube()
            self.faceTurn("U'")
            update_cube()
            self.faceTurn("F'")
            update_cube()
            self.faceTurn("U")
            update_cube()
            self.faceTurn("F")
            update_cube()

        def wrong_orientation():
            arr = ["U", "R", "U'", "R'", "U'", "F'", "U", "F", "U", "U", "U", "R", "U'", "R'", "U'", "F'", "U", "F"]
            for element in arr:
                self.faceTurn(element)
                update_cube()

        def checkFront():
            print("Check Front")
            for i in range(4):
                for j in range(4):
                    if self.faces[1].squares[4].color == self.faces[1].squares[3].color:
                        pass
                    else:
                        self.faceTurn("U")
                        update_cube()
                    if self.faces[1].squares[4].color == self.faces[1].squares[3].color:
                        if self.faces[4].squares[5].color == self.faces[0].squares[4].color:
                            left_alg()
                            return False
                        if self.faces[4].squares[5].color == self.faces[2].squares[4].color:
                            right_alg()
                            return False
                self.cubeRotation("y", 0)
            return True

        def checkAdjacent():
            print("Check Adjacent")
            for i in range(4):
                if (self.faces[1].squares[7].color == self.faces[2].squares[4].color) and (self.faces[2].squares[1].color == self.faces[1].squares[4].color):
                    wrong_orientation()
                self.cubeRotation("y", 0)




        print("Second Layer")
        time.sleep(2)

        while not is_solved():
            checkFront()
            checkAdjacent()

        self.cubeRotation("x", 0)
        self.cubeRotation("x", 0)
        update_cube()

    def yellow_cross(self, screen):
        self.cubeRotation("x", 0)
        self.cubeRotation("x", 0)
        def update_cube():
            self.draw(screen)
            pygame.display.flip()
            pygame.time.wait(500)
        update_cube()
        def is_solved():
            solved = True
            arr = [1,3,5,7]
            for i in arr:
                if self.faces[4].squares[i].color != YELLOW:
                    solved = False
            return solved

        def cross_alg():
            print("Build Cross")
            self.faceTurn("F")
            update_cube()
            self.faceTurn("R")
            update_cube()
            self.faceTurn("U")
            update_cube()
            self.faceTurn("R'")
            update_cube()
            self.faceTurn("U'")
            update_cube()
            self.faceTurn("F'")
            update_cube()
            self.cubeRotation("y", 0)
            update_cube()
            self.cubeRotation("y", 0)
            update_cube()


        time.sleep(2)
        while not is_solved():
            cross_alg()






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