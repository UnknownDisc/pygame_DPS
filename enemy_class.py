import math

import pygame

from settings import *


class Enemy(pygame.sprite.Sprite):

    def __init__(self, player_pos, y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Assets/enemy.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] // 5, self.image.get_size()[1] // 5))

        self.x = WIDTH + self.image.get_size()[0]
        self.y = y

        self.rect = pygame.Rect(self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2, self.image.get_size()[0], self.image.get_size()[1])

        self.player_pos = player_pos

        self.angle = math.atan2(player_pos[1] - y, player_pos[0] - self.x)
    
    def main(self, player_pos, screen):

        self.rect = pygame.Rect(self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2, self.image.get_size()[0], self.image.get_size()[1])

        self.angle = (90 - math.atan2(player_pos[1] - self.y, player_pos[0] - self.x))

        self.x += math.sin(self.angle) * 1
        self.y += math.cos(self.angle) * 1

        screen.blit(self.image, (self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2))
