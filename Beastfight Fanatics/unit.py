# unit.py
import pygame
import time

# Base Unit Class
# unit.py

import time

class Unit:
    def __init__(self, name, attack, health, ability_description, image_path, attack_speed, attack_range):
        self.name = name
        self.attack = attack
        self.health = health
        self.max_health = health
        self.ability_description = ability_description
        self.attack_speed = attack_speed
        self.attack_interval = 1 / attack_speed
        self.attack_range = attack_range
        self.last_attack_time = time.time()
        self.x, self.y = 0, 0  # Initialize position

        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (98, 98))
        except pygame.error as e:
            print(f"Could not load image for {name} at {image_path}: {e}")
            self.image = None

    def can_attack(self, target):
        """Check if the unit can attack the target based on its range."""
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        if self.attack_range == 'close':
            return distance == 1
        elif self.attack_range == 'medium':
            return distance <= 2
        elif self.attack_range == 'long':
            knight_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]
            return distance <= 3 or (abs(self.x - target.x), abs(self.y - target.y)) in knight_moves
        return False

    def attack_enemy(self, enemy):
        """Attack the enemy if enough time has passed since the last attack."""
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_interval:
            if self.can_attack(enemy):
                print(f"{self.name} attacks {enemy.name} for {self.attack} damage!")
                enemy.health -= self.attack
                self.last_attack_time = current_time  # Reset last attack time after attacking


# Fire Characters
class Phoenix(Unit):
    def __init__(self):
        super().__init__("Phoenix", attack=5, health=30, ability_description="Revives after death if mana is full.",
                         image_path="Fire Characters/phe1.png", attack_speed=0.5, attack_range="long")

class Lion(Unit):
    def __init__(self):
        super().__init__("Lion", attack=8, health=25, ability_description="Gains bonus AD every 5 attacks.",
                         image_path="Fire Characters/lio1.png", attack_speed=0.4, attack_range="close")

class Salamander(Unit):
    def __init__(self):
        super().__init__("Salamander", attack=6, health=35, ability_description="Burns enemies when mana is full.",
                         image_path="Fire Characters/sal1.png", attack_speed=0.3, attack_range="close")

class Dragon(Unit):
    def __init__(self):
        super().__init__("Dragon", attack=10, health=40, ability_description="AOE damage when mana is full.",
                         image_path="Fire Characters/dra1.png", attack_speed=0.2, attack_range="medium")

class Scorpion(Unit):
    def __init__(self):
        super().__init__("Scorpion", attack=9, health=28, ability_description="Deals high damage to close enemies.",
                         image_path="Fire Characters/scr1.png", attack_speed=0.25, attack_range="close")

# Grass Characters
class Bear(Unit):
    def __init__(self):
        super().__init__("Bear", attack=7, health=35, ability_description="Powerful melee unit.",
                         image_path="Grass Characters/bea1.png", attack_speed=0.5, attack_range="close")

class Deer(Unit):
    def __init__(self):
        super().__init__("Deer", attack=5, health=30, ability_description="Fast and agile unit.",
                         image_path="Grass Characters/dee1.png", attack_speed=0.6, attack_range="medium")

class Frog(Unit):
    def __init__(self):
        super().__init__("Frog", attack=4, health=25, ability_description="Leaps to dodge attacks.",
                         image_path="Grass Characters/fro1.png", attack_speed=0.7, attack_range="long")

class Mushroom(Unit):
    def __init__(self):
        super().__init__("Mushroom", attack=6, health=20, ability_description="Releases spores on death.",
                         image_path="Grass Characters/mus1.png", attack_speed=0.4, attack_range="close")

class Squirrel(Unit):
    def __init__(self):
        super().__init__("Squirrel", attack=3, health=15, ability_description="Quick but fragile.",
                         image_path="Grass Characters/squ1.png", attack_speed=0.8, attack_range="close")
