class User:
    def __init__(self, data):
        self.name = data["username"]
        self.id = data["id"]
        self.discriminator = data["discriminator"]