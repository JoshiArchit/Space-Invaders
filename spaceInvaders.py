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

    def render_enemy(self):
        """
        Helper to create a list of enemy objects (Rectangles) on screen.
        The list will have gaps between each enemy.
        If collision is detected, remove the enemy from the list.
        :return:
        """
        enemies = []
        enemy = pygame.Rect(15, 50, 10, 10)
        enemies.append(enemy)
        next_enemy_x = enemy.right + 10
        while next_enemy_x < SURFACE_WIDTH:
            enemy = pygame.Rect(next_enemy_x, 50, 10, 10)
            # Return if last enemy goes out of bounds
            if enemy.right >= SURFACE_WIDTH:
                return enemies
            enemies.append(enemy)
            next_enemy_x = enemy.right + 10
        return enemies

    def movement(self):
        """
        Helper function for jagged enemy movement.
        :return: None
        """
        self.enemy_update_counter += 1
        if self.enemy_update_counter >= self.enemy_update_delay:
            self.enemy_update_counter = 0
            for enemy in self.enemies:
                enemy.x += self.enemy_speed
                if enemy.left < 0:
                    enemy.x = 0
                    self.enemy_speed = abs(self.enemy_speed)
                elif enemy.right >= SURFACE_WIDTH:
                    enemy.right = SURFACE_WIDTH
                    self.enemy_speed = -abs(self.enemy_speed)

    def firebullet(self):
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
            for enemy in self.enemies:
                # Check collision only if bullet was fired
                if enemy.colliderect(self.bullet):
                    self.enemies.remove(enemy)
                    self.bullet_fired = False
                    # Reset bullet position
                    self.bullet.y = self.player.centery



    def run(self):
        # game loop to display window
        while True:
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
            # Todo: Needs to have a separate render enemy function that renders list of enemies
            for enemy in self.enemies:
                pygame.draw.rect(self.display, (255, 0, 0), enemy)
            # Update every enemy's position
            self.movement()
            self.firebullet()
            self.collision()

            # Blit display to screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            # Update display and cap refresh rate
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
