import pygame
import os, sys

# For .exe paths
def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# View
WIDTH, HEIGHT = 960, 540 
FPS = 60
CAPTION = "Everblade"

# World
TILE_SIZE = 48
GRAVITY = 0.5
MOVE_SPEED = 4
JUMP_FORCE = -11

# Colors (placeholders)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (109, 170, 255)
GREEN = (80, 200, 120)
GOLD = (255, 208, 0)
RED = (220, 70, 70)
DARK = (30, 30, 40)

# Control
KEY_LEFT = pygame.K_a
KEY_RIGHT = pygame.K_d
KEY_JUMP = pygame.K_SPACE
KEY_ATTACK = pygame.K_k

# Assets' folders
ASSETS_DIR = "src/assets"
IMG_DIR = os.path.join(ASSETS_DIR, "images")
SND_DIR = os.path.join(ASSETS_DIR, "sounds")