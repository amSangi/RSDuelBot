from abc import ABC, abstractmethod


class Item(ABC):

    @abstractmethod
    async def evaluate(self, player, enemy):
        pass


class Food(Item):

    def __init__(self, heal_amount):
        self.heal_amount = heal_amount

    async def evaluate(self, player, enemy):
        return self.heal_amount
