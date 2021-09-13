from .Channel import Channel

class Guild:
    def __init__(self, data):
        self.name = data["name"]
        
        self.channels = []
        for channel in data["channels"]:
            self.channels.append(Channel(channel))