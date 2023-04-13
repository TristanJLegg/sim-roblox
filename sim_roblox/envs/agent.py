import pygame

class Agent:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.color = pygame.Color.b # blue

    def draw(self, win):
        if not self.eaten:
            pygame.draw.rect(win, self.color, (self.x * 10, self.y * 10, 10, 10))

    def reset(self):
        self.eaten = False