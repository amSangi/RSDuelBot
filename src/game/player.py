
class Player:

    def __init__(self):
        self.hp = 100
        self.name = ""
        self.id = -1
        self.spec_available = 100

    async def reset(self,):
        self.hp = 100
        self.name = ""
        self.id = -1
        self.spec_available = 100

    async def set_user(self, user):
        self.name = user.name
        self.id = user.id

    async def status(self):
        status = self.name + " : \r\n"

        status += "HP: " + str(self.hp) + "   " + ("░" * (int(self.hp/5)))
        status += "\r\n"

        status += "SPEC: " + str(self.spec_available)
        status += "\r\n"

        return status

