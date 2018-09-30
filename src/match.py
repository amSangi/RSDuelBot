import time
from player import Player
from item import Food
from weapon import Weapon


class Move:

    def __init__(self, player, enemy, item):
        self.player = player
        self.enemy = enemy
        self.item = item

    async def evaluate(self):
        value = await self.item.evaluate(self.player, self.enemy)

        # Food use
        if isinstance(self.item, Food):
            value = min(value, 100 - self.player.hp)
            self.player.hp += value
            return self.player.name + " heals for " + str(value)

        # Weapon use
        total_dmg = 0
        for val in value:
            total_dmg += val
        self.player.spec_available -= self.item.spec
        self.enemy.hp -= total_dmg

        return self.player.name + " did " + ", ".join(map(str, value)) + " damage"


class Match:
    """
    A match between two players

    Class Attributes:
        max_time_interval_ms (int) : Max length in seconds for a match
            - New matches can be started using .dm command

    Attributes:
        player1 (Player) : The first player in the match
        player2 (Player) : The second player in the match
        time_stamp (int) : The current
    """
    max_time_interval_ms = 5 * 60

    def __init__(self):
        self.player1 = Player()
        self.player2 = Player()
        self.moves = {}
        self.time_stamp = 1

    async def is_player(self, user):
        """
        :param user: a discord user
        :return: True if the discord user is a current player
        """
        return self.player1.id == user.id or self.player2.id == user.id

    async def begin(self, user):
        """
        :param user: the discord user initiating or accepting the match
        :return: a response message
        """
        if self.player1.id == -1:
            await self.player1.set_user(user)
            self.time_stamp = int(time.time())
            return user.name + " is looking for a challenge!"
        elif self.player2.id == -1 and self.player1.id != user.id:
            await self.player2.set_user(user)
            return user.name + " has accepted the challenge!"
        else:
            if (int(time.time()) - self.time_stamp) >= Match.max_time_interval_ms:
                await self._reset()
                msg = "Time limit reached!\r\n"
                res = await self.begin(user)
                return msg + res
            return "There is a match in progress!"

    async def cancel(self):
        """
        Cancel the current match and reset values

        :return: a status message
        """
        await self._reset()
        return "The match has been cancelled!"

    async def register_item(self, user, item):
        """
        Register an item use by a user

        :param user: the user initiating the attack
        :param item: the item used by the user
        :return: a status message
        """
        if user.id in self.moves:
            return "You have already registered your move!"

        player, enemy = await self._get_player_and_enemy(user)

        if isinstance(item, Weapon) and player.spec_available < item.spec:
            return "You do not have enough spec"

        self.moves[user.id] = Move(player, enemy, item)

        if len(self.moves) == 2:
            msg = await self._evaluate_moves()
            self.moves.clear()
            return msg

        return player.name + " has registered their move!"

    async def _evaluate_moves(self):
        """
        Evaluate both player moves and return a status update

        :return: a status message
        """
        message = ""
        for _, move in self.moves.items():
            move_msg = await move.evaluate()
            message += (move_msg + "\r\n")

        if self.player1.hp <= 0 and self.player2.hp <= 0:
            message += "Draw!"
            await self._reset()
            return message
        elif self.player1.hp <= 0:
            message += self.player2.name + " has won!"
            await self._reset()
            return message
        elif self.player2.hp <= 0:
            message += self.player1.name + " has won!"
            await self._reset()
            return message

        message += "\r\n"
        message += await self.player1.status()
        message += "\r\n\r\n"
        message += await self.player2.status()
        return message

    async def _reset(self):
        await self.player1.reset()
        await self.player2.reset()
        self.moves.clear()

    async def _get_player_and_enemy(self, user):
        if user.id == self.player1.id:
            return self.player1, self.player2
        return self.player2, self.player1
