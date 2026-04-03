# login.py
import pygame
import random
import asyncio

async def login_screen(screen):
    WIDTH, HEIGHT = 800, 600
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsansms", 50, bold=True)
    small_font = pygame.font.SysFont("comicsansms", 24)
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
    username = ""

    stars = [
        [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)]
        for _ in range(100)
    ]
    glow_direction = 1

    while True:
        screen.fill((5, 5, 25))

        # Animate stars
        for star in stars:
            star[1] += star[2]
            if star[1] > HEIGHT:
                star[0] = random.randint(0, WIDTH)
                star[1] = 0
                star[2] = random.randint(1, 3)
            pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), star[2])

        # Animate glowing input box
        glow_g = 200 + 55 * glow_direction
        glow_g = max(200, min(255, glow_g))
        glow_color = (0, glow_g, 255)
        if glow_g >= 255:
            glow_direction = -1
        elif glow_g <= 200:
            glow_direction = 1

        pygame.draw.rect(screen, glow_color, input_box, 4, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), input_box.inflate(-4, -4), border_radius=12)

        # Title
        title_surface = font.render("SPACE INVADER LOGIN", True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
        screen.blit(title_surface, title_rect)

        # Username text
        user_surface = font.render(username, True, (255, 255, 255))
        text_rect = user_surface.get_rect(midleft=(input_box.x + 10, input_box.centery))
        screen.blit(user_surface, text_rect)

        # Hint
        hint = small_font.render("Press Enter to Start", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username != "":
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 12:
                    username += event.unicode

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)
