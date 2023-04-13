import pygame

class Apple:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.color = pygame.Color.r # red

    def draw(self, win):
        if not self.eaten:
            pygame.draw.rect(win, self.color, (self.x * 10, self.y * 10, 10, 10))

    def eat(self):
        self.eaten = True

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.eaten = False