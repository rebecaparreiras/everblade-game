import pygame
from settings import MOVE_SPEED, JUMP_FORCE, GRAVITY, GOLD, RED, TILE_SIZE

def load_or_placeholder(path, size, color):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, solid_sprites):
        super().__init__(groups)
        self.image = load_or_placeholder("src/assets/images/player.png", (32, 40), (70, 120, 255))
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.solid_sprites = solid_sprites
        self.can_attack = True
        self.attack_cooldown = 280  #ms
        self.last_attack = 0
        self.health = 3
        self.coins = 0

    def input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel.x = -MOVE_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel.x = MOVE_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = JUMP_FORCE

    def horizontal_collisions(self):
        self.rect.x += self.vel.x
        for sprite in self.solid_sprites:
            if self.rect.colliderect(sprite.rect):
                if self.vel.x > 0:
                    self.rect.right = sprite.rect.left
                elif self.vel.x < 0:
                    self.rect.left = sprite.rect.right

    def vertical_collisions(self):
        self.vel.y += GRAVITY
        if self.vel.y > 16:
            self.vel.y = 16

        self.rect.y += self.vel.y
        self.on_ground = False
        for sprite in self.solid_sprites:
            if self.rect.colliderect(sprite.rect):
                if self.vel.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.vel.y = 0

    def attack_rect(self):
        # hitbox
        facing = 1 if self.vel.x >= 0 else -1
        return pygame.Rect(self.rect.centerx, self.rect.y+8, 30*facing, 24)

    def try_attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack >= self.attack_cooldown:
            self.last_attack = now
            return True
        return False

    def update(self):
        self.input()
        self.horizontal_collisions()
        self.vertical_collisions()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, bounds_x):
        super().__init__()
        self.image = load_or_placeholder("src/assets/images/enemy.png", (32, 32), RED)
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 2
        self.min_x, self.max_x = bounds_x
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= self.min_x or self.rect.right >= self.max_x:
            self.direction *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_or_placeholder("src/assets/images/coin.png", (20, 20), GOLD)
        self.rect = self.image.get_rect(center=(pos[0]+TILE_SIZE//2, pos[1]+TILE_SIZE//2))