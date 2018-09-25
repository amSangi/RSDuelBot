import discord
from asyncio import CancelledError
from message_handler import MessageHandler


class BotClient(discord.Client):
    """A subclass of the discord client

    Attributes:
        server_map (dict): A dictionary map from server id to the servers MessageHandler
        weapons (dict): A dictionary map from weapon name to weapon
    """

    def __init__(self, food_heal, weapons):
        super().__init__()
        self.server_map = {}
        self.food_heal = food_heal
        self.weapons = weapons

    async def on_ready(self):
        """Initialize the server map"""
        for server in self.servers:
            self.server_map[server.id] = MessageHandler(server, self.food_heal, self.weapons)

    async def on_message(self, message):
        """Delegate message to respective MessageHandler"""
        if message.author == self.user:
            return

        server = message.server
        try:
            if server.id in self.server_map:
                res = await self.server_map[server.id].handle(message)
            else:
                handler = MessageHandler(server, self.food_heal, self.weapons)
                self.server_map[server.id] = handler
                res = await handler.handle(message)
        except CancelledError:
            res = None

        if res is not None:
            await self.send_message(message.channel, res)
