import pygame
import os
import math
import random

pygame.init()
# размеры окна:
size = width, height = 500, 500
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
Ball_MOVE = [3, 0]
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        # self.vx = random.randint(-5, 5)
        # self.vy = random.randrange(-5, 5)
        self.vx = Ball_MOVE[0]
        self.vy = Ball_MOVE[1]

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

Ball(10, 250, 400)
running = True
POS = [0, 0]
flag = True
flag1 = True
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 150)
MYEVENTTYPE1 = 31
pygame.time.set_timer(MYEVENTTYPE1, 10)
v = 100  # пикселей в секунду
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION and flag:
            POS[0] = event.pos[0]
            POS[1] = event.pos[1]
            if POS[0] <= 250 and POS[1] > 70:
                POS[0] = 0
            elif POS[0] >= 250 and POS[1] > 70:
                POS[0] = 500
            else:
                POS[1] = 0

        if event.type == pygame.MOUSEBUTTONDOWN and flag1:
            flag = False
            flag1 = False
            Ball_MOVE[1] = -((500 - POS[1]) / 100)
            if POS[0] <= 250:
                Ball_MOVE[0] = -3

        if event.type == MYEVENTTYPE1:
            all_sprites.update()
        if event.type == MYEVENTTYPE and not flag1:
            Ball(10, 250, 400)
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 255, 0), (250, 400), (POS[0], POS[1]), 1)
    all_sprites.draw(screen)
    pygame.display.flip()
# завершение работы:
pygame.quit()