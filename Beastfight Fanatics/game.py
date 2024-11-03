# game.py

import random
import time
from player_board import PlayerBoard
from unit import Phoenix, Lion, Salamander, Dragon, Scorpion, Bear, Deer, Frog, Mushroom, Squirrel

class Game:
    def __init__(self, screen_width, screen_height):
        self.board = PlayerBoard(screen_width, screen_height)

        # Define possible fire and grass units with specific ranges
        fire_units = [Phoenix(), Lion(), Salamander(), Dragon(), Scorpion()]
        grass_units = [Bear(), Deer(), Frog(), Mushroom(), Squirrel()]

        # Randomly select 3 fire and 3 grass units
        self.units = random.sample(fire_units, 3) + random.sample(grass_units, 3)

        # Place units on random positions on the board without overlap
        self.place_units_randomly()

        # Timer for controlling movement and attack frequency
        self.game_start_time = time.time()
        self.last_action_time = self.game_start_time
        self.action_interval = 1.5  # Start with 1.5-second delay

    def place_units_randomly(self):
        """Place each unit at a random position on the board without overlap."""
        occupied_positions = set()
        for unit in self.units:
            while True:
                x = random.randint(0, 11)  # 12 columns
                y = random.randint(0, 3)   # 4 rows
                if (x, y) not in occupied_positions:
                    self.board.place_unit(unit, x, y)
                    occupied_positions.add((x, y))
                    break

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
                    # Calculate the direction for the shortest move (one unit at a time)
                    dx = target.x - unit.x
                    dy = target.y - unit.y

                    # Move horizontally if closer horizontally, otherwise move vertically
                    new_x, new_y = unit.x, unit.y
                    if abs(dx) > abs(dy):
                        new_x += 1 if dx > 0 else -1
                    elif abs(dy) > abs(dx):
                        new_y += 1 if dy > 0 else -1
                    else:
                        # If dx == dy (moving diagonally), prioritize horizontal or vertical moves
                        new_x += 1 if dx > 0 else -1 if dx < 0 else 0
                        new_y += 1 if dy > 0 else -1 if dy < 0 else 0

                    # Update the board with the new position
                    self.board.place_unit(unit, new_x, new_y)

    def start_combat(self):
        """Combat loop: Units attempt to attack if in range."""
        for unit in self.units:
            for target in self.units:
                if target != unit and target.health > 0 and unit.can_attack(target):
                    unit.attack_enemy(target)
                    if target.health <= 0:
                        print(f"{target.name} has been defeated!")
                        self.board.grid[target.y][target.x] = None
                        self.units.remove(target)

    def update(self):
        """Update game state with an initial 1.5-second pause, then move every 0.75 seconds."""
        current_time = time.time()

        # Initial 1.5-second pause
        if current_time - self.game_start_time < 1.5:
            return  # Pause the game for the first 1.5 seconds

        # After 1.5 seconds, change interval to 0.75 seconds
        if self.action_interval != 0.75:
            self.action_interval = 0.75  # Set new interval to 0.75 seconds after initial pause

        # Execute movement and combat if 0.75 seconds have passed since last action
        if current_time - self.last_action_time >= self.action_interval:
            self.execute_movement()
            self.start_combat()
            self.last_action_time = current_time  # Reset the timer

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear screen (optional if background is set)
        self.board.draw(screen)
