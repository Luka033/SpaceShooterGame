import pygame
import os
import random
from pygame import mixer
from ships import *


pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "enemy_red.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "enemy_green.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "enemy_blue.png"))

# Player player
PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship2.png"))

# Lasers
PLAYER_LASER = pygame.image.load(os.path.join("assets", "player_laser.png"))

RED_LASER = pygame.image.load(os.path.join("assets", "red_laser.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "green_laser.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "blue_laser.png"))

# Explosions
EXPLOSION = pygame.image.load(os.path.join("assets", "explosion.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space-bg.gif")), (WIDTH, HEIGHT))

# Lives
LIVES = pygame.image.load(os.path.join("assets", "health.png"))

num_times_lost = 0

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def game_loop():
    bgY = 0
    bgY2 = -BG.get_height()
    explosion_flag = False
    damage_flag = True

    run = True
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    enemies = []
    wave_length = 5
    enemy_vel = int(1)
    laser_vel = 5
    player_laser_vel = 8
    player_vel = 5
    enemy_range = -1500

    player = Player(300, 630)
    lost = False

    def redraw_window():
        # draw background
        WIN.blit(BG, (0, bgY))
        WIN.blit(BG, (0, bgY2))
        # draw text
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        # draw lives
        for i in range(lives):
            WIN.blit(LIVES, (i * 35 + 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        if explosion_flag:
            explosion = Enemy(explosion_x - 20, explosion_y - 20, "explosion")
            explosion.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        # animate moving background
        bgY += 0.7
        bgY2 += 0.7
        if bgY > BG.get_height():
            bgY = -BG.get_height()
        if bgY2 > BG.get_height():
            bgY2 = -BG.get_height()
        # check if player lost the game
        if lives < 0:
            lost = True
        # check if player lost a life
        elif player.health <= 0:
            player.health = 100
            lives -= 1
            os.system("afplay assets/lose_life.wav&")
            damage_flag = True

        if lost:
            os.system("afplay assets/you_lost.wav&")
            run = False
            global num_times_lost
            num_times_lost += 1
            pygame.mixer.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # if level is over, increase difficulty
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            player.health = 100
            enemy_vel += int(0.2)
            enemy_range -= 150
            if level > 1:
                os.system("afplay assets/level_completed2.wav&")
                if level % 5 == 0:
                    # reward player with a life every 5 levels
                    lives += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(enemy_range, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        explosion_flag, explosion_x, explosion_y = player.move_lasers(-player_laser_vel, enemies)

        if player.health == 10 and damage_flag:
            os.system("afplay assets/severe_damage.wav&")
            damage_flag = False

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 3 * 90) == 1:
                if enemy.y > 0:
                    enemy.shoot()

            if collide(enemy, player):
                os.system("afplay assets/explosion.wav&")
                player.health -= 10

                # TODO add explosion
                explosion_flag = True
                explosion_x = enemy.x
                explosion_y = enemy.y
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                player.health -= 10
                enemies.remove(enemy)

        redraw_window()



if __name__ == '__main__':
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        if num_times_lost < 1:
            title_label = title_font.render("Press to begin...", 1, (255, 255, 255))
        else:
            title_label = title_font.render("Press to Play Again", 1, (255, 255, 255))

        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mixer.init()
                mixer.music.load('assets/engine.wav')
                pygame.mixer.music.set_volume(0.6)
                mixer.music.play(-1)
                game_loop()
    pygame.quit()


