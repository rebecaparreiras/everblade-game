import pygame
from settings import WHITE, BLACK

class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 22, bold=True)

    def draw(self, screen, coins, health):
        txt = self.font.render(f"Coins: {coins}   HP: {health}", True, WHITE)
        outline = self.font.render(f"Coins: {coins}   HP: {health}", True, BLACK)
        screen.blit(outline, (22, 22))
        screen.blit(txt, (20, 20))