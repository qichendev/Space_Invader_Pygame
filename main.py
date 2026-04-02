# main.py
import math
import random
import pygame
from pygame import mixer
from login import login_screen
import time
import sys

def run_game(username):
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Space Invader")

    # Clock for FPS control
    clock = pygame.time.Clock()
    clock.tick(60)  # Set to 60 FPS

    # Safe loading function (prevents crashes)
    def load_image(path):
        try:
            return pygame.image.load(path)
        except:
            print(f"Error loading {path}")
            sys.exit()

    icon = load_image('ufo.png')
    pygame.display.set_icon(icon)

    # Background
    background = load_image('background.png')

    try:
        mixer.music.load("background.wav")
        mixer.music.play(-1)
    except:
        print("Background music not found")

    # Fonts
    font = pygame.font.Font('freesansbold.ttf', 32)
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    # Player
    playerImg = load_image('player.png')
    playerX, playerY = 370, 480
    playerX_change = 0

    # Bullet
    bulletImg = load_image('bullet.png')
    bulletX, bulletY = 0, 480
    bulletY_change = 10
    bullet_state = "ready"

    # Enemies
    num_of_enemies = 6
    enemyImg = [load_image('enemy.png') for _ in range(num_of_enemies)]
    enemyX = [random.randint(0, 736) for _ in range(num_of_enemies)]
    enemyY = [random.randint(50, 150) for _ in range(num_of_enemies)]
    enemyX_change = [4 for _ in range(num_of_enemies)]
    enemyY_change = [40 for _ in range(num_of_enemies)]

    # Game variables
    score_value = 0
    lives = 3

    # Power-up
    powerup_active = True
    powerupX = random.randint(50, 750)
    powerupY = random.randint(50, 300)
    powerup_speed = 3
    special_bullet_active = False
    special_bullet_end_time = 0

    # UI
    def show_ui():
        top_color = (50, 50, 50)
        if special_bullet_active:
            top_color = (255, 100, 0)

        pygame.draw.rect(screen, top_color, (0, 0, 800, 50))
        screen.blit(font.render(f"Score: {score_value}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Player: {username}", True, (255, 255, 0)), (550, 10))
        screen.blit(font.render(f"Lives: {lives}", True, (255, 0, 0)), (350, 10))

    def game_over_text():
        screen.blit(over_font.render("GAME OVER", True, (255, 255, 255)), (200, 250))
        screen.blit(font.render("Press R to Restart", True, (200, 200, 0)), (270, 350))

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))

    def fire_bullet(x, y):
        nonlocal bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(ex, ey, bx, by):
        return math.sqrt((ex - bx) ** 2 + (ey - by) ** 2) < 27

    def reset_game():
        nonlocal playerX, playerX_change, bulletX, bulletY, bullet_state
        nonlocal score_value, lives
        nonlocal enemyX, enemyY, enemyX_change, enemyY_change
        nonlocal special_bullet_active, special_bullet_end_time

        playerX, playerX_change = 370, 0
        bulletX, bulletY, bullet_state = 0, 480, "ready"
        score_value, lives = 0, 3

        enemyX = [random.randint(0, 736) for _ in range(num_of_enemies)]
        enemyY = [random.randint(50, 150) for _ in range(num_of_enemies)]
        enemyX_change = [4 for _ in range(num_of_enemies)]
        enemyY_change = [40 for _ in range(num_of_enemies)]

        special_bullet_active = False
        special_bullet_end_time = 0

    running = True
    paused = False
    game_over = False

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

                if event.key == pygame.K_r and game_over:
                    reset_game()
                    game_over = False

                if not paused and not game_over:
                    if event.key == pygame.K_LEFT:
                        playerX_change = -5
                    if event.key == pygame.K_RIGHT:
                        playerX_change = 5
                    if event.key == pygame.K_SPACE and bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                        try:
                            mixer.Sound("laser.wav").play()
                        except:
                            pass

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    playerX_change = 0

        if not paused and not game_over:
            playerX += playerX_change
            playerX = max(0, min(playerX, 736))

            for i in range(num_of_enemies):
                enemyX[i] += enemyX_change[i]

                if enemyX[i] <= 0 or enemyX[i] >= 736:
                    enemyX_change[i] *= -1
                    enemyY[i] += enemyY_change[i]

                # Collision
                if bullet_state == "fire":
                    if special_bullet_active:
                        if abs(enemyX[i] - bulletX) < 50:
                            score_value += 1
                            enemyX[i] = random.randint(0, 736)
                            enemyY[i] = random.randint(50, 150)
                            bulletY = 480
                            bullet_state = "ready"
                    else:
                        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                            score_value += 1
                            enemyX[i] = random.randint(0, 736)
                            enemyY[i] = random.randint(50, 150)
                            bulletY = 480
                            bullet_state = "ready"

                # Enemy hits bottom
                if enemyY[i] > 440:
                    lives -= 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

                    if lives <= 0:
                        game_over = True

                enemy(enemyX[i], enemyY[i], i)

            # Bullet movement
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            # Power-up
            if powerup_active:
                powerupY += powerup_speed
                pygame.draw.rect(screen, (0, 255, 255), (powerupX, powerupY, 30, 30))

                if powerupY > 600:
                    powerupY = random.randint(50, 300)
                    powerupX = random.randint(50, 750)

                if math.sqrt((powerupX - playerX) ** 2 + (powerupY - playerY) ** 2) < 40:
                    special_bullet_active = True
                    special_bullet_end_time = time.time() + 5
                    powerupY = random.randint(50, 300)
                    powerupX = random.randint(50, 750)

            if special_bullet_active and time.time() > special_bullet_end_time:
                special_bullet_active = False

        player(playerX, playerY)
        show_ui()

        if game_over:
            game_over_text()

        pygame.display.update()
        clock.tick(60)  # IMPORTANT (smooth gameplay)


if __name__ == "__main__":
    username = login_screen()
    run_game(username)