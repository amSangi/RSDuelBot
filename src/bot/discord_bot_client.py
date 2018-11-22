from discord import Client
from asyncio import CancelledError
from message_handler import MessageHandler


class DiscordBotClient(Client):
    """
    A subclass of the bot client

    Attributes:
        server_map (dict): A dictionary map from server id to the servers MessageHandler
        food (Food) : A food object
        weapons (dict): A dictionary map from weapon name to weapon
    """

    def __init__(self, food, weapons):
        super().__init__()
        self.server_map = {}
        self.food = food
        self.weapons = weapons

    async def on_ready(self):
        """Initialize the server map"""
        for server in self.servers:
            self.server_map[server.id] = MessageHandler(server, self.food, self.weapons)

    async def on_message(self, message):
        """Delegate message to respective MessageHandler"""
        if message.author == self.user:
            return

        server = message.server
        try:
            if server.id in self.server_map:
                res = await self.server_map[server.id].handle(message)
            else:
                handler = MessageHandler(server, self.food, self.weapons)
                self.server_map[server.id] = handler
                res = await handler.handle(message)
        except CancelledError:
            res = None

        if res is not None:
            await self.send_message(message.channel, res)
