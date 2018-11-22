from game import Match
import prettytable as pt


class MessageHandler:
    """
    Handles  messages for an incoming message

    Args:
        server (bot.Server) : The bot server this instance corresponds to

    Attributes:
        matches (dict) : A map of channel id to a given Match
    """
    def __init__(self, server, food, weapons):
        self.weapons = weapons
        self.food = food
        self.matches = {}
        for channel in server.channels:
            self.matches[channel.id] = Match()

    async def handle(self, message):
        """
        Return a status update of the match after evaluating the message
        :param message: the user message
        :return: a status update for the match
        """
        channel_id = message.channel.id
        if channel_id in self.matches:
            match = self.matches[channel_id]
        else:
            match = Match()
            self.matches[channel_id] = match
        return await self._parse_command(message.author, message.content, match)

    async def _parse_command(self, user, content, match):
        """
        Return status update for the game

        :param content: The message contents
        :param match: The match in the current channel
        :return: the status of the game given a command
        """

        if not content.startswith("$"):
            return None

        command = content[1:]

        if command == "items":
            return await self._display_items()
        elif command == "dm":
            return await match.begin(user)
        elif not await match.is_player(user):
            return None
        elif command == "ff":
            return await match.cancel()
        elif command in self.weapons:
            return await match.register_item(user, self.weapons[content[1:]])
        elif command == "food":
            return await match.register_item(user, self.food)
        return None

    async def _display_items(self):
        # Weapon Table
        weapons_table = pt.PrettyTable()
        weapons_table.title = "Weapons"
        weapons_table.field_names = ["Name", "Damage", "Hits/Attack", "Spec", "Accuracy"]
        for name, weapon in self.weapons.items():
            weapons_table.add_row([name, weapon.base_hit, weapon.hits_per_attack, weapon.spec, weapon.accuracy * 100])

        # Food Table
        food_table = pt.PrettyTable()
        food_table.title = "Food"
        food_table.field_names = ["Name", "Heal Amount"]
        food_table.add_row(["food", self.food.heal_amount])
        return "`" + str(weapons_table) + "\n" + str(food_table) + "`"


