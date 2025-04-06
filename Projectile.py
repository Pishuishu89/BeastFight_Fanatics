import pygame

class Projectile:
    def __init__(self, image_path, start_x, start_y, target_unit, cell_size, offset_x, offset_y, speed=5):
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (48,48)) #change to 48 48
        except pygame.error as e:
            print(f"Error loading projectile image: {e}")
            self.image = None  # Fallback for error handling

        self.x = start_x
        self.y = start_y
        self.target_unit = target_unit
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.speed = speed

    def update(self):
        """Move the projectile closer to the target's current position."""
        # Dynamically calculate the target's current pixel coordinates
        target_x = self.target_unit.x * self.cell_size + self.offset_x + self.target_unit.image.get_width() // 2
        target_y = self.target_unit.y * self.cell_size + self.offset_y + self.target_unit.image.get_height() // 2

        # Recalculate direction
        dx = target_x - self.x
        dy = target_y - self.y
        distance = max((dx**2 + dy**2)**0.5, 1e-5)  # Prevent division by zero
        dir_x = dx / distance
        dir_y = dy / distance

        # Move the projectile
        self.x += dir_x * self.speed
        self.y += dir_y * self.speed

        # Check if the projectile has hit the target
        return self.has_hit_target(target_x, target_y)

    def has_hit_target(self, target_x, target_y):
        """Check if the projectile is close enough to the target's current position."""
        return ((self.x - target_x)**2 + (self.y - target_y)**2)**0.5 < self.speed

    def draw(self, screen):
        """Render the projectile on the screen."""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
