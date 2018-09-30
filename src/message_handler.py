from match import Match


class MessageHandler:
    """
    Handles  messages for an incoming message

    Args:
        server (discord.Server) : The discord server this instance corresponds to

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

        if not content.startswith("."):
            return None

        if content == ".items":
            return None
        elif content == ".dm":
            return await match.begin(user)
        elif not await match.is_player(user):
            return None
        elif content == ".ff":
            return await match.cancel()
        elif content[1:] in self.weapons:
            return await match.register_item(user, self.weapons[content[1:]])
        elif content == ".food":
            return await match.register_item(user, self.food)
        return None
