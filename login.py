# login.py
import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Login - Space Invader")
# login screen
def login_screen():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsansms", 50, bold=True)
    small_font = pygame.font.SysFont("comicsansms", 24)
    input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 60)
    username = ""
    active = True

    # Create stars for background
    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(100)]

    glow_color = (0, 255, 255)  # initial glow color
    glow_direction = 1

    while active:
        screen.fill((5, 5, 25))  # dark space background

        # Move stars
        for star in stars:
            star[1] += star[2]
            if star[1] > HEIGHT:
                star[0] = random.randint(0, WIDTH)
                star[1] = 0
                star[2] = random.randint(1, 3)
            pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), star[2])

        # Animate glowing input box
        glow_color = (0, 200 + 55 * glow_direction, 255)
        if glow_color[1] >= 255:
            glow_direction = -1
        elif glow_color[1] <= 200:
            glow_direction = 1

        pygame.draw.rect(screen, glow_color, input_box, 4, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), input_box.inflate(-4, -4), border_radius=12)  # inner dark fill

        # Title
        title_surface = font.render("SPACE INVADER LOGIN", True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 120))
        screen.blit(title_surface, title_rect)

        # Show username inside the rectangle
        user_surface = font.render(username, True, (255, 255, 255))
        # Ensure text stays inside the box
        text_rect = user_surface.get_rect(midleft=(input_box.x + 10, input_box.centery))
        screen.blit(user_surface, text_rect)

        # Hint text
        hint = small_font.render("Press Enter to Start", True, (200, 200, 200))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 80))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username != "":
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 12:
                    username += event.unicode

        pygame.display.update()
        clock.tick(60)