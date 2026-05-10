import pygame

def screen_config():
    screen_size = (1080, 920)
    screen = pygame.display.set_mode(screen_size)
    
    pygame.init()
    pygame.display.set_caption("Earth Simulator")

    return screen