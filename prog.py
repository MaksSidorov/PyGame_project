import pygame
import os
import math
import random
from classes import *
import sys

pygame.init()

FPS = 50
pygame.display.set_caption('Balls&Blocks')
# Фоновая музыка
pygame.mixer.music.load('data//music.mp3')
pygame.mixer.music.play(-1)
sound = pygame.mixer.Sound('data//boom_sound.wav')
# размеры окна:
size = width, height = 600, 600
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
# Колисчество шариков у игрока
balls_cou = 10
balls_cou_1 = balls_cou


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Balls&Blocks", "",
                  "Правила игры",
                  "Набить максимальный счет, ",
                  "так чтобы блоки не коснулись дна",
                  "Чтобы продолжить нажмите на любую клавишу",
                  "Зеленый шарик увеличивает количкство красных на 1",
                  "Бомба дает одному шарику максимальный урон(999)"]

    fon = pygame.transform.scale(pygame.image.load('data//background.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


def end_screen(score):
    intro_text = ["Balls&Blocks", "",
                  "Конец игры", "Ваш счет",
                  str(score)]

    fon = pygame.transform.scale(pygame.image.load('data//background.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


start_screen()
# Группа всех спрайтов
all_sprites = pygame.sprite.Group()
# Нижняя часть экрана
horizontal_borders_1 = pygame.sprite.Group()
# Верхняя часть экрана
horizontal_borders_2 = pygame.sprite.Group()
# Боковые стороны
vertical_borders = pygame.sprite.Group()
# Блоки
blocks = pygame.sprite.Group()
spec_balls = pygame.sprite.Group()
# Шарики
balls = pygame.sprite.Group()
# Позиция линии наведения
POS = [0, 0]
running = True


# Игровые блоки
class NewBlock(Block):
    def __init__(self, x1, y1, w, h, main_group, blocks_group, score):
        super().__init__(x1, y1, w, h, main_group, blocks_group, score)

    def update(self):
        self.rect = self.rect.move(0, 50)
        if pygame.sprite.spritecollideany(self, horizontal_borders_1):
            global running
            running = False


# Красные шарики
class PlayBall(Ball):
    def __init__(self, radius, x, y, sx, sy, main_group, balls_group):
        super().__init__(radius, x, y, sx, sy, main_group, balls_group)

    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders_1):
            self.kill()
            global balls_falls
            balls_falls += 1
            return
        elif pygame.sprite.spritecollideany(self, horizontal_borders_2):
            self.vy = -self.vy
        elif pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        elif pygame.sprite.spritecollideany(self, blocks):
            bl = pygame.sprite.spritecollide(self, blocks, False)
            for i in range(len(bl)):
                if bl[i].rect.x + 5 > self.rect.x or bl[i].rect.x + bl[i].rect.w - 5 < self.rect.x:
                    self.vx = -self.vx
                else:
                    self.vy = -self.vy
                pygame.sprite.spritecollide(self, blocks, False)[0].get_min(self.dam)
                break
        elif pygame.sprite.spritecollideany(self, spec_balls):
            if pygame.sprite.spritecollide(self, spec_balls, False)[0].ball_id == 1:
                self.dam = 999
            elif pygame.sprite.spritecollide(self, spec_balls, False)[0].ball_id == 2:
                global balls_cou
                balls_cou += 1
            pygame.sprite.spritecollide(self, spec_balls, False)[0].kill()
        self.rect = self.rect.move(self.vx, self.vy)


# Количество упавших шариков
balls_falls = 0
# Стороны поля
Border(0, 0, width, 0, all_sprites, vertical_borders, horizontal_borders_1, horizontal_borders_2)
Border(0, height + 20, width, height, all_sprites, vertical_borders, horizontal_borders_1, horizontal_borders_2)
Border(0, 0, 0, height, vertical_borders, all_sprites, horizontal_borders_1, horizontal_borders_2)
Border(width, 0, width, height, vertical_borders, all_sprites, horizontal_borders_1, horizontal_borders_2)
# Фон
game_fon = pygame.transform.scale(pygame.image.load('data//game_background.jpg'), (width, height))
# Флаг начала запуска шариков
flag = True
# Флаг для
flag1 = False
#
flag_col = True
# Очки игрока
score = 1
# Таймер для запуска шариков
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 150)
# Таймер для движения шариков
MYEVENTTYPE1 = 31
pygame.time.set_timer(MYEVENTTYPE1, 10)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()

        if flag_col:
            col = 20
            while col + 50 <= 500:
                if random.randint(0, 1):
                    NewBlock(col, 500, 50, 50, all_sprites, blocks, score)
                elif random.randint(1, 50) <= 3:
                    SpecBall(25, col, 20, random.randint(1, 2), all_sprites, spec_balls)
                col += 50
            blocks.update()
            spec_balls.update()
            flag_col = False
        if event.type == pygame.MOUSEMOTION and flag:
            POS[0] = event.pos[0]
            POS[1] = event.pos[1]
            if POS[0] < height // 2:
                POS[1] = width - ((height // 2 * (width - POS[1])) // (height // 2 - POS[0]))
                POS[0] = 0
            elif POS[0] == height // 2:
                POS[1] = 0
            else:
                POS[1] = width - ((height // 2 * (width - POS[1])) // (POS[0] - height // 2))
                POS[0] = height
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag = False
            flag1 = True
            balls_cou_1 = 0
        if event.type == MYEVENTTYPE and flag1 and balls_cou_1 < balls_cou:
            balls_cou_1 += 1
            sx = 0
            if POS[0] == 0:
                sx = -width / 200
                sy = -((height - POS[1]) / 100)
            elif POS[0] == height:
                sx = POS[0] / 200
                sy = -((height - POS[1]) / 100)
            else:
                sx = (POS[0] - 300) / 100
                sy = -((height - POS[1]) / 200)
            PlayBall(10, width // 2, height, sx, sy, all_sprites, balls)
            sound.play()
        if event.type == MYEVENTTYPE1 and flag1:
            balls.update()
        if balls_falls == balls_cou:
            print(balls_falls)
            balls_falls = 0
            flag = True
            flag_col = True
            score += 1

    screen.blit(game_fon, (0, 0))
    if flag:
        pygame.draw.line(screen, (0, 255, 0), (width // 2, height), (POS[0], POS[1]), 1)
    font = pygame.font.Font(None, 25)
    text = font.render(str(score), 1, (255, 255, 0))
    screen.blit(text, (500, 500))
    all_sprites.draw(screen)
    pygame.display.flip()

end_screen(score)

# завершение работы:
pygame.quit()
