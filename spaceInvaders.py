"""
Filename : spaceInvaders.py
Author : Archit
Date Created : 6/2/2024
Description : Space Invaders
Language : python3
"""

import pygame
import sys
from updates import (movement, fire_bullet, collision, scorebar, render_enemy, player_movement,
                     DISPLAY_WIDTH, DISPLAY_HEIGHT, SURFACE_WIDTH, SURFACE_HEIGHT)


class Game:
    # Game class. Handle window dimensions, object dimensions.
    # Todo: Create classes for Player and Enemies later

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyGame Space Invaders")
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.display = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        self.clock = pygame.time.Clock()

        # Enemy rectangle (top-left = 20, bottom-left=50, width & height = 20)
        self.enemies = render_enemy()
        self.enemy_speed = 2  # Will move continuously
        # Todo: Reduce frames as difficulty increases
        self.enemy_update_delay = 25  # Number of frames between each movement
        self.enemy_update_counter = 0

        # Player rectangle (top-left = 150, bottom-left = 200, width & height = 20)
        self.player = pygame.Rect(150, 200, 25, 15)
        self.player_speed = 5
        self.move_left = False
        self.move_right = False

        # Bullet initialization
        self.bullet = pygame.Rect(self.player.centerx - 2, self.player.centery, 5,
                                  self.player.height // 2)
        self.bullet_speed = 5
        self.bullet_fired = False

        # Score
        self.score = 0
        self.lives = 3

    def game_over(self):
        pass

    def run(self):
        # game loop to display window
        while True:
            if self.lives == 0:
                pygame.quit()
                sys.exit()

            # Check for events
            for event in pygame.event.get():
                # QUIT event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Bullet fire event
                # Player movement events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.bullet_fired:
                        self.bullet_fired = True
                    if event.key == pygame.K_LEFT:
                        self.move_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.move_right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.move_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.move_right = False

                # Todo: Movement code

            # Fill display with black color
            self.display.fill((0, 0, 0))

            # Render objects
            pygame.draw.rect(self.display, (255, 255, 255), self.player)
            pygame.draw.rect(self.display, (0, 255, 0), self.bullet)
            # # ORIGINAL enemies dictionary to store enemy objects and alive status
            # for enemy, isalive in self.enemies.values():
            #     color = (255, 0, 0) if isalive else (0, 0, 0)
            #     if isalive:
            #         pygame.draw.rect(self.display, color, enemy)
            for enemy in self.enemies:
                color = (255, 0, 0) if enemy[1] else (0, 0, 0)
                pygame.draw.rect(self.display, color, enemy[0])

            # Object update functions : Check updates.py
            player_movement(game)
            movement(game)
            fire_bullet(game)
            collision(game)
            scorebar(game)

            # Blit display to screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            # Update display and cap refresh rate
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
