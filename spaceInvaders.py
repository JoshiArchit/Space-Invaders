"""
Filename : spaceInvaders.py
Author : Archit
Date Created : 6/2/2024
Description : Space Invaders
Language : python3
"""

import sys
import pygame
import utils

from entities import Player, Bullet, Enemy
from updates import (movement, fire_bullet, collision, player_movement,
                     DISPLAY_WIDTH, DISPLAY_HEIGHT, SURFACE_WIDTH, SURFACE_HEIGHT)


class Game:
    """
    Class to initialize the game window, objects and run the game loop.
    """

    def __init__(self, current_waves=3, current_enemies_per_wave=8, current_score=0,
                 current_lives=3):
        """
        Initialize the game window, objects and variables. Instantiate the player, bullet and enemy
        objects from the entities class.

        :param current_waves: Denotes the number of waves in the current level, increases with each
        level
        :param current_enemies_per_wave: Denotes the number of enemies in each wave, increases with
        each level
        """
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("PyGame Space Invaders")
        # Game screen
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        # Game display which will be scaled and blitted to the screen
        self.display = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        self.clock = pygame.time.Clock()

        # Player, bullet and enemy objects
        # Player rectangle (top-left = 150, bottom-left = 200, width & height = 20)
        self.player_obj = Player()
        # Bullet initialization
        self.bullet_obj = Bullet(self.player_obj.player)
        # Enemy rectangle (top-left = 20, bottom-left=50, width & height = 20)
        self.enemy_obj = Enemy(current_waves, current_enemies_per_wave)
        print("Current waves = ", current_waves)

        # Score and lives
        self.score = current_score
        self.lives = current_lives

    def scoreboard(self):
        """
        Function to display the score and lives on the screen.

        :return: None
        """
        # Create a dedicated surface for the scoreboard
        score_display = pygame.Surface((DISPLAY_WIDTH, 40))
        # Light grey background
        score_display.fill((200, 200, 200))
        # Font object
        font = pygame.font.Font(None, 36)
        # Render text
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {self.lives}", True, (0, 0, 0))
        # Blit text to the surface
        score_display.blit(score_text, (10, 10))
        score_display.blit(lives_text, (DISPLAY_WIDTH - 150, 10))
        # Blit the scoreboard to the screen
        self.screen.blit(score_display, (0, 0))

    def check_events(self):
        """
        Wrapper function to check for events in the game while the game loop runs.

        :return: None
        """
        for event in pygame.event.get():
            # QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Key press events - Space to fire bullet, Left and Right to move player
            if event.type == pygame.KEYDOWN:  # Key press events
                if event.key == pygame.K_SPACE and not self.bullet_obj.bullet_fired:
                    self.bullet_obj.bullet_fired = True
                if event.key == pygame.K_LEFT:
                    self.player_obj.move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.player_obj.move_right = True
            if event.type == pygame.KEYUP:  # Key release events
                if event.key == pygame.K_LEFT:
                    self.player_obj.move_left = False
                elif event.key == pygame.K_RIGHT:
                    self.player_obj.move_right = False

    def render_objects(self):
        """
        Wrapper function to render the player, bullet and enemy objects on the screen.

        :return: None
        """
        # Blit player and bullet
        self.display.blit(
            self.player_obj.player_img,
            (self.player_obj.player.x, self.player_obj.player.y)
        )

        # Blit bullet at player center
        pygame.draw.rect(
            self.display,
            (0, 255, 0),
            self.bullet_obj.bullet
        )

        for enemy in self.enemy_obj.enemies:
            # Scale the image to the required dimensions
            enemy[1] = pygame.transform.scale(enemy[1], (10, 10))

            self.display.blit(enemy[1], enemy[0])

    def gameover(self):
        """
        Game over decision function. If lives are 0, display game over message and exit game.

        :return: None
        """
        # Decrement lives
        self.lives -= 1

        # Game over message
        if self.lives == 0:
            display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, (0, 0, 0))
            display.blit(text, (DISPLAY_WIDTH // 2 - 50, DISPLAY_HEIGHT // 2))
            self.screen.blit(display, (0, 0))
            pygame.display.update()

    def run(self):
        """
        Main game loop function. Check for events, render objects, update objects and display the
        game window. Returns the number of lives left after the game ends. Returns -1 if all enemies
        for the current wave are destroyed.

        :return: Lives left after the game ends or -1 if all enemies are destroyed
        """
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
            # Collision detection - Get the score increment and player collision status
            score_increment, player_collision = collision(self.bullet_obj, self.enemy_obj,
                                                          self.player_obj)
            self.score += score_increment

            # If player collision is detected, game over
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
    """
    Main game function to run the game loop. If player wins, prompt to play next level. If player
    loses, prompt to play again or exit the game. Loop until the player decides to exit the game.

    :param new_game: Game object
    :return: None
    """
    while True:
        lives = new_game.run()  # Run the game loop and get the number of lives left
        current_waves = new_game.enemy_obj.waves
        current_enemies_per_wave = new_game.enemy_obj.num_enemies_per_wave
        print("Lives = ", lives)
        start_score = current_waves * current_enemies_per_wave
        if lives > 0:
            # Player lost but has lives left, prompt to retry or exit
            choice = utils.try_again(new_game)
            if choice:
                # Retry the game with the same difficulty
                new_game = Game(new_game.enemy_obj.waves, new_game.enemy_obj.num_enemies_per_wave,
                                current_score=start_score, current_lives=lives)
            else:
                utils.goodbye()
                pygame.quit()
                sys.exit()
        elif lives == 0:
            # Player lost and has no lives left, prompt to retry or exit
            choice = utils.try_again(new_game)
            if choice:
                # Start a new game from the beginning
                new_game = Game()
            else:
                utils.goodbye()
                pygame.quit()
                sys.exit()
        elif lives == -1:
            # Player won, prompt to play the next level
            play_next = utils.winner(new_game)
            if play_next:
                # Increase difficulty for the next level
                new_game = Game(current_waves=current_waves + 1,
                                current_enemies_per_wave=current_enemies_per_wave + 3,
                                current_score=new_game.score, current_lives=new_game.lives)
            else:
                utils.goodbye()
                pygame.quit()
                sys.exit()
        print("New lives = ", new_game.lives)


if __name__ == '__main__':
    game = Game()
    playgame(game)
