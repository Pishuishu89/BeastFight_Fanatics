# main.py

import pygame
from game import Game

def main():
    # Initialize Pygame and set to full-screen mode
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Full-screen mode
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Beastfight Fanatics")

    # Initialize Game
    game = Game(screen_width, screen_height)

    # Game Loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the exit button was clicked
                if exit_button.collidepoint(event.pos):
                    running = False

        # Update game (includes both movement and combat)
        game.update()

        # Draw game state
        game.draw(screen)

        # Draw the exit button
        exit_button = pygame.Rect(screen_width - 100, 10, 90, 40)
        pygame.draw.rect(screen, (255, 206, 27), exit_button)  # Golden color
        font = pygame.font.Font(None, 36)
        text = font.render("EXIT", True, (255, 255, 255))  # White text
        screen.blit(text, (screen_width - 85, 15))

        # Update display
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
