import pygame

# view
WIDTH, HEIGHT = 960, 540 
FPS = 60
CAPTION = "Everblade"

# world
TILE_SIZE = 48
GRAVITY = 0.5
MOVE_SPEED = 4
JUMP_FORCE = -10

# colors (placeholders)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (109, 170, 255)
GREEN = (80, 200, 120)
GOLD = (255, 208, 0)
RED = (220, 70, 70)
DARK = (30, 30, 40)

# control
KEY_LEFT = pygame.K_a
KEY_RIGHT = pygame.K_d
KEY_JUMP = pygame.K_SPACE
KEY_ATTACK = pygame.K_k