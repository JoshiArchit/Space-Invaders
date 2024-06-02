"""
Filename : spaceInvaders.py
Author : Archit
Date Created : 6/2/2024
Description : Space Invaders
Language : python3
"""

import pygame
import sys

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
SURFACE_WIDTH = 320
SURFACE_HEIGHT = 240


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
        self.enemies = self.render_enemy()
        self.enemy_speed = 2  # Will move continuously
        self.alive_enemies = len(self.enemies) * [True]
        # Todo: Reduce frames as difficulty increases
        self.enemy_update_delay = 25  # Number of frames between each movement
        self.enemy_update_counter = 0

        # Player rectangle (top-left = 150, bottom-left = 200, width & height = 20)
        self.player = pygame.Rect(150, 200, 25, 15)
        self.player_speed = 5

        # Bullet initialization
        self.bullet = pygame.Rect(self.player.centerx - 2, self.player.centery, 5,
                                  self.player.height // 2)
        self.bullet_speed = 5
        self.bullet_fired = False

        # Score
        self.score = 0
        self.lives = 3

    def render_enemy(self):
        """
        Helper to create a list of enemy objects (Rectangles) on screen.
        The list will have gaps between each enemy.
        If collision is detected, remove the enemy from the list.
        :return:
        """
        # enemies dictionary to store enemy objects and alive status
        enemies = dict()
        enemy_y = 50
        enemy_x = 15
        counter = 0
        while True:
            enemies[counter] = (pygame.Rect(enemy_x, enemy_y, 10, 10), True)
            enemy_x += enemies[counter][0].width + 10
            if enemy_x >= SURFACE_WIDTH or enemies[counter][0].right > SURFACE_WIDTH:
                enemies.pop(counter)
                return enemies
            counter += 1

    def movement(self):
        """
        Helper function for jagged enemy movement.
        :return: None
        """
        self.enemy_update_counter += 1
        if self.enemy_update_counter >= self.enemy_update_delay:
            self.enemy_update_counter = 0

            # Check the leftmost and rightmost enemies
            leftmost_enemy = self.enemies[min(self.enemies.keys())][0]
            rightmost_enemy = self.enemies[max(self.enemies.keys())][0]

            # Doesnt matter if they are alive or dead. They will move together. Alive or dead is
            # handled in collision
            for enemy, info in self.enemies.items():
                enemy_rect = info[0]  # Rect object is the first element in the tuple
                enemy_rect.x += self.enemy_speed

            # Check if the leftmost enemy has hit the left wall
            if leftmost_enemy.left <= 0:
                self.enemy_speed = abs(self.enemy_speed)
                for enemy, info in self.enemies.items():
                    enemy_rect = info[0]
                    enemy_rect.y += 10
            # Check if the rightmost enemy has hit the right wall
            elif rightmost_enemy.right >= SURFACE_WIDTH:
                self.enemy_speed = -abs(self.enemy_speed)
                for enemy, info in self.enemies.items():
                    enemy_rect = info[0]
                    enemy_rect.y += 10

    def fire_bullet(self):
        """
        Helper function to fire a bullet from the player object.
        :return: None
        """
        if self.bullet_fired:
            # Move bullet up (subtract speed)
            self.bullet.y -= self.bullet_speed
            # Out of bounds condition
            if self.bullet.top <= 0:
                self.bullet_fired = False
                # Reset y to player center
                self.bullet.y = self.player.centery

    def collision(self):
        """
        Helper function to detect collision between bullet and enemies. Successful collision
        removes enemy from list.

        :return: None
        """
        if self.bullet_fired:
            for enemy, enemy_info in self.enemies.items():
                rect_enemy, isalive = enemy_info
                if rect_enemy.colliderect(self.bullet) and isalive:
                    self.bullet_fired = False
                    self.bullet.y = self.player.centery
                    # Remove enemy from list
                    self.enemies[enemy] = (rect_enemy, False)

    def scorebar(self):
        pass

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.bullet_fired is False:
                        self.bullet_fired = True
                # Todo: Movement code

            # Fill display with black color
            self.display.fill((0, 0, 0))

            # Render objects
            pygame.draw.rect(self.display, (255, 255, 255), self.player)
            pygame.draw.rect(self.display, (0, 255, 0), self.bullet)
            for enemy, isalive in self.enemies.values():
                color = (255, 0, 0) if isalive else (0, 0, 0)
                if isalive:
                    pygame.draw.rect(self.display, color, enemy)

            # Object update functions
            self.movement()
            self.fire_bullet()
            self.collision()
            self.game_over()

            # Blit display to screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            # Update display and cap refresh rate
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
