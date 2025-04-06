import pygame
import threading

class Ability:
    def __init__(self, owner):
        self.owner = owner  # Reference to the unit that owns this ability

    def trigger(self):
        """Trigger the ability. To be implemented by subclasses."""
        pass

import pygame
import time

class LionAbility(Ability):
    def __init__(self, owner):
        super().__init__(owner)
        self.icon = pygame.image.load("Fire Characters/lioabil.png")  # Load the ability icon
        self.icon_timer = 0  # Track how long the icon should display
        self.icon_duration = 0.5  # Display for 2 seconds

    def trigger(self):
        """Activate the Lion's ability and display an icon."""
        self.owner.attack_damage += 20  # Increase attack damage
        self.owner.attack_speed = max(0.5, self.owner.attack_speed - 0.2)  # Faster attack (lower interval)
        self.owner.current_mana = 0  # Reset mana to 0 after ability activation
        self.icon_timer = time.time()  # Start the icon display timer
        print(f"{self.owner.name}'s ability activated! Attack damage: {self.owner.attack_damage}, Attack speed: {self.owner.attack_speed}")

class SalamanderAbility(Ability):
    def __init__(self, owner):
        super().__init__(owner)
        self.damage_duration = 2.0  # Total duration for damage (in seconds)
        self.damage_interval = 0.5  # Time between each damage tick

    def trigger(self, target):
        """Apply the Salamander's ability to the unit it is attacking."""
        if not target or target.health <= 0:
            print(f"{self.owner.name}'s ability failed: No valid target.")
            return

        print(f"{self.owner.name}'s ability triggered! Burning {target.name} for 5% of its max health over 2 seconds.")
        self.owner.current_mana = 0  # Reset mana after ability activation
        self.apply_damage_over_time(target)

    def apply_damage_over_time(self, target):
        """Deal 5% of max health as damage to the target over 2 seconds."""
        ticks = int(self.damage_duration / self.damage_interval)  # Total number of damage ticks
        damage_per_tick = target.max_health * 0.15 / ticks  # Calculate damage per tick

        def apply_tick_damage(tick):
            if tick > 0 and target.health > 0:  # Ensure the target is alive
                target.health -= damage_per_tick
                print(f"{target.name} takes {damage_per_tick:.2f} burn damage. Health: {target.health:.2f}")
                if target.health <= 0:
                    print(f"{target.name} has been defeated!")
                    target.health = 0  # Clamp health to 0
                threading.Timer(self.damage_interval, apply_tick_damage, args=(tick - 1,)).start()

        # Start the first tick
        apply_tick_damage(ticks)

