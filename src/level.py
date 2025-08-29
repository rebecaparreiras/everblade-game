import pygame
from settings import TILE_SIZE, WIDTH, HEIGHT, SKY
from tiles import Tile
from entities import Player, Enemy, Coin

def _extract_platform_segments(tiles_group):
    # Gets horizontal segments per line
    by_row = {}
    for t in tiles_group:
        by_row.setdefault(t.rect.y, []).append(t.rect)
    segments = []
    for y, rects in by_row.items():
        rects = sorted(rects, key=lambda r: r.x)
        start = rects[0].x
        end = rects[0].right
        for r in rects[1:]:
            if r.x == end:
                end = r.right
            else:
                segments.append(pygame.Rect(start, y, end - start, rects[0].height))
                start, end = r.x, r.right
        segments.append(pygame.Rect(start, y, end - start, rects[0].height))
    return segments

LEVEL_MAP = [
    "                                                     ",
    "                                                     ",
    "                                                     ",
    "                                                     ",
    "                                                     ",
    "                           XXXXXXXXX                 ",
    "                                     XXX      CCC    ",
    "              C     C                  CC   XXXXXXX  ",
    "       CCC  XXXXX XXXXX   CCC     XXX XXXX           ",  
    "      XXXXX             XXXXXXX                      ",  
    "   P    C                 CCC                        ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

# Simple camera following the player
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.Vector2(0, 0)
        self.half_w = WIDTH // 2
        self.half_h = HEIGHT // 2
        self.bg_color = SKY

    def custom_draw(self, surface, target_rect):
        self.offset.x = target_rect.centerx - self.half_w
        self.offset.y = target_rect.centery - self.half_h

        surface.fill(self.bg_color)

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_rect = sprite.rect.copy()
            offset_rect.topleft -= self.offset
            surface.blit(sprite.image, offset_rect)

class Level:
    def __init__(self):
        self.camera = CameraGroup()
        self.tiles = pygame.sprite.Group()       
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.player = None
        self.build()

        # After building tiles, creates enemies per platform (except ground level)
        segments = _extract_platform_segments(self.tiles)
        ground_y = max(seg.y for seg in segments) if segments else 999999

        for seg in segments:
            if seg.y >= ground_y:   # skips ground level
                continue
            # An enemy at the center of each segment
            enemy_x = seg.centerx - 16  
            enemy_y = seg.top - 32      
            enemy = Enemy((enemy_x, enemy_y), (seg.left, seg.right))
            self.enemies.add(enemy)
            self.camera.add(enemy)

    def build(self):
        for row_idx, row in enumerate(LEVEL_MAP):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if cell == "X":
                    tile = Tile(x, y)
                    self.tiles.add(tile)
                    self.camera.add(tile)
                elif cell == "P":
                    self.player = Player((x, y - 20), [self.camera], self.tiles)
                elif cell == "E":
                    enemy = Enemy((x, y - 16), (x - 80, x + 120))
                    self.enemies.add(enemy)
                    self.camera.add(enemy)
                elif cell == "C":
                    coin = Coin((x, y))
                    self.coins.add(coin)
                    self.camera.add(coin)

    def update(self, events):
        self.camera.update()

        # Coin 
        for coin in list(self.coins):
            if self.player.rect.colliderect(coin.rect):
                coin.kill()
                self.coins.remove(coin)
                self.player.coins += 1
                # optional sound here

        # Attack
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_k:
                if self.player.try_attack():
                    hitbox = self.player.attack_rect()
                    for enemy in list(self.enemies):
                        if hitbox.colliderect(enemy.rect):
                            enemy.kill()
                            self.enemies.remove(enemy)

        # Damage
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.health = max(0, self.player.health - 1)
                # Pull
                if self.player.rect.centerx < enemy.rect.centerx:
                    self.player.rect.x -= 20
                else:
                    self.player.rect.x += 20

    def draw(self, screen):
        self.camera.custom_draw(screen, self.player.rect)