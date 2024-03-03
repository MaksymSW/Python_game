import random
import os
import time
from datetime import datetime

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()
# Константы - ЗАГЛАВНЫЕ БУКВЫ
HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)
FONT_1 = pygame.font.SysFont('Comic Sans', 100)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_ORANGE = (255, 102, 0)
COLOR_RED = (150, 0, 24)


main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
# Создание игрока
player_size = (20, 20)
# player = pygame.Surface(player_size)
player = pygame.image.load('player.png').convert_alpha() 
# player.fill(COLOR_BLACK)
# размещение на поле, по умолчанию (0, 0)
# player_rect = player.get_rect()
# player_rect = pygame.Rect(0, random.randint(0, HEIGHT), *player_size)
player_rect = player.get_rect(center = (350, 450))
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]


# def - создание функции
def create_enemy():
    
    # Создание врага
    # enemy_size = (30, 30)
    
    # enemy = pygame.Surface(enemy_size)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_size = enemy.get_size()
    # enemy.fill(COLOR_BLUE)
    # размещение на поле с заданными координатами
    # enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(15, HEIGHT - 15), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

# Создание константы(заглавные буквы), создание User Event
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)


def create_bonus():
    
    # Создание бонуса
    # bonus_size = (35, 35)
    # bonus = pygame.Surface(bonus_size)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_size = bonus.get_size()
    # bonus.fill(COLOR_ORANGE)
    # размещение на поле с заданными координатами
    # bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_rect = pygame.Rect(random.randint(25, WIDTH - 25), 0, *bonus_size) #сузить коридор появления бонусов
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

# Создание константы(заглавные буквы), создание User Event
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)



enemies = []
bonuses = []

score = 0

image_index = 0

playing = True



while playing:
    FPS.tick(120)


    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False

        if event.type == CREATE_ENEMY:
           enemies.append(create_enemy())
   
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index +=1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    
    
    # main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()  

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    
    
    
    keys = pygame.key.get_pressed() # клавиша нажата

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)



    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1]) # отображение объекта на мониторе

        if player_rect.colliderect(enemy[1]):

            playing = False

            main_display.blit(FONT_1.render(str("GAME OVER"), True, COLOR_RED), (WIDTH - 900, 200))
            pygame.display.flip() # забывает обновить кадр
            pygame.time.delay(2000) # задержка на 2 секунды
            exit() # прерывает выполниение программы


    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1]) # отображение объекта на мониторе

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))




    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)  # Размещение на поле
    

 

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))


    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))


