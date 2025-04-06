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
        """Place a unit at a specific grid position. If occupied, find the next closest empty space."""
        while y < self.grid_height and self.grid[y][x] is not None:
            y += 1  # Move downward
            if y >= self.grid_height:
                y = 0  # Wrap around to the top
                x = (x + 1) % self.grid_width  # Move to the next column

        # Place the unit in the found position
        if self.grid[y][x] is None:
            # Clear previous position
            if 0 <= unit.y < self.grid_height and 0 <= unit.x < self.grid_width:
                self.grid[unit.y][unit.x] = None

            # Update unit's position
            unit.x, unit.y = x, y
            self.grid[y][x] = unit
            return True
        return False

    def draw(self, screen):
        """Draw the background, grid, units, health bars, and resource bars."""
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Draw grid lines
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(
                    self.offset_x + x * self.cell_size,
                    self.offset_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

        # Draw each unit and its bars
        for y, row in enumerate(self.grid):
            for x, unit in enumerate(row):
                if unit and unit.image:
                    self.draw_unit(screen, unit, x, y)

    def draw_unit(self, screen, unit, grid_x, grid_y):
        """Draw a unit, its health bar, and its resource bar."""
        # Position calculations
        unit_x = self.offset_x + grid_x * self.cell_size + (self.cell_size - unit.image.get_width()) // 2
        unit_y = self.offset_y + grid_y * self.cell_size + (self.cell_size - unit.image.get_height()) // 2
        screen.blit(unit.image, (unit_x, unit_y))

        # Health bar
        health_bar_width = int(self.cell_size * 0.9)
        health_bar_height = 8
        health_ratio = unit.health / unit.max_health
        health_bar_x = unit_x + (self.cell_size - health_bar_width) // 2
        health_bar_y = unit_y - 12  # Position above the unit image

        # Draw health bar
        self.draw_bar(
            screen,
            health_bar_x,
            health_bar_y,
            health_bar_width,
            health_bar_height,
            health_ratio,
            (255, 0, 0),  # Background color (red)
            (255, 206, 27)  # Fill color (mustard yellow)
        )

        # Resource bar
        magic_bar_height = 6
        magic_bar_x = health_bar_x
        magic_bar_y = health_bar_y + health_bar_height + 2

        # Determine resource bar colors
        if unit.hasMana:
            magic_ratio = unit.current_mana / unit.mana_pool
            magic_bar_color = (0, 0, 128)  # Dark blue for mana
            magic_fill_color = (0, 0, 255)  # Bright blue for filled mana
        else:
            magic_ratio = unit.current_mana / unit.mana_pool
            magic_bar_color = (128, 0, 0)  # Dark red for rage
            magic_fill_color = (255, 0, 0)  # Bright red for filled rage

        # Draw resource bar
        self.draw_bar(
            screen,
            magic_bar_x,
            magic_bar_y,
            health_bar_width,
            magic_bar_height,
            magic_ratio,
            magic_bar_color,
            magic_fill_color
        )

    @staticmethod
    def draw_bar(screen, x, y, width, height, ratio, bg_color, fill_color):
        """Draw a bar (health, mana, rage, etc.) with the specified parameters."""
        # Background bar
        pygame.draw.rect(screen, bg_color, (x, y, width, height))
        # Filled portion
        filled_width = int(width * ratio)  # Calculate the width of the filled portion
        pygame.draw.rect(screen, fill_color, (x, y, filled_width, height))
