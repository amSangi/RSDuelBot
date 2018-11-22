from bot import DiscordBotClient
from config_loader import ConfigLoader
from game import SimpleWeapon, DHAxe
from game import Food

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
