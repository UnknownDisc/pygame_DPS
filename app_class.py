import math
import random

import pygame

from settings import *
from player_class import Player
from enemy_class import Enemy

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
            
            elif self.state == "TUTORIAL":
                self.tutorial_draw()
                self.tutorial_events()
                self.update()
            
            elif self.state == "PLAYING":

                self.playing_draw()
                self.playing_update()
                self.playing_events()
                self.update()

            self.clock.tick(FPS)
    
    def tutorial_draw(self):

        self.screen.fill(BLACK)

        self.write_text("You, the player will always be pointing towards the mouse pointer.", self.screen, [WIDTH // 2, 25], 18, (255, 189, 99), "arial black", True)
        self.write_text("Press SPACE BAR to shoot the bullet towards the enemy.", self.screen, [WIDTH // 2, HEIGHT // 250], 18, (255, 189, 99), "arial black", True)
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