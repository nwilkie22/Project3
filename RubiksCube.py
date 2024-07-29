import pygame

# define colors
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
RED = (255, 0, 0)
Orange = (255, 128, 0)
White = (255, 255, 255)

class RubiksCube(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos, size = 30):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.size = size
        self.face = ["up", "down", "left", "right", "front", "back"]



    def draw(self, screen):
        # draws a face
        for i in range(3):
            for j in range(3):
                rect = pygame.Rect(self.xpos + i * self.size, self.ypos + j * self.size,self.size,self.size)
                pygame.draw.rect(screen, RED, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
