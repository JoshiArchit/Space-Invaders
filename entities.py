"""
Filename : entities.py
Author : Archit
Date Created : 6/2/2024
Description : 
Language : python3
"""
import pygame

from updates import render_enemy


class Player:
    # Player rectangle (top-left = 150, bottom-left = 200, width & height = 20)
    def __init__(self):
        self.player_img = pygame.image.load('assets/player.png')
        self.player_img.set_colorkey((0, 0, 0))
        self.player = self.player_img.get_rect()
        self.player.width = 30
        self.player.height = 20
        self.player.x = 150
        self.player.y = 200
        self.player_speed = 5
        self.move_left = False
        self.move_right = False
        # Scale image to player dimensions
        self.player_img = pygame.transform.scale(self.player_img,
                                                 (self.player.width, self.player.height))


class Enemy:
    def __init__(self):
        # Enemy rectangle (top-left = 20, bottom-left=50, width & height = 20)
        self.enemy_img = pygame.image.load('assets/green.png')
        self.enemy_img.set_colorkey((0, 0, 0))
        self.enemy_img = pygame.transform.scale(self.enemy_img, (10, 10))
        self.enemies = render_enemy()
        self.enemy_speed = 2  # Will move continuously
        # Todo: Reduce frames as difficulty increases
        self.enemy_update_delay = 25  # Number of frames between each movement
        self.enemy_update_counter = 0


class Bullet:
    def __init__(self, player):
        self.bullet = pygame.Rect(player.centerx - 2, player.centery, 5, player.height // 2)
        self.bullet_speed = 5
        self.bullet_fired = False
