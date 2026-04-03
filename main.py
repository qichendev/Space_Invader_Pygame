# main.py
import asyncio
import math
import random
import time

import pygame
from pygame import mixer

from login import login_screen

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_START_X = 370
PLAYER_START_Y = 480
PLAYER_SPEED = 5
BULLET_START_Y = 480
BULLET_SPEED = 10
ENEMY_COUNT = 6
ENEMY_SPEED = 4
ENEMY_DROP = 40
POWERUP_SPEED = 3
POWERUP_DURATION = 5
SPECIAL_BULLET_RANGE = 50
COLLISION_RADIUS = 27
PLAYER_BOUNDARY = 736


async def run_game(screen, username):
    pygame.display.set_caption("Space Invader")
    icon = pygame.image.load("ufo.png")
    pygame.display.set_icon(icon)

    background = pygame.image.load("background.png")
    mixer.music.load("background.ogg")
    mixer.music.play(-1)

    laser_sound = mixer.Sound("laser.ogg")
    explosion_sound = mixer.Sound("explosion.ogg")

    font = pygame.font.Font("freesansbold.ttf", 32)
    over_font = pygame.font.Font("freesansbold.ttf", 64)

    playerImg = pygame.image.load("player.png")
    bulletImg = pygame.image.load("bullet.png")
    enemyImg = [pygame.image.load("enemy.png") for _ in range(ENEMY_COUNT)]

    def make_enemy_positions():
        return (
            [random.randint(0, PLAYER_BOUNDARY) for _ in range(ENEMY_COUNT)],
            [random.randint(50, 150) for _ in range(ENEMY_COUNT)],
            [ENEMY_SPEED for _ in range(ENEMY_COUNT)],
            [ENEMY_DROP for _ in range(ENEMY_COUNT)],
        )

    def make_powerup_position():
        return random.randint(50, 750), random.randint(50, 300)

    def initial_state():
        ex, ey, exc, eyc = make_enemy_positions()
        px, py = make_powerup_position()
        return {
            "playerX": PLAYER_START_X,
            "playerX_change": 0,
            "bulletX": 0,
            "bulletY": BULLET_START_Y,
            "bullet_state": "ready",
            "score": 0,
            "lives": 3,
            "enemyX": ex,
            "enemyY": ey,
            "enemyX_change": exc,
            "enemyY_change": eyc,
            "powerupX": px,
            "powerupY": py,
            "special_bullet_active": False,
            "special_bullet_end_time": 0,
            "game_over": False,
            "paused": False,
        }

    state = initial_state()
    clock = pygame.time.Clock()

    def isCollision(ex, ey, bx, by):
        return math.sqrt((ex - bx) ** 2 + (ey - by) ** 2) < COLLISION_RADIUS

    def show_ui():
        top_color = (255, 100, 0) if state["special_bullet_active"] else (50, 50, 50)
        pygame.draw.rect(screen, top_color, (0, 0, SCREEN_WIDTH, 50))
        screen.blit(font.render(f"Score: {state['score']}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Player: {username}", True, (255, 255, 0)), (550, 10))
        screen.blit(font.render(f"Lives: {state['lives']}", True, (255, 0, 0)), (350, 10))

    def game_over_text():
        screen.blit(over_font.render("GAME OVER", True, (255, 255, 255)), (200, 250))
        screen.blit(font.render("Press R to Restart", True, (200, 200, 0)), (270, 350))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state["paused"] = not state["paused"]
                if event.key == pygame.K_r and state["game_over"]:
                    state = initial_state()
                if not state["paused"] and not state["game_over"]:
                    if event.key == pygame.K_LEFT:
                        state["playerX_change"] = -PLAYER_SPEED
                    if event.key == pygame.K_RIGHT:
                        state["playerX_change"] = PLAYER_SPEED
                    if event.key == pygame.K_SPACE and state["bullet_state"] == "ready":
                        state["bulletX"] = state["playerX"]
                        state["bullet_state"] = "fire"
                        laser_sound.play()

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    state["playerX_change"] = 0

        if not state["paused"] and not state["game_over"]:
            # Player movement
            state["playerX"] = max(
                0, min(state["playerX"] + state["playerX_change"], PLAYER_BOUNDARY)
            )

            # Enemies
            for i in range(ENEMY_COUNT):
                state["enemyX"][i] += state["enemyX_change"][i]
                if state["enemyX"][i] <= 0:
                    state["enemyX_change"][i] = ENEMY_SPEED
                    state["enemyY"][i] += state["enemyY_change"][i]
                elif state["enemyX"][i] >= PLAYER_BOUNDARY:
                    state["enemyX_change"][i] = -ENEMY_SPEED
                    state["enemyY"][i] += state["enemyY_change"][i]

                # Bullet collision
                if state["bullet_state"] == "fire":
                    hit = False
                    if state["special_bullet_active"]:
                        hit = abs(state["enemyX"][i] - state["bulletX"]) < SPECIAL_BULLET_RANGE
                    else:
                        hit = isCollision(
                            state["enemyX"][i], state["enemyY"][i],
                            state["bulletX"], state["bulletY"],
                        )
                    if hit:
                        explosion_sound.play()
                        state["score"] += 1
                        state["enemyX"][i] = random.randint(0, PLAYER_BOUNDARY)
                        state["enemyY"][i] = random.randint(50, 150)
                        state["bulletY"] = BULLET_START_Y
                        state["bullet_state"] = "ready"

                # Enemy reaches bottom
                if state["enemyY"][i] > 440:
                    state["lives"] -= 1
                    state["enemyX"][i] = random.randint(0, PLAYER_BOUNDARY)
                    state["enemyY"][i] = random.randint(50, 150)
                    if state["lives"] <= 0:
                        state["game_over"] = True

                screen.blit(enemyImg[i], (state["enemyX"][i], state["enemyY"][i]))

            # Bullet movement
            if state["bulletY"] <= 0:
                state["bulletY"] = BULLET_START_Y
                state["bullet_state"] = "ready"
            if state["bullet_state"] == "fire":
                screen.blit(bulletImg, (state["bulletX"] + 16, state["bulletY"] + 10))
                state["bulletY"] -= BULLET_SPEED

            # Power-up
            state["powerupY"] += POWERUP_SPEED
            pygame.draw.rect(screen, (0, 255, 255), (state["powerupX"], state["powerupY"], 30, 30))
            if state["powerupY"] > SCREEN_HEIGHT:
                state["powerupX"], state["powerupY"] = make_powerup_position()
            player_dist = math.sqrt(
                (state["powerupX"] - state["playerX"]) ** 2
                + (state["powerupY"] - PLAYER_START_Y) ** 2
            )
            if player_dist < 40:
                state["special_bullet_active"] = True
                state["special_bullet_end_time"] = time.time() + POWERUP_DURATION
                state["powerupX"], state["powerupY"] = make_powerup_position()

            # Expire special bullet
            if state["special_bullet_active"] and time.time() > state["special_bullet_end_time"]:
                state["special_bullet_active"] = False

        screen.blit(playerImg, (state["playerX"], PLAYER_START_Y))
        show_ui()
        if state["game_over"]:
            game_over_text()

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    username = await login_screen(screen)
    await run_game(screen, username)


asyncio.run(main())
