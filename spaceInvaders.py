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
        self.enemy_pos = (20, 50)
        self.enemy = pygame.Rect(20, 50, 20, 20)
        self.enemy_speed = 5  # Will move continuously

        # Player rectangle (top-left = 150, bottom-left = 200, width & height = 20)
        self.player_pos = (150, 200)
        self.player = pygame.Rect(150, 200, 20, 20)
        self.player_speed = 5

    def movement(self, dt):
        # Move enemy continuously (speed = distance/time ; distance = speed * time)
        self.enemy.x += self.enemy_speed * dt
        if self.enemy.x < 0:
            # Reached left bound, bounce to right
            self.enemy.x = 0
            self.enemy_speed = abs(self.enemy_speed)
        elif self.enemy.x >= SURFACE_WIDTH - self.enemy.width:
            # Reached right bound, bounce to left
            self.enemy.x = SURFACE_WIDTH - self.enemy.width
            self.enemy_speed = -abs(self.enemy_speed)

    def run(self):
        # game loop to display window
        last_time = pygame.time.get_ticks()
        while True:
            # Check for events
            for event in pygame.event.get():
                # QUIT event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Todo: Movement code

            # Fill display with black color
            self.display.fill((0, 0, 0))
            # Display player and enemy on display
            pygame.draw.rect(self.display, (255, 255, 255), self.player)
            pygame.draw.rect(self.display, (255, 0, 0), self.enemy)

            # Get displacement for enemy movements
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 100
            last_time = current_time
            self.movement(delta_time)

            # Blit display to screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            # Update display and cap refresh rate
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
