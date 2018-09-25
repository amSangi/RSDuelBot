from match import Match


class MessageHandler:
    """A class that handles messages for an incoming message

    Args:
        server (discord.Server) : The discord server this instance corresponds to

    Attributes:
        matches (dict) : A map of channel id to a given Match
    """
    def __init__(self, server, food_heal, weapons):
        self.weapons = weapons
        self.food_heal = food_heal
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
        return self._parse_command(message.user, message.content, match)

    def _parse_command(self, user, content, match):
        """
        Return status update for the match

        :param content: The message contents
        :param match: The match in the current channel
        :return: the status of the match
        """
        if not content.startswith("."):
            return None

        if content == ".dm":
            return match.begin(user)
        elif content == ".ff" and match.is_player(user):
            return match.cancel()
        elif content[1:] in self.weapons:
            return match.register_move(user, self.weapons[content[1:]])
        elif content == ".food":
            return match.register_heal(user, self.food_heal)
        return None
