import pygame
import random as rd

class Stars:
    def __init__(self, quantity, screen_size):
        self.screen_size = screen_size
        self.star_list = []

        for _ in range(quantity):
            x = rd.randint(0, screen_size[0])
            y = rd.randint(0, screen_size[1])

            shine = rd.randint(150, 255)
            size = rd.choice([1,1,2])

            self.star_list.append([x,y,shine,size])

    def draw(self, screen):
        for star in self.star_list:
            x,y,shine,size = star
            pygame.draw.circle(screen, (shine, shine, shine), (x,y), size)