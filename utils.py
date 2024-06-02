"""
Filename : utils.py
Author : Archit
Date Created : 6/2/2024
Description : 
Language : python3
"""
import sys

import pygame

from updates import DISPLAY_WIDTH, DISPLAY_HEIGHT


def try_again(game):
    """
    Function to display the try again screen
    :return: None
    """
    # Display score, try again message and take input
    game.screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 25)
    score_text = font.render(f"Score: {game.score}   Lives: {game.lives}", True, (255, 255, 255))

    try_again_text = font.render("Press 'ENTER' to try again or 'ESC' to quit", True,
                                 (255, 255, 255))
    game.screen.blit(score_text, (DISPLAY_WIDTH // 2 - 50, DISPLAY_HEIGHT // 2 - 50))
    game.screen.blit(try_again_text, (DISPLAY_WIDTH // 2 - 100, DISPLAY_HEIGHT // 2))
    pygame.display.flip()
    # Wait for 'R' key press to restart the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.score = 0
                    game.lives = 3
                    return 1
                elif event.key == pygame.K_ESCAPE:
                    return 2
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def goodbye():
    """
    Function to display the goodbye screen
    :return: None
    """
    # Display score, try again message and take input
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    goodbye_text = font.render("Goodbye!", True, (255, 255, 255))
    screen.blit(goodbye_text, (DISPLAY_WIDTH // 2 - 50, DISPLAY_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()
