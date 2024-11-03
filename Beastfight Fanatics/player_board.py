# player_board.py

import pygame


class PlayerBoard:
    def __init__(self, screen_width, screen_height):
        self.grid_width = 12
        self.grid_height = 4
        self.cell_size = min(screen_width // self.grid_width, screen_height // 8)
        self.grid = [[None for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Calculate offsets to center the grid horizontally and position it at the bottom
        self.offset_x = (screen_width - (self.grid_width * self.cell_size)) // 2
        self.offset_y = screen_height - (self.grid_height * self.cell_size) - 50

        # Load the background image
        try:
            self.background = pygame.image.load("Fire Characters/background.png")
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except pygame.error as e:
            print(f"Could not load background image: {e}")
            self.background = None

    def place_unit(self, unit, x, y):
        """Place unit at a new position on the grid and update its coordinates."""
        if 0 <= unit.y < self.grid_height and 0 <= unit.x < self.grid_width:
            self.grid[unit.y][unit.x] = None
        unit.x, unit.y = x, y
        self.grid[y][x] = unit

    def draw(self, screen):
        """Draw the background, grid, units, and health bars."""
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Draw 12x4 grid lines centered at the bottom of the screen
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(
                    self.offset_x + x * self.cell_size,
                    self.offset_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        # Draw each unit and its health bar
        for y, row in enumerate(self.grid):
            for x, unit in enumerate(row):
                if unit and unit.image:
                    # Position the unit image within the cell
                    unit_x = self.offset_x + x * self.cell_size + (self.cell_size - unit.image.get_width()) // 2
                    unit_y = self.offset_y + y * self.cell_size + (self.cell_size - unit.image.get_height()) // 2
                    screen.blit(unit.image, (unit_x, unit_y))

                    # Draw health bar above the unit image
                    health_bar_width = int(self.cell_size * 0.9)  # Health bar width is 90% of cell size
                    health_bar_height = 8  # Increase height to 8 pixels
                    health_ratio = unit.health / unit.max_health
                    health_bar_color = (255, 206, 27)  # Mustard yellow
                    health_bar_x = unit_x + (self.cell_size - health_bar_width) // 2
                    health_bar_y = unit_y - 12  # Position the health bar a bit higher above the unit

                    # Draw the background of the health bar (red)
                    pygame.draw.rect(screen, (255, 0, 0),
                                     (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

                    # Draw the current health (mustard yellow)
                    pygame.draw.rect(screen, health_bar_color, (
                    health_bar_x, health_bar_y, int(health_bar_width * health_ratio), health_bar_height))
