import pygame
import os
import math
import random

pygame.init()
# размеры окна:
size = width, height = 600, 600
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
Ball_MOVE = [3, 0]
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
blocks = pygame.sprite.Group()


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


class Block(pygame.sprite.Sprite):
    def __init__(self, x1, y1, w, h):
        super().__init__(all_sprites)
        self.add(blocks)
        self.image = pygame.Surface([w, h])
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, w, h))
        self.rect = pygame.Rect(x1, y1, w, h)

    def update(self):
        pygame.draw.rect(self.image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (0, 0, self.rect.width, self.rect.height))


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.x = x
        self.y = y
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        # self.vx = random.randint(-5, 5)
        # self.vy = random.randrange(-5, 5)
        self.vx = Ball_MOVE[0]
        self.vy = Ball_MOVE[1]

    def update(self):
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        elif pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        elif pygame.sprite.spritecollideany(self, blocks):
            for i in pygame.sprite.spritecollide(self, blocks, False):
                if i.rect.x + 5 > self.rect.x or i.rect.x + i.rect.w - 5< self.rect.x:
                    self.vx = -self.vx
                    print(i.rect.x, self.rect.x, i.rect.x + i.rect.w )

                else:
                    self.vy = -self.vy
                    print(i.rect.x, self.rect.x, i.rect.x + i.rect.w )
        self.rect = self.rect.move(self.vx, self.vy)

Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)
Block(35, 80, 50, 50)
Block(85, 80, 50, 50)
Block(135, 80, 50, 50)
Ball(10, 300, 500)
running = True
POS = [0, 0]
flag = True
COU = 1
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
            if POS[0] < 300:
                POS[1] = 600 - ((300 * (600 - POS[1]))//(300 - POS[0]))
                POS[0] = 0
            elif POS[0] == 300:
                POS[1] = 0
            else:
                POS[1] = 600 - ((300 * (600 - POS[1])) // (POS[0] - 300))
                POS[0] = 600

        if event.type == pygame.MOUSEBUTTONDOWN and flag1:
            flag = False
            flag1 = False
            Ball_MOVE[1] = -((600 - POS[1]) / 100)
            print(POS)
            if POS[0] <= 300:
                Ball_MOVE[0] = -3

        if event.type == MYEVENTTYPE1:
            all_sprites.update()
        if event.type == MYEVENTTYPE and not flag1 and COU <= 10:
            COU += 1
            Ball(10, 300, 500)
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 255, 0), (300, 500), (POS[0], POS[1]), 1)
    all_sprites.draw(screen)
    pygame.display.flip()
# завершение работы:
pygame.quit()