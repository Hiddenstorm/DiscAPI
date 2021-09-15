from .User import User
from .Channel import Channel

class Message:
    def __init__(self, data, HTMLClient):
        """
        This is the message class. It only stores variables at the time. 
        It can be replied by message.channel.send({content})
        """
        
        self.content = data["content"]
        self.id = data["id"]
        self.author = User(data["author"])
        self.channel = Channel(data["channel_id"], HTMLClient.get_channel(data["channel_id"]), HTMLClient)