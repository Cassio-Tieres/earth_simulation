import pygame
import random as rd
import math

class Stars:
    def __init__(self, quantity, screen_size):
        self.screen_size = screen_size
        self.star_list = []

        for _ in range(quantity):
            x = rd.randint(0, screen_size[0])
            y = rd.randint(0, screen_size[1])

            shine = rd.randint(150, 255)
            size = rd.choice([1,1,2])

            # define shines
            offset = rd.uniform(0, 2 * math.pi)
            pulse_velocity = rd.uniform(0.01, 0.1)

            self.star_list.append([x,y,shine,size,offset,pulse_velocity])

    def draw(self, screen):
        for star in self.star_list:
            star[4] += star[5]
            oscilation = math.sin(star[4]) * 50
            current_shine = max(50, min(255, star[2] + oscilation))
            color = (current_shine, current_shine, current_shine)
            pygame.draw.circle(screen, color, (star[0], star[1]), star[3])