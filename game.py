import random
import time

from player_board import PlayerBoard
from unit import Phoenix, Lion, Salamander, Dragon, Scorpion, Dummy

class Game:
    def __init__(self, screen_width, screen_height):
        self.board = PlayerBoard(screen_width, screen_height)
        # Update projectiles and remove those that hit the target
        self.projectile = []

        # Fire Character Pool
        self.fire_character_pool = [
            Phoenix(), Lion(), Salamander(), Dragon(), Scorpion()
        ]

        # Generate Target Dummy and a random Fire unit
        self.units = [Dragon()]  # Always include the Target Dummy
        self.units.append(Phoenix())  # Add a random Fire unit

        # Place the Target Dummy and Fire unit
        self.place_units()

        # Timer for controlling movement and attack frequency
        self.game_start_time = time.time()
        self.last_action_time = self.game_start_time
        self.action_interval = 1.5  # Start with 1.5-second delay

    def place_units(self):
        """Place the Target Dummy at the top and the Fire unit at the bottom."""
        # Target Dummy at the top center
        self.board.place_unit(self.units[0], x=self.board.grid_width // 2, y=0)

        # Fire unit at the bottom center
        self.board.place_unit(self.units[1], x=self.board.grid_width // 2, y=self.board.grid_height - 1)

    def calculate_distance(self, unit, target):
        """Calculate Manhattan distance between two units (diagonal counts as 2 units)."""
        dx = abs(unit.x - target.x)
        dy = abs(unit.y - target.y)
        return dx + dy if dx == 0 or dy == 0 else dx + dy + 1

    def find_nearest_target(self, unit):
        """Find the nearest enemy unit for a given unit."""
        nearest_target = None
        min_distance = float('inf')
        for target in self.units:
            if target != unit and target.health > 0:
                distance = self.calculate_distance(unit, target)
                if distance < min_distance:
                    min_distance = distance
                    nearest_target = target
        return nearest_target

    def execute_movement(self):
        """Move each unit according to its range and proximity to nearest enemy."""
        for unit in self.units:
            if unit.health <= 0:
                continue  # Skip dead units

            # Check if there is any target in range
            in_combat = False
            for target in self.units:
                if target != unit and target.health > 0 and unit.can_attack(target):
                    in_combat = True
                    break

            # Move towards the nearest target if not in combat
            if not in_combat:
                target = self.find_nearest_target(unit)
                if target:
                    dx = target.x - unit.x
                    dy = target.y - unit.y
                    new_x = unit.x + (1 if dx > 0 else -1 if dx < 0 else 0)
                    new_y = unit.y + (1 if dy > 0 else -1 if dy < 0 else 0)

                    # Place the unit at the new position
                    self.board.place_unit(unit, new_x, new_y)

    def start_combat(self):
        """Combat loop: Units attempt to attack if in range."""
        for unit in self.units:
            if unit.health <= 0:
                continue  # Skip defeated units

            # Normal attack on enemies
            for target in self.units:
                if target != unit and target.health > 0 and unit.can_attack(target):
                    projectile = unit.attack_enemy(
                        target,
                        cell_size=self.board.cell_size,
                        offset_x=self.board.offset_x,
                        offset_y=self.board.offset_y
                    )

                    if projectile:  # If a projectile was created
                        self.projectile.append(projectile)  # Add it to the game’s projectile list

                    if target.health <= 0:  # Handle target death
                        print(f"{target.name} has been defeated!")
                        self.handle_unit_death(target)

    def handle_unit_death(self, unit):
        """Remove a defeated unit from the grid and update its position to None."""
        if unit.health <= 0:
            print(f"{unit.name} has been defeated!")
            # Clear the grid position for the defeated unit
            self.board.grid[unit.y][unit.x] = None
            # Remove the unit from the units list
            self.units.remove(unit)

    def update(self):
        """Update game state."""
        current_time = time.time()

        # Initial pause logic
        if current_time - self.game_start_time < 1.5:
            return  # Pause for the first 1.5 seconds

        if self.action_interval != 0.75:
            self.action_interval = 0.75  # Update interval after the initial pause

        self.execute_movement()
        self.start_combat()
        self.last_action_time = current_time  # Reset timer

        # Update and remove projectiles that hit their target
        for projectile in list(self.projectile):  # Use a copy of the list to modify safely
            if projectile.update():  # If projectile hits the target
                self.projectile.remove(projectile)

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear the screen
        self.board.draw(screen)  # Draw the board, units, and bars
        for projectile in self.projectile:
            projectile.draw(screen)
