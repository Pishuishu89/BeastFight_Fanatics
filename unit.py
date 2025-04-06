import pygame
import time
import random

from Projectile import Projectile
from Ability import LionAbility, SalamanderAbility


class Unit:
    def __init__(
            self,
            name="Unit",
            health=100,
            mana_pool=100,
            mana_regen=10,
            attack_range="close",
            attack_damage=10,
            attack_speed=1.0,
            crit_chance=0.1,
            ability_power=0,
            class_type="Neutral",
            trait="None",
            ability_description="No ability",
            image_path="",
            current_mana=0,
            hasMana=True,
            needsTarget=False,
    ):
        # Core stats
        self.name = name
        self.health = health
        self.max_health = health
        self.mana_pool = mana_pool
        self.current_mana = current_mana
        self.mana_regen = mana_regen
        self.attack_range = attack_range
        self.attack_damage = attack_damage
        self.attack_speed = attack_speed
        self.crit_chance = crit_chance
        self.ability_power = ability_power
        self.class_type = class_type
        self.trait = trait
        self.ability_description = ability_description
        self.hasMana = hasMana
        self.ability = None  # Ability assigned to the unit
        self.needsTarget = needsTarget
        # Load character image
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (98, 98))
        except pygame.error as e:
            print(f"Could not load image for {name} at {image_path}: {e}")
            self.image = None

        # Attack mechanics
        self.last_attack_time = time.time()
        self.attack_interval = 1 / attack_speed
        self.x, self.y = 0, 0  # Initialize position

    def attack_enemy(self, enemy, cell_size, offset_x, offset_y):
        """Attack an enemy unit and regenerate mana/rage on attack."""
        if self.health <= 0:
            return  # Defeated units cannot attack

        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_interval:
            if self.can_attack(enemy):
                is_critical = random.random() < self.crit_chance
                damage = self.attack_damage * 1.5 if is_critical else self.attack_damage
                print(f"{self.name} attacks {enemy.name} for {damage:.2f} damage!{' (Critical Hit!)' if is_critical else ''}")
                enemy.health -= damage  # Apply damage
                self.last_attack_time = current_time
                print(f"{self.name} attacks {enemy.name} for {self.attack_damage} damage!")
                enemy.health -= self.attack_damage  # Apply damage
                self.last_attack_time = current_time

                # Regenerate resource on attack using mana_regen
                self.current_mana = min(self.current_mana + self.mana_regen, self.mana_pool)
                resource_name = "mana" if self.hasMana else "rage"
                print(f"{self.name} gains {resource_name} on attack: {self.current_mana}/{self.mana_pool}")

                # Trigger mana regeneration for the enemy when attacked
                if enemy.health > 0 and enemy.hasMana:  # Ensure the enemy is alive and has mana
                    enemy.gain_mana_when_attacked()

                if self.current_mana == self.mana_pool and self.ability and self.needsTarget == True:
                    self.ability.trigger(enemy)  # Pass the target enemy to the ability
                if self.current_mana == self.mana_pool and self.ability and self.needsTarget == False:
                    self.ability.trigger()

                # Create a projectile
                projectile_image = (
                    "Fire Characters/firecc.png"
                    if self.attack_range == "close"
                    else "Fire Characters/firelr.png"
                )
                projectile = Projectile(
                    image_path=projectile_image,
                    start_x=self.x * cell_size + offset_x + (self.image.get_width() // 2) - (32 // 2),
                    # Adjust for projectile size (e.g., 32x32)
                    start_y=self.y * cell_size + offset_y + (self.image.get_height() // 2) - (32 // 2),
                    # Adjust for projectile size
                    target_unit=enemy,
                    cell_size=cell_size,
                    offset_x=offset_x,
                    offset_y=offset_y,
                    speed=5
                )

                return projectile

    def gain_mana_when_attacked(self):
        """Gain mana equal to 30% of mana_regen when taking damage."""
        if self.hasMana:
            mana_gain = self.mana_regen * 0.3  # 30% of mana_regen
            previous_mana = self.current_mana
            self.current_mana = min(self.current_mana + mana_gain, self.mana_pool)
            print(f"{self.name} gains mana when attacked: {self.current_mana:.2f}/{self.mana_pool}")

    def can_attack(self, target):
        """Check if this unit can attack a target based on range."""
        distance_x = abs(self.x - target.x)
        distance_y = abs(self.y - target.y)

        if self.attack_range == 'close':
            return distance_x <= 1 and distance_y <= 1
        elif self.attack_range == 'medium':
            return distance_x <= 2 and distance_y <= 2
        elif self.attack_range == 'long':
            knight_moves = [(2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2)]
            return distance_x <= 3 or (distance_x, distance_y) in knight_moves
        return False


# Fire Characters
class Phoenix(Unit):
    def __init__(self):
        super().__init__(
            name="Inferna",
            health=400,
            mana_pool=100,
            mana_regen=17,
            attack_range="long",
            attack_damage=50,
            attack_speed=0.75,
            crit_chance=0.15,
            ability_power=125,
            class_type="Fire",
            trait="Mythical, Sharpshooter",
            ability_description="Inferna starts to shoot an extra attack (for the round) after casting.",
            image_path="Fire Characters/phe1.png",
            current_mana=0,
            hasMana=True
        )


class Lion(Unit):
    def __init__(self):
        super().__init__(
            name="Pyroar",
            health=395,
            mana_pool=100,
            mana_regen=20,
            attack_range="close",
            attack_damage=55,
            attack_speed=0.6,
            crit_chance=0.20,
            ability_power=0,
            class_type="Fire",
            trait="Rager, Marauders",
            ability_description="Pyroar has no mana. Upon attacking 5 times, Pyroar will gain 15 Attack Damage and 20% attack speed (x1.2)",
            image_path="Fire Characters/lio1.png",
            current_mana=100,
            hasMana=False,
            needsTarget = False
        )
        self.ability = LionAbility(self)


class Salamander(Unit):
    def __init__(self):
        super().__init__(
            name="Blazetail",
            health=500,
            mana_pool=100,
            mana_regen=22,
            attack_range="close",
            attack_damage=35,
            attack_speed=0.4,
            crit_chance=0.15,
            ability_power=150,
            class_type="Fire",
            trait="Sentinels",
            ability_description="Blazetail burns enemies, doing 15% of their max health as damage over 3 seconds.",
            image_path="Fire Characters/sal1.png",
            current_mana=0,
            hasMana=True,
            needsTarget=True
        )
        self.ability = SalamanderAbility(self)


class Dragon(Unit):
    def __init__(self):
        super().__init__(
            name="Ignis",
            health=750,
            mana_pool=100,
            mana_regen=25,
            attack_range="medium",
            attack_damage=40,
            attack_speed=0.4,
            crit_chance=0.15,
            ability_power=250,
            class_type="Fire",
            trait="Sharpshooter",
            ability_description="Ignis does AOE damage to his current target.",
            image_path="Fire Characters/dra1.png",
            current_mana=0,
            hasMana=True,
            needsTarget = True
        )
        #self.ability = DragonAbility(self)

class Scorpion(Unit):
    def __init__(self):
        super().__init__(
            name="Magma Scourge",
            health=400,
            mana_pool=100,
            mana_regen=23,
            attack_range="close",
            attack_damage=45,
            attack_speed=0.7,
            crit_chance=0.15,
            ability_power=75,
            class_type="Fire",
            trait="Stunners",
            ability_description="Stuns the current target for 1.5 seconds.",
            image_path="Fire Characters/Scr1.png",
            current_mana=0,
            hasMana=True,
            needsTarget = True
        )


# Grass Characters
class Bear(Unit):
    def __init__(self):
        super().__init__(
            name="Bear",
            health=35,
            mana_pool=100,
            mana_regen=15,
            attack_range="close",
            attack_damage=7,
            attack_speed=0.4,
            crit_chance=0.15,
            ability_power=0,
            class_type="Grass",
            trait="Bear",
            ability_description="Heals himself for 2 seconds.",
            image_path="Grass Characters/bea1.png",
            current_mana=0,
            hasMana=True
        )


class Deer(Unit):
    def __init__(self):
        super().__init__(
            name="Deer",
            health=30,
            mana_pool=100,
            mana_regen=20,
            attack_range="medium",
            attack_damage=5,
            attack_speed=0.6,
            crit_chance=0.15,
            ability_power=15,
            class_type="Grass",
            trait="Spellweaver",
            ability_description="Increases magic amount after cast.",
            image_path="Grass Characters/dee1.png",
            current_mana=0,
            hasMana=True
        )


class Frog(Unit):
    def __init__(self):
        super().__init__(
            name="Frog",
            health=25,
            mana_pool=100,
            mana_regen=18,
            attack_range="long",
            attack_damage=4,
            attack_speed=0.7,
            crit_chance=0.15,
            ability_power=10,
            class_type="Grass",
            trait="Aegis",
            ability_description="Gives teammates steroids that increase their attack speed.",
            image_path="Grass Characters/fro1.png",
            current_mana=0,
            hasMana=True
        )


class Mushroom(Unit):
    def __init__(self):
        super().__init__(
            name="Mushroom",
            health=20,
            mana_pool=100,
            mana_regen=-28,
            attack_range="close",
            attack_damage=6,
            attack_speed=0.4,
            crit_chance=0.15,
            ability_power=15,
            class_type="Grass",
            trait="Mythicals, Rager",
            ability_description="Releases spores.",
            image_path="Grass Characters/mus1.png",
            current_mana=100,
            hasMana=False
        )


class Squirrel(Unit):
    def __init__(self):
        super().__init__(
            name="Squirrel",
            health=15,
            mana_pool=100,
            mana_regen=17,
            attack_range="close",
            attack_damage=3,
            attack_speed=0.8,
            crit_chance=0.15,
            ability_power=5,
            class_type="Grass",
            trait="Striker",
            ability_description="Has a snack.",
            image_path="Grass Characters/squ1.png",
            current_mana=0,
            hasMana=True
        )


class Crocodile(Unit):
    def __init__(self):
        super().__init__(
            name="Crocodile",
            health=35,
            mana_pool=100,
            mana_regen=15,
            attack_range="close",
            attack_damage=10,
            attack_speed=0.3,
            crit_chance=0.15,
            ability_power=20,
            class_type="Water",
            trait="Sentinels",
            ability_description="Powerful bite with high defense.",
            image_path="Water Characters/cro1.png",
            current_mana=0,
            hasMana=True
        )


class Goldfish(Unit):
    def __init__(self):
        super().__init__(
            name="Goldfish",
            health=15,
            mana_pool=100,
            mana_regen=10,
            attack_range="medium",
            attack_damage=3,
            attack_speed=0.8,
            crit_chance=0.15,
            ability_power=8,
            class_type="Water",
            trait="Arcanist",
            ability_description="Low attack but fast swimmer.",
            image_path="Water Characters/gol1.png",
            current_mana=0,
            hasMana=True
        )


class Jellyfish(Unit):
    def __init__(self):
        super().__init__(
            name="Jellyfish",
            health=20,
            mana_pool=100,
            mana_regen=12,
            attack_range="long",
            attack_damage=5,
            attack_speed=0.6,
            crit_chance=0.15,
            ability_power=15,
            class_type="Water",
            trait="Mythicals, Spellweaver",
            ability_description="Electric stings with paralyzing effect.",
            image_path="Water Characters/jel1.png",
            current_mana=0,
            hasMana=True
        )


class Octopus(Unit):
    def __init__(self):
        super().__init__(
            name="Octopus",
            health=28,
            mana_pool=100,
            mana_regen=15,
            attack_range="medium",
            attack_damage=7,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Water",
            trait="Arcanist",
            ability_description="Can camouflage and escape attacks.",
            image_path="Water Characters/oct1.png",
            current_mana=0,
            hasMana=True
        )


class Otter(Unit):
    def __init__(self):
        super().__init__(
            name="Otter",
            health=18,
            mana_pool=100,
            mana_regen=10,
            attack_range="medium",
            attack_damage=4,
            attack_speed=0.7,
            crit_chance=0.15,
            ability_power=12,
            class_type="Water",
            trait="Otter",
            ability_description="Playful yet agile with water attacks.",
            image_path="Water Characters/ott1.png",
            current_mana=0,
            hasMana=True
        )


# Wind Characters
class Cheetah(Unit):
    def __init__(self):
        super().__init__(
            name="Cheetah",
            health=22,
            mana_pool=100,
            mana_regen=-8,
            attack_range="close",
            attack_damage=9,
            attack_speed=0.9,
            crit_chance=0.15,
            ability_power=10,
            class_type="Wind",
            trait="Rager",
            ability_description="Fastest land animal, hits hard.",
            image_path="Wind Characters/che1.png",
            current_mana=100,
            hasMana=False
        )


class Eagle(Unit):
    def __init__(self):
        super().__init__(
            name="Eagle",
            health=25,
            mana_pool=100,
            mana_regen=15,
            attack_range="medium",
            attack_damage=7,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=12,
            class_type="Wind",
            trait="Sharpshooters",
            ability_description="Attacks with sharp talons from above.",
            image_path="Wind Characters/eag1.png",
            current_mana=0,
            hasMana=True
        )


class Hare(Unit):
    def __init__(self):
        super().__init__(
            name="Hare",
            health=23,
            mana_pool=100,
            mana_regen=10,
            attack_range="medium",
            attack_damage=6,
            attack_speed=0.6,
            crit_chance=0.15,
            ability_power=8,
            class_type="Wind",
            trait="Sharpshooters, Stunners",
            ability_description="Mythical creature with wind gusts.",
            image_path="Wind Characters/har1.png",
            current_mana=0,
            hasMana=True
        )


class Hawk(Unit):
    def __init__(self):
        super().__init__(
            name="Hawk",
            health=20,
            mana_pool=100,
            mana_regen=-12,
            attack_range="close",
            attack_damage=5,
            attack_speed=0.7,
            crit_chance=0.15,
            ability_power=10,
            class_type="Wind",
            trait="Rager",
            ability_description="Swoops down quickly for surprise attacks.",
            image_path="Wind Characters/haw1.png",
            current_mana=100,
            hasMana=False
        )


class Horse(Unit):
    def __init__(self):
        super().__init__(
            name="Horse",
            health=28,
            mana_pool=100,
            mana_regen=35,
            attack_range="close",
            attack_damage=8,
            attack_speed=0.4,
            crit_chance=0.15,
            ability_power=20,
            class_type="Wind",
            trait="Marauders",
            ability_description="Strong charge attack at close range.",
            image_path="Wind Characters/hor1.png",
            current_mana=0,
            hasMana=True
        )


# Ice Characters
class Penguin(Unit):
    def __init__(self):
        super().__init__(
            name="Penguin",
            health=18,
            mana_pool=100,
            mana_regen=15,
            attack_range="medium",
            attack_damage=4,
            attack_speed=0.6,
            crit_chance=0.15,
            ability_power=8,
            class_type="Ice",
            trait="Strikers",
            ability_description="Quick on ice, slippery to catch.",
            image_path="Ice Characters/pen1.png",
            current_mana=0,
            hasMana=True
        )


class Walrus(Unit):
    def __init__(self):
        super().__init__(
            name="Walrus",
            health=35,
            mana_pool=100,
            mana_regen=15,
            attack_range="close",
            attack_damage=8,
            attack_speed=0.3,
            crit_chance=0.15,
            ability_power=10,
            class_type="Ice",
            trait="Aegis, Stunner",
            ability_description="Large and resilient with thick skin.",
            image_path="Ice Characters/wal1.png",
            current_mana=0,
            hasMana=True
        )


class SnowLeopard(Unit):
    def __init__(self):
        super().__init__(
            name="Snow Leopard",
            health=30,
            mana_pool=100,
            mana_regen=17,
            attack_range="close",
            attack_damage=10,
            attack_speed=0.6,
            crit_chance=0.15,
            ability_power=12,
            class_type="Ice",
            trait="Arcanist",
            ability_description="Stealthy predator with high agility.",
            image_path="Ice Characters/snl1.png",
            current_mana=0,
            hasMana=True
        )


# Rock Characters
class Armadillo(Unit):
    def __init__(self):
        super().__init__(
            name="Armadillo",
            health=35,
            mana_pool=100,
            mana_regen=12,
            attack_range="close",
            attack_damage=7,
            attack_speed=0.3,
            crit_chance=0.15,
            ability_power=10,
            class_type="Rock",
            trait="Sentinels",
            ability_description="Has a hard shell for high defense.",
            image_path="Rock Characters/arm1.png",
            current_mana=0,
            hasMana=True
        )


class Elephant(Unit):
    def __init__(self):
        super().__init__(
            name="Elephant",
            health=50,
            mana_pool=100,
            mana_regen=15,
            attack_range="medium",
            attack_damage=10,
            attack_speed=0.2,
            crit_chance=0.15,
            ability_power=8,
            class_type="Rock",
            trait="Sentinels",
            ability_description="Massive and strong with long reach.",
            image_path="Rock Characters/ele1.png",
            current_mana=0,
            hasMana=True
        )


class Giraffe(Unit):
    def __init__(self):
        super().__init__(
            name="Giraffe",
            health=40,
            mana_pool=100,
            mana_regen=10,
            attack_range="long",
            attack_damage=8,
            attack_speed=0.3,
            crit_chance=0.15,
            ability_power=6,
            class_type="Rock",
            trait="Sharpshooters",
            ability_description="Uses long neck to strike from afar.",
            image_path="Rock Characters/gir1.png",
            current_mana=0,
            hasMana=True
        )


class Rhino(Unit):
    def __init__(self):
        super().__init__(
            name="Rhino",
            health=45,
            mana_pool=100,
            mana_regen=13,
            attack_range="close",
            attack_damage=9,
            attack_speed=0.25,
            crit_chance=0.15,
            ability_power=10,
            class_type="Rock",
            trait="Sentinels, Stunners",
            ability_description="Charges with high momentum.",
            image_path="Rock Characters/rhi1.png",
            current_mana=0,
            hasMana=True
        )


# Light Characters
class Butterfly(Unit):
    def __init__(self):
        super().__init__(
            name="Butterfly",
            health=15,
            mana_pool=100,
            mana_regen=10,
            attack_range="medium",
            attack_damage=-4,
            attack_speed=0.7,
            crit_chance=0.15,
            ability_power=12,
            class_type="Light",
            trait="Healer",
            ability_description="Delicate but swift with evasive maneuvers.",
            image_path="Light Characters/but1.png",
            current_mana=0,
            hasMana=True
        )


class Swan(Unit):
    def __init__(self):
        super().__init__(
            name="Swan",
            health=18,
            mana_pool=100,
            mana_regen=12,
            attack_range="medium",
            attack_damage=-5,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=15,
            class_type="Light",
            trait="Aegis, Stunner",
            ability_description="Graceful yet strong in defense.",
            image_path="Light Characters/swa1.png",
            current_mana=0,
            hasMana=True
        )


class Unicorn(Unit):
    def __init__(self):
        super().__init__(
            name="Unicorn",
            health=30,
            mana_pool=100,
            mana_regen=15,
            attack_range="long",
            attack_damage=-8,
            attack_speed=0.4,
            crit_chance=0.15,
            ability_power=20,
            class_type="Light",
            trait="Mythicals",
            ability_description="Mythical creature with healing abilities.",
            image_path="Light Characters/uni1.png",
            current_mana=0,
            hasMana=True
        )


class Bat(Unit):
    def __init__(self):
        super().__init__(
            name="Bat",
            health=20,
            mana_pool=100,
            mana_regen=10,
            attack_range="long",
            attack_damage=6,
            attack_speed=0.6,
            crit_chance=0.15,
            ability_power=15,
            class_type="Dark",
            trait="Spellweaver",
            ability_description="Attacks quickly with poison.",
            image_path="Dark Characters/bat1.png",
            current_mana=0,
            hasMana=True
        )


class Owl(Unit):
    def __init__(self):
        super().__init__(
            name="Owl",
            health=22,
            mana_pool=100,
            mana_regen=15,
            attack_range="long",
            attack_damage=5,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=12,
            class_type="Dark",
            trait="Spellweaver",
            ability_description="Attacks from afar with silent swoop.",
            image_path="Dark Characters/owl1.png",
            current_mana=0,
            hasMana=True
        )


class Panther(Unit):
    def __init__(self):
        super().__init__(
            name="Panther",
            health=30,
            mana_pool=100,
            mana_regen=12,
            attack_range="close",
            attack_damage=9,
            attack_speed=0.4,
            crit_chance=0.15,
            ability_power=20,
            class_type="Dark",
            trait="Marauders",
            ability_description="Stealthy and powerful melee unit.",
            image_path="Dark Characters/pan1.png",
            current_mana=0,
            hasMana=True
        )


class Spider(Unit):
    def __init__(self):
        super().__init__(
            name="Spider",
            health=18,
            mana_pool=100,
            mana_regen=8,
            attack_range="medium",
            attack_damage=4,
            attack_speed=0.7,
            crit_chance=0.15,
            ability_power=10,
            class_type="Dark",
            trait="Stunner",
            ability_description="Weaves webs to immobilize enemies.",
            image_path="Dark Characters/spi1.png",
            current_mana=0,
            hasMana=True
        )


class Wolf(Unit):
    def __init__(self):
        super().__init__(
            name="Wolf",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="close",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Dark",
            trait="Marauders, Strikers",
            ability_description="Strong pack animal with ferocious bite.",
            image_path="Dark Characters/wol1.png",
            current_mana=0,
            hasMana=True
        )


class DragonFruit(Unit):
    def __init__(self):
        super().__init__(
            name="Riyaz",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="close",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Fire, Grass",
            trait="Sentinel, Aegis",
            ability_description="Siphons health with attack",
            image_path="High Cost Characters/dgf1.png",
            current_mana=0,
            hasMana=True
        )


class Cat(Unit):
    def __init__(self):
        super().__init__(
            name="Ahmed",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="close",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Fire, Dark",
            trait="Strikers, Sharpshooters",
            ability_description="Throws a kunai at lowest max hp enemy. does bonus damage based on missing health. if it kills teleport to where the unit last died. if take 50% damage teleports back to old spot. ",
            image_path="High Cost Characters/cat1.png",
            current_mana=0,
            hasMana=True
        )


class Orangutan(Unit):
    def __init__(self):
        super().__init__(
            name="Cano",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="close",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Dark, Grass",
            trait="Stunners , Marauders",
            ability_description="Drops a tool that stuns enemies. Gains health for every enemy hit. Gains attack damage when hitting enemies that are stunned.",
            image_path="High Cost Characters/can1.png",
            current_mana=0,
            hasMana=True
        )


class Sloth(Unit):
    def __init__(self):
        super().__init__(
            name="Shaan",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="Medium",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Ice, Stone",
            trait="Aegis, Spellweaver",
            ability_description="Charges up for a long time and then blasts a large zone. While charging creates a shield, and does more damage the bigger the shield is.",
            image_path="High Cost Characters/slo1.png",
            current_mana=0,
            hasMana=True
        )


class Turtle(Unit):
    def __init__(self):
        super().__init__(
            name="Tamzie",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="Close",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Water, Stone",
            trait="Sentinels, Arcanist",
            ability_description="Pulls a large group of units closer and then drops a rock, gives a shield when it does that and then waterboards them",
            image_path="High Cost Characters/tur1.png",
            current_mana=0,
            hasMana=True
        )


class Banana(Unit):
    def __init__(self):
        super().__init__(
            name="Ajpiwa",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="long",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Light, Ice",
            trait="Sentinels, Arcanist",
            ability_description="drops bananas on spawn in the x squares. When enemies walk over it stun + gains ap",
            image_path="High Cost Characters/ban1.png",
            current_mana=0,
            hasMana=True
        )


class Quokka(Unit):
    def __init__(self):
        super().__init__(
            name="Artin",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="long",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Water, Wind",
            trait="Spellweaver, Sharpshooter",
            ability_description="drops bananas on spawn in the x squares. When enemies walk over it stun + gains ap",
            image_path="High Cost Characters/qua1.png",
            current_mana=0,
            hasMana=True
        )


class Jaguar(Unit):
    def __init__(self):
        super().__init__(
            name="",
            health=25,
            mana_pool=100,
            mana_regen=10,
            attack_range="Close",
            attack_damage=8,
            attack_speed=0.5,
            crit_chance=0.15,
            ability_power=18,
            class_type="Wind, Light",
            trait="Spellweaver, Sharpshooter",
            ability_description="Just uses close combat or smth",
            image_path="High Cost Characters/jag1.png",
            current_mana=0,
            hasMana=False
        )


class Dummy(Unit):
    def __init__(self):
        super().__init__(
            name="Target Dummy",
            health=1000,
            mana_pool=0.0000001,
            mana_regen=0.0000001,
            attack_range="long",
            attack_damage=10,
            attack_speed=1,
            crit_chance=0,
            ability_power=0,
            class_type="",
            trait="",
            ability_description="",
            image_path="Fire Characters/phe0.png",
            current_mana=0,
            hasMana=True
        )


