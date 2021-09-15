class Channel:
    def __init__(self, ID, data, HTMLClient):
        self.Id = ID
        self.name = data["name"]
        self.guild_id = data["guild_id"]
        self.HTMLClient = HTMLClient

    async def send(self, content):
        """
        This method sends a message in this Channel.
        
        It requires one string parameter which represents the text sent as a discord message.
        """

        self.HTMLClient.send_message(self.Id, content)
        return

    async def get_guild(self):
        """
        This method returns the guild object of the guild this channel is in.

        It has no parameters.
        """

        guild = self.HTMLClient.get_guild(self.guild_id)
        return guild