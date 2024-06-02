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
    def __init__(self, waves=3):
        # Enemy rectangle (top-left = 20, bottom-left=50, width & height = 20)
        self.assets = {
            '1': pygame.image.load('assets/green.png'),
            '2': pygame.image.load('assets/red.png'),
            '3': pygame.image.load('assets/yellow.png')
        }
        self.width, self.height = 10, 10
        self.enemy_img = self.assets['1']
        self.enemy_img.set_colorkey((0, 0, 0))
        self.waves = waves
        self.enemies = render_enemy(self.waves)
        self.enemy_speed = 2  # Will move continuously
        # Todo: Reduce frames as difficulty increases
        self.enemy_update_delay = 10  # Number of frames between each movement
        self.enemy_update_counter = 0
        self.current_type = 1

    def render(self, enemy_obj):
        enemy_types = len(self.assets)
        if self.current_type > enemy_types:
            self.current_type = 1

        if self.current_type <= enemy_types:
            enemy_obj.enemy_img = enemy_obj.assets[str(self.current_type)]
            self.current_type += 1

        return pygame.transform.scale(
                    enemy_obj.enemy_img,
                    (self.width, self.height)
        )


class Bullet:
    def __init__(self, player):
        self.bullet = pygame.Rect(player.centerx - 2, player.centery, 5, player.height // 2)
        self.bullet_speed = 10
        self.bullet_fired = False
