import pygame

class Earth:
    def __init__(self, rotation_v, radius, center):
        self.rotation_v = rotation_v
        self.radius = radius
        self.center = center
        self.x_map = 0
        try:
            # upload earth image
            self.map = pygame.image.load("imgs/mapa_mundi.jpg").convert()
            self.map = pygame.transform.scale(self.map, (self.radius * 4, self.radius * 2))
        except Exception as e:
            self.map = pygame.Surface((self.radius * 4, self.radius * 2))
            self.map.fill((30,144,255))
            pygame.draw.rect(self.map, (34, 139, 34), (50,50,100,100))


        self.e_width = self.map.get_width() // 2
        self.alpha_mask = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.alpha_mask, (255, 255, 255, 255), (self.radius, self.radius), self.radius)
    
    # create earth
    def create_earth(self):
        # update rotation position
        self.x_map -= self.rotation_v
        if self.x_map <= (-self.e_width * 2):
            self.x_map = 0
        
        earth_frame = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

        earth_frame.blit(self.map, (self.x_map + 2, 0))
        earth_frame.blit(self.map, (self.x_map + self.e_width + self.radius * 2, 0))
        earth_frame.blit(self.alpha_mask, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
        return earth_frame