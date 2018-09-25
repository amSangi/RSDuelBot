from abc import ABC, abstractmethod
import random


class Weapon(ABC):
    """ Abstract weapon class that computes damage given a player and enemy

    Args:
        obj (dict): Weapon obj loaded from config.json

    Attributes:
        base_hit (int): The base hit damage of the weapon
        hits_per_attack (int): The number of attacks per turn
        spec (int): The amount of spec the weapon uses (0 <= spec <= 100)
        accuracy: The weapon accuracy
    """

    def __init__(self, obj):
        self.base_hit = obj['base_hit']
        self.hits_per_attack = obj['hits_per_attack']
        self.spec = obj['spec']
        self.accuracy = obj['accuracy']

    @abstractmethod
    def evaluate(self, player, enemy):
        """
        Compute the damage to apply on enemy
        :Assume: The player has enough spec to use this weapon
        :param player: The player initiating the attack
        :param enemy: The enemy receiving the attack
        :return: int tuple: each tuple represents damage for that hit
        """
        pass


class SimpleWeapon(Weapon):
    """A weapon that computes simple damage per hit"""
    def __init__(self, obj):
        super().__init__(obj)

    async def evaluate(self, player, enemy):
        damage_per_hit = []
        for _ in range(0, self.hits_per_attack):
            # Determine if player hit
            hit_chance = random.random()
            if hit_chance < self.accuracy:
                damage_per_hit.append(0)
                continue

            # Compute damage
            hit_damage = random.randint(1, self.base_hit)
            damage_per_hit.append(hit_damage)

        return tuple(damage_per_hit)


class DHAxe(Weapon):
    """A weapon that represents the DHAxe. It does more damage the less hp the attacking player has"""
    def __init__(self, obj):
        super().__init__(obj)

    async def evaluate(self, player, enemy):
        """ Max Damage = base_hit + (base_hit * (1/player_hp)) """

        hit_chance = random.random()
        if hit_chance < self.accuracy:
            return tuple([0])

        max_hit_damage = self.base_hit + int(self.base_hit * (1 / player.hp))
        return tuple(random.randint(1, max_hit_damage))



