import pygame
from config.screen import screen_config
from classes.earth import Earth
from classes.stars import Stars

screen = screen_config()
closer = False

stars = Stars(200, (1080,920))
earth = Earth(0.5, 150, (1080, 920))

# initialization pygame
while not closer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Simulação fechada')
            closer = True
    screen.fill((0,0,0))
    stars.draw(screen)

    earth_surface = earth.create_earth()

    screen.blit(earth_surface, (1080//2 - 150, 920//2 - 150))
    
    pygame.time.wait(1)
    pygame.display.flip()

pygame.quit()