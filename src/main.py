from bot_client import BotClient
from config_loader import ConfigLoader
from weapon import SimpleWeapon, DHAxe
from item import Food

if __name__ == "__main__":
    loader = ConfigLoader()
    loader.load()
    items = {}
    for name, obj in loader.data['weapons'].items():
        if name == "dhaxe":
            items[name] = DHAxe(obj)
        else:
            items[name] = SimpleWeapon(obj)
    client = BotClient(Food(loader.data['food']['heal']), items)
    client.run(loader.data['token'])
