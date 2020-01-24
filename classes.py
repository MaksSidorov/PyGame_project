import pygame
import random


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, main_group, ver_group, hor_1_group, hor_2_group):
        super().__init__(main_group)
        if x1 == x2:
            self.add(ver_group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            if y1 >= 10:
                self.add(hor_1_group)
            else:
                self.add(hor_2_group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Block(pygame.sprite.Sprite):
    def __init__(self, x1, y1, w, h, main_group, blocks_group, score):
        super().__init__(main_group)
        self.add(blocks_group)
        # Количество раз сколько надо ударить по блоку
        self.sc = score
        self.rect = pygame.Rect(x1, y1, w, h)
        self.make_image(self.sc)

    def update(self):
        self.rect = self.rect.move(0, 50)

    def get_min(self, c):
        self.sc -= c
        self.make_image(self.sc)
        # Если количество ударов <= 0, удаляем блок
        if self.sc <= 0:
            self.kill()

    def make_image(self, sc):
        color = [0, 0, 0]
        if sc >= 250:
            color[0] = 255
        elif sc >= 100:
            color = [255, 255, 0]
        elif sc >= 50:
            color = [0, 255, 0]
        elif sc >= 10:
            color = [0, 255, 255]
        else:
            color = [0, 0, 255]
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        pygame.draw.rect(self.image, color, (0, 0, self.rect.width, self.rect.height))
        font = pygame.font.Font(None, 25)
        text = font.render(str(self.sc), 1, (0, 0, 0))
        text_x = 25 - text.get_width() // 2
        text_y = 25 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, sx, sy, main_group, balls_group):
        super().__init__(main_group)
        self.add(balls_group)
        self.radius = radius
        self.x = x
        self.y = y
        self.dam = 1
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = sx
        self.vy = sy


class SpecBall(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, gr_id, main_group, spec_balls_group):
        super().__init__(main_group)
        self.add(spec_balls_group)
        self.radius = radius
        self.x = x
        self.y = y
        self.ball_id = gr_id
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        if gr_id == 1:
            img = pygame.image.load('data//bomb1.png').convert_alpha()
            img = pygame.transform.scale(img, (50, 50))
            self.image.blit(img, (0, 0))
        elif gr_id == 2:
            pygame.draw.circle(self.image, pygame.Color("green"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)

    def update(self):
        self.rect = self.rect.move(0, 50)
