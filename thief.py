import pygame


class Thief:

    def __init__(self, gameDisplay, width, height):
        self.DISPLAY = gameDisplay
        self.WIDTH = width
        self.HEIGHT = height

        self.IMG = pygame.image.load('pics/thief.png')
        self.IMG = pygame.transform.scale(self.IMG, (self.WIDTH, self.HEIGHT))

    def draw(self, x, y):
        self.DISPLAY.blit(self.IMG, (x * self.WIDTH, y * self.HEIGHT))
