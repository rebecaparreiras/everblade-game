import pygame
from settings import TILE_SIZE, GREEN

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        super().__init__()
        height = 20  # platform height
        if image:
            self.image = pygame.transform.scale(image, (TILE_SIZE, height))
        else:
            self.image = pygame.Surface((TILE_SIZE, height))
            self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))