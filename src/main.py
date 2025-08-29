import pygame, sys
from settings import WIDTH, HEIGHT, FPS, CAPTION, DARK
from level import Level
from ui import HUD

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    level = Level()
    hud = HUD()

    running = True
    while running:
        dt = clock.tick(FPS)
        events = []
        for event in pygame.event.get():
            events.append(event)
            if event.type == pygame.QUIT:
                running = False

        # Logic
        level.update(events)

        # Render
        level.draw(screen)
        hud.draw(screen, coins=level.player.coins, health=level.player.health)

        # Slow pause when dying (demo)
        if level.player.health <= 0:
            font = pygame.font.SysFont("arial", 36, bold=True)
            txt = font.render("Game Over - Press R", True, (255, 230, 230))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//3))
            pygame.display.flip()
            # Press R to restart
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                level = Level()
        # Victory when no enemies
        elif len(level.enemies) == 0:
            font = pygame.font.SysFont("arial", 36, bold=True)
            txt = font.render("You won! Press R to restart", True, (200, 255, 200))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//3))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                level = Level()
        else:
            pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()