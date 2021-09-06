import math
import random

import pygame

from settings import *

pygame.init()

class App:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(NAME)

        self.score = 0

        self.player = Player()

        self.enemies = []

        self.running = True
        self.state = "INTRO"

        self.enemy_timer = 0
        self.enemy_num = 0

        self.clock = pygame.time.Clock()

    def run(self):

        while self.running:
            
            if self.state == "INTRO":

                self.intro_draw()
                self.intro_events()
                self.update()
            
            if self.state == "TUTORIAL":
                self.tutorial_draw()
                self.tutorial_events()
                self.update()
            
            if self.state == "PLAYING":

                self.playing_draw()
                self.playing_update()
                self.playing_events()
                self.update()
            
            if self.state == "DEFEAT":
                self.defeat_draw()
                self.defeat_events()
                self.update()

            self.clock.tick(FPS)
    
    def defeat_draw(self):

        self.screen.fill(BLACK)

        self.write_text("YOU LOST!", self.screen, [WIDTH // 2, 25], 20, (255, 189, 99), "arial black", True)
        self.write_text("Press SPACE BAR to start again!", self.screen, [WIDTH // 2, HEIGHT - 25], 20, (255, 189, 99), "arial black", True)
    
    def defeat_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    self.state = "START"

    def tutorial_draw(self):

        self.screen.fill(BLACK)

        self.write_text("You, the player will always be pointing towards the mouse pointer.", self.screen, [WIDTH // 2, HEIGHT // 3], 18, (255, 189, 99), "arial black", True)
        self.write_text("Press SPACE BAR to shoot the bullet towards the enemy.", self.screen, [WIDTH // 2, HEIGHT // 2], 18, (255, 189, 99), "arial black", True)
        self.write_text("Use WASD to move around.", self.screen, [WIDTH // 2, HEIGHT - 150], 18, (255, 189, 99), "arial black", True)
        self.write_text("Press 'S' to START!", self.screen, [WIDTH // 2, HEIGHT - 75], 18, (255, 189, 99), "arial black", True)
    
    def tutorial_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:

                    self.state = "PLAYING"

    def create_enemy(self):

        self.enemies.append(Enemy((self.player.x, self.player.y), random.randrange(HEIGHT)))
        self.enemy_num += 1

    def update(self):
        pygame.display.update()

    def playing_update(self):

        self.player.move()

        if self.enemy_timer % 200 == 0:
            self.create_enemy()
        
        self.enemy_timer += 1

        if self.enemy_num > 0:

                for i in range(len(self.enemies)):
                    
                    try:    
                        self.enemies[i].main((self.player.x, self.player.y), self.screen)
                    
                    except IndexError:
                        pass

        for i in range(len(self.player.bullets)):

            self.player.bullets[list(self.player.bullets.keys())[i]]["show/hide"] += 1

            if self.player.bullets[list(self.player.bullets.keys())[i]]["show/hide"] >= 5:

                self.screen.blit(self.player.bullets[list(self.player.bullets.keys())[i]]["image"], (self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["x"] - self.player.bullets[list(self.player.bullets.keys())[i]]["image"].get_size()[0] // 2, self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["y"] - self.player.bullets[list(self.player.bullets.keys())[i]]["image"].get_size()[1] // 2))

            self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["x"] += (math.sin(self.player.bullets[list(self.player.bullets.keys())[i]]["angle"]) * 15)
            self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["y"] += (math.cos(self.player.bullets[list(self.player.bullets.keys())[i]]["angle"]) * 15)

            self.player.bullets[list(self.player.bullets.keys())[i]]["rect"] = pygame.Rect(self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["x"] - self.player.bullets[list(self.player.bullets.keys())[i]]["image"].get_size()[0] // 2, self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["y"] - self.player.bullets[list(self.player.bullets.keys())[i]]["image"].get_size()[1] // 2, self.player.bullets[list(self.player.bullets.keys())[i]]["image"].get_size()[0], self.player.bullets[list(self.player.bullets.keys())[i]]["image"].get_size()[1])

            if self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["x"] > WIDTH or self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["x"] < 0 or self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["y"] > HEIGHT or self.player.bullets[list(self.player.bullets.keys())[i]]["pos"]["y"] < 0 or self.player.bullets[list(self.player.bullets.keys())[i]]["hit enemy"]:
                self.player.delete.append(list(self.player.bullets.keys())[i])
        
        for i in range(len(self.enemies)):

            try:
                self.enemy_rect = self.enemies[i].rect
            
            except IndexError:
                pass

            if self.player.rect.colliderect(self.enemy_rect):

                self.state = "DEFEAT"

            for j in range(len(self.player.bullets)):

                self.bullet_name = list(self.player.bullets.keys())[j]

                self.bullet_rect = self.player.bullets[self.bullet_name]["rect"]

                if self.enemy_rect.colliderect(self.bullet_rect):

                    self.player.bullets[self.bullet_name]["hit enemy"] = True
                    self.score += 1

                    try:
                        self.enemies.pop(i)

                    except IndexError:
                        pass
        
        for i in range(len(self.player.delete)):

            try:
                self.player.bullets.pop(self.player.delete[i])
            
            except Exception:
                pass

    def intro_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.state = "TUTORIAL"

    def intro_draw(self):

        self.screen.fill(BLACK)
        self.write_text("Press SPACE BAR to start", self.screen, [WIDTH // 2, HEIGHT // 2], 40, (255, 189, 99), "arial black", True)

    def playing_events(self):

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    self.state = "SHOP"
                
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.player.left = True
                
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.right = True
                
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.up = True
                
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.player.down = True
                
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.player.left = False
                
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.player.right = False
                
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.up = False
                
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.player.down = False
    
    def playing_draw(self):

        self.screen.fill(GREY)

        self.player.point()

        self.write_text(f"Score: {self.score}", self.screen, [5, 0], 16, BLACK, "arialblack")

        self.screen.blit(self.player.rotated_image, (self.player.x - self.player.rotated_image.get_size()[0] // 2, self.player.y - self.player.rotated_image.get_size()[1] // 2))
    
    def write_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)

        text = font.render(words, False, colour)
        text_size = text.get_size()

        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2

        screen.blit(text, pos)

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
