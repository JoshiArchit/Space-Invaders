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
    """
    Class to define the player object.
    Player dimensions --> top-left (x, y) = (150, 200), width & height = 20px
    """
    def __init__(self):
        """
        Initialize the player object with the player image, dimensions, position and speed.
        """
        # Player sprite
        self.player_img = pygame.image.load('assets/player.png')
        self.player_img.set_colorkey((0, 0, 0))
        self.player = self.player_img.get_rect()
        # Scale the image to the required dimensions
        self.player_img = pygame.transform.scale(
            self.player_img,
            (self.player.width, self.player.height))

        # Player dimensions
        self.player.width = 30
        self.player.height = 20
        self.player.x = 150
        self.player.y = 200

        # Player motion
        self.player_speed = 5
        self.move_left = False
        self.move_right = False


class Enemy:
    """
    Class to define the enemy object.
    Enemy dimensions (start) --> top-left (x, y) = (20, 50), width & height = 20px
    """
    def __init__(self, waves, num_per_wave):
        """
        Initialize the enemy object with the enemy image, dimensions, position, speed and
        update delay. The parameters increment with each level.

        :param waves: Number of waves in the current level
        :param num_per_wave: Number of enemies in each wave
        """
        # Enemy sprites
        self.assets = {
            '1': pygame.image.load('assets/green.png'),
            '2': pygame.image.load('assets/red.png'),
            '3': pygame.image.load('assets/yellow.png')
        }
        self.width, self.height = 10, 10
        self.enemy_img = self.assets['1']
        self.enemy_img.set_colorkey((0, 0, 0))

        # Enemy dimensions
        self.waves = waves
        self.num_enemies_per_wave = num_per_wave
        self.enemies = render_enemy(self.waves, self.num_enemies_per_wave)
        self.enemy_speed = 2  # Will move continuously
        # Todo: Reduce frames as difficulty increases
        self.enemy_update_delay = 10  # Number of frames between each movement
        self.enemy_update_counter = 0
        self.current_type = 1

    def render(self, enemy_obj):
        """
        Function to render the enemy objects on the screen.

        :param enemy_obj: list of enemy Rect objects
        :return: scaled enemy image
        """
        enemy_types = len(self.assets)
        # Change enemy type after every wave and reset the counter if it exceeds the number of types
        if self.current_type > enemy_types:
            self.current_type = 1

        if self.current_type <= enemy_types:
            enemy_obj.enemy_img = enemy_obj.assets[str(self.current_type)]
            self.current_type += 1

        # Scale the image to the required dimensions
        return pygame.transform.scale(
                    enemy_obj.enemy_img,
                    (self.width, self.height)
        )


class Bullet:
    """
    Class to define the bullet object.
    """
    def __init__(self, player):
        self.bullet = pygame.Rect(player.centerx - 2, player.centery, 5, player.height // 2)
        self.bullet_speed = 10
        self.bullet_fired = False
