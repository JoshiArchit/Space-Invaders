"""
Filename : spaceInvaders.py
Author : Archit
Date Created : 6/2/2024
Description : Space Invaders
Language : python3
"""

import pygame
import sys

import utils
from updates import (movement, fire_bullet, collision, render_enemy, player_movement,
                     DISPLAY_WIDTH, DISPLAY_HEIGHT, SURFACE_WIDTH, SURFACE_HEIGHT)
from entities import Player, Bullet, Enemy


class Game:
    # Game class. Handle window dimensions, object dimensions.

    def __init__(self, next_level=False, current_waves=3):
        pygame.init()
        pygame.display.set_caption("PyGame Space Invaders")
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.display = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        self.clock = pygame.time.Clock()

        # Player rectangle (top-left = 150, bottom-left = 200, width & height = 20)
        self.player_obj = Player()
        # Bullet initialization
        self.bullet_obj = Bullet(self.player_obj.player)
        # Enemy rectangle (top-left = 20, bottom-left=50, width & height = 20)
        self.enemy_obj = Enemy(current_waves)

        # Score and lives
        self.score = 0
        self.lives = 3

    def scoreboard(self):
        """
        Function to display the score and lives on the screen
        :return: None
        """
        # Create a dedicated surface for the scoreboard
        score_display = pygame.Surface((DISPLAY_WIDTH, 40))
        # Light grey background
        score_display.fill((200, 200, 200))
        # Font object
        font = pygame.font.Font(None, 36)
        # Render text
        score_text = font.render(f"Score: {game.score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {game.lives}", True, (0, 0, 0))
        # Blit text to the surface
        score_display.blit(score_text, (10, 10))
        score_display.blit(lives_text, (DISPLAY_WIDTH - 150, 10))
        # Blit the scoreboard to the screen
        self.screen.blit(score_display, (0, 0))

    def check_events(self):
        for event in pygame.event.get():
            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Bullet fire event
            # Player movement events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.bullet_obj.bullet_fired:
                    self.bullet_obj.bullet_fired = True
                if event.key == pygame.K_LEFT:
                    self.player_obj.move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.player_obj.move_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player_obj.move_left = False
                elif event.key == pygame.K_RIGHT:
                    self.player_obj.move_right = False

    def render_objects(self):
        # Blit player and bullet
        self.display.blit(
            self.player_obj.player_img,
            (self.player_obj.player.x, self.player_obj.player.y)
        )

        pygame.draw.rect(
            self.display,
            (0, 255, 0),
            self.bullet_obj.bullet
        )

        # Get starting indexes for each wave
        enemy_per_wave = len(self.enemy_obj.enemies) // self.enemy_obj.waves
        row_start = [i * enemy_per_wave for i in range(self.enemy_obj.waves)]

        for enemy in self.enemy_obj.enemies:
            # If end of current wave is reached, print DONE before moving to next row
            if self.enemy_obj.enemies.index(enemy) in row_start:
                # Cycle through enemy types and render different sprite
                self.enemy_obj.enemy_img = self.enemy_obj.render(self.enemy_obj)
            self.display.blit(self.enemy_obj.enemy_img, enemy[0])

    def gameover(self):
        self.lives -= 1
        if self.lives == 0:
            pass
        else:
            display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, (0, 0, 0))
            display.blit(text, (DISPLAY_WIDTH // 2 - 50, DISPLAY_HEIGHT // 2))
            self.screen.blit(display, (0, 0))
            pygame.display.update()

    def run(self):
        # game loop to display window
        while True:
            # Check if all enemies are destroyed
            if not self.enemy_obj.enemies:
                # Reset enemies
                print("All enemies destroyed")
                return -1

            self.display.fill((0, 0, 0))

            # Check for events
            self.check_events()
            # Render objects
            self.render_objects()

            # Object update functions : Check updates.py
            player_movement(self.player_obj, self.bullet_obj)
            movement(self.enemy_obj)
            fire_bullet(self.bullet_obj, self.player_obj)
            score_increment, player_collision = collision(self.bullet_obj, self.enemy_obj,
                                                          self.player_obj)
            self.score += score_increment
            if player_collision:
                self.gameover()
                pygame.time.wait(2000)
                return self.lives

            # Blit display to screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            # Local functions
            self.scoreboard()
            # Update display and cap refresh rate
            pygame.display.update()
            # Reset enemy type after every wave to keep rendering consistent at each refresh
            self.enemy_obj.current_type = 1
            self.clock.tick(60)


def playgame(new_game):
    # Todo : what after you win?
    lives = new_game.run()
    current_waves = new_game.enemy_obj.waves
    while lives > 0 or lives == -1:
        if lives == -1:
            print("winner")
            # Player has won
            play_next = utils.winner(new_game)
            if play_next:
                new_game = Game(next_level=True, current_waves=current_waves + 1)
                lives = new_game.run()
        else:
            # Give choice to play again
            choice = utils.try_again(new_game)
            if choice:
                game = Game()
                lives = game.run()
            else:
                utils.goodbye()
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    game = Game()
    playgame(game)
