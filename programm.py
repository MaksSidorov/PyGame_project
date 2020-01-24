import pygame
import os
import math
import random

pygame.init()
# размеры окна:
size = width, height = 600, 600
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
C = 10
all_sprites = pygame.sprite.Group()
horizontal_borders_1 = pygame.sprite.Group()
horizontal_borders_2 = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            if y1 >= 295:# горизонтальная стенка
                self.add(horizontal_borders_1)
            else:
                self.add(horizontal_borders_2)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Block(pygame.sprite.Sprite):
    def __init__(self, x1, y1, w, h):
        super().__init__(all_sprites)
        self.add(blocks)
        self.c = 100
        self.image = pygame.Surface([w, h])
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, w, h))
        font = pygame.font.Font(None, 25)
        text = font.render(str(self.c), 1, (0, 0, 0))
        text_x = 25 - text.get_width() // 2
        text_y = 25 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))
        self.rect = pygame.Rect(x1, y1, w, h)

    def update(self):
        self.rect = self.rect.move(0, 50)

    def get_min(self, c):
        self.c -= c
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        pygame.draw.rect(self.image, (0, 0, 255), (0, 0, self.rect.width, self.rect.height))
        font = pygame.font.Font(None, 25)
        text = font.render(str(self.c), 1, (0, 0, 0))
        text_x = 25 - text.get_width() // 2
        text_y = 25 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))
        if self.c <= 0:
            self.kill()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(balls)
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
        if pygame.sprite.spritecollideany(self, horizontal_borders_1):
            self.vy = -self.vy
            self.kill()
            global C
            C -= 1
            print(C)
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

                pygame.sprite.spritecollide(self, blocks, False)[0].get_min(1)
                break
        self.rect = self.rect.move(self.vx, self.vy)

Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)
D = 20
# Block(35, 80, 50, 50)
# Block(85, 80, 50, 50)
# Block(135, 80, 50, 50)

running = True
POS = [0, 0]
flag = True
COU = 1
flag1 = True
MYEVENTTYPE = 30
pygame.time.set_timer(MYEVENTTYPE, 150)
MYEVENTTYPE1 = 31
pygame.time.set_timer(MYEVENTTYPE1, 10)
MYEVENTTYPE2 = 29
pygame.time.set_timer(MYEVENTTYPE2, 250)
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
            balls.update()
        if event.type == MYEVENTTYPE and not flag1 and COU <= 10:
            COU += 1
            Ball(10, 300, 500)
        if event.type == pygame.KEYDOWN and C == 0:
            T = 35

            while T + 35 <= 500:
                if random.randint(0,1):
                    Block(T, 35, 50, 50)
                print(T)
                T += 50
            blocks.update()
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()
# завершение работы:
pygame.quit()