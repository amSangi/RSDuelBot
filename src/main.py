from discord.discord_bot_client import DiscordBotClient
from config_loader import ConfigLoader
from game.weapon import SimpleWeapon, DHAxe
from game.item import Food

if __name__ == "__main__":
    loader = ConfigLoader()
    loader.load()
    items = {}
    for name, obj in loader.data['weapons'].items():
        if name == "dhaxe":
            items[name] = DHAxe(obj)
        else:
            items[name] = SimpleWeapon(obj)
    client = DiscordBotClient(Food(loader.data['food']['heal']), items)
    client.run(loader.data['token'])
