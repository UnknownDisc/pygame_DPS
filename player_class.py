import math

import pygame

from settings import *


class Player:

    def __init__(self):

        self.image = pygame.image.load("Assets/player.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] // 3, self.image.get_size()[1] // 3))

        self.x_vel = 0
        self.y_vel = 0

        self.x = WIDTH // 4
        self.y = HEIGHT // 2

        self.rect = pygame.Rect(self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2, self.image.get_size()[0], self.image.get_size()[1])

        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

        self.angle = 0

        self.speed = 5

        self.bullets = dict()
        self.bullet_num = 1

        self.state = "alive"

        self.delete = []
    
    def rotate(self, surface, angle):

        self.rect = pygame.Rect(self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2, self.image.get_size()[0], self.image.get_size()[1])

        self.rotated_image = pygame.transform.rotozoom(surface, angle, 1)
        self.rotated_rect = self.rotated_image.get_rect(center = (300, 300))

        return (self.rotated_image, self.rotated_rect)

    def move(self):

        self.rect = pygame.Rect(self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2, self.image.get_size()[0], self.image.get_size()[1])

        self.x_vel = 0
        self.y_vel = 0

        if self.left and not self.right:
            self.x_vel = self.speed * -1
        
        if self.right and not self.left:
            self.x_vel = self.speed
        
        if self.up and not self.down:
            self.y_vel = self.speed * -1
        
        if self.down and not self.up:
            self.y_vel = self.speed
        
        self.x += self.x_vel
        self.y += self.y_vel

        if self.x > WIDTH - 25:
            self.x = WIDTH - 25
        
        if self.x < 25:
            self.x = 25
        
        if self.y > HEIGHT - 25:
            self.y = HEIGHT - 25
        
        if self.y < 25:
            self.y = 25

    def shoot(self):

        self.rect = pygame.Rect(self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2, self.image.get_size()[0], self.image.get_size()[1])

        bullet_name = f"bullet{self.bullet_num}"

        self.bullets[bullet_name] = {}
        self.bullets[bullet_name]["angle"] = math.atan2(pygame.mouse.get_pos()[0] - self.x, pygame.mouse.get_pos()[1] - self.y)
        self.bullets[bullet_name]["show/hide"] = 0
        self.bullets[bullet_name]["hit enemy"] = False

        self.bullets[bullet_name]["image"] = pygame.image.load("Assets/bullet.png")
        self.bullets[bullet_name]["image"] = pygame.transform.scale(self.bullets[bullet_name]["image"], (self.bullets[bullet_name]["image"].get_size()[0] // 20, self.bullets[bullet_name]["image"].get_size()[1] // 20))
        self.bullets[bullet_name]["image"] = pygame.transform.rotozoom(self.bullets[bullet_name]["image"], self.angle, 1)

        self.bullets[bullet_name]["pos"] = {}
        self.bullets[bullet_name]["pos"]["x"] = self.x
        self.bullets[bullet_name]["pos"]["y"] = self.y

        self.bullets[bullet_name]["rect"] = pygame.Rect(self.bullets[bullet_name]["pos"]["x"] - self.bullets[bullet_name]["image"].get_size()[0] // 2, self.bullets[bullet_name]["pos"]["x"] - self.bullets[bullet_name]["image"].get_size()[1] // 2, self.bullets[bullet_name]["image"].get_size()[0], self.bullets[bullet_name]["image"].get_size()[1])

        self.bullet_num += 1

    def point(self):

        self.rect = pygame.Rect(self.x - self.image.get_size()[0] // 2, self.y - self.image.get_size()[1] // 2, self.image.get_size()[0], self.image.get_size()[1])

        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]

        self.x_distance = self.mouse_x - self.x

        self.angle = (-90 - math.atan2((self.mouse_y - self.y), self.x_distance) * 180/math.pi) + 180
        
        self.rotated_image, self.image_rotated_rect = self.rotate(self.image, self.angle)
