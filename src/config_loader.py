import json


class ConfigLoader:
    """Load and store configuration details"""

    def __init__(self):
        self.data = None

    def load(self):
        """Load and store configuration details"""
        with open('../resources/config.json') as configfile:
            self.data = json.load(configfile)
