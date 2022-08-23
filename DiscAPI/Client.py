import asyncio
import time
import threading

from .APISocket import Connection, Connection, opcode
from .Log import Log
from .Guild import Guild

class Client:
    def __init__(self, Log = False):
        """
        The Client class to instantiate a Discord Client.
        
        Parameters
        ----------

        Optional: Bool Log | Default = False
            Prints out extra information.
        """

        self.Log = Log
        self.Loop = asyncio.get_event_loop()
        self.handlers = {}
        self.uptime = 0
        self.guilds = []


    def run(self, TOKEN, SECRET):
        """
        This function starts the client.
        Return nothing.

        Parameters
        ----------

        Required: String Token
            The Client Token you get on https://discord.com/developers/applications/{AppID}/bot
        
        Required: String Secret
            The Client Secret you get on https://discord.com/developers/applications/{AppID}/oauth2
        """

        self.Token=TOKEN
        self.Secret=SECRET
        self.con = Connection(self)
        self.GatewayThread = threading.Thread(target=self.con.connect)
        self.GatewayThread.setName("Gateway")
        self.GatewayThread.start()
        self.UptimeThread = threading.Thread(target=self.counttime)
        self.UptimeThread.setName("Uptime")
        self.UptimeThread.start()
        self.Loop.run_forever()
        

    def event(self, method):
        """
        Putting
        @client.event("event")
        above a function will make it get called everytime that specific event happens.

        Events
        ------

        on_ready(): gets called when the client is ready to interact with discord.

        on_message(): gets called when a message gets posted into a discord guild and includes a message object in the function parameters.

        Example
        -------

        >>> @client.event("on_ready")
        >>> async def my_function():
        >>>     print("Bot is logged in.")
        """
        
        def registerhandler(handler):
            if method in self.handlers:
                self.handlers[method].append(handler)
            else:
                self.handlers[method] = [handler]
            return handler

        return registerhandler


    def counttime(self):
        """
        This is not meantto be used outside the package!
        Use client.get_uptime() instead!
        """
        
        while True:
            self.uptime += 1
            time.sleep(1)

    def call_event(self, type, *args, **kwargs):
        """
        This is not meantto be used outside the package!
        """

        Log.Debug(self, "Calling " + type + " event.")
        if type in self.handlers:
            for Method in self.handlers[type]:
                asyncio.run(Method(*args, **kwargs))


    async def set_status(self, state, activity=""):
        """
        This function is used to set the clients status and activity.
        Because of the way discord works, it might take a while to update status and activity.

        Parameters
        ----------

        Required: str State:
            "online" / "idle" / "dnd" / "invisible"
            something else wont work and results in an error.
        Currently required: str Activity:
            Example: "Counting sheep... zzz"
        """
        
        Log.Debug(self, "Setting status to {} and activity to {}...".format(state, activity))
        self.HTTPClient.Send_API(opcode.Status_update(state, activity))
        return


    async def get_guild(self, id):
        """
        This function returns a guild object.

        Parameters
        ----------
        Required: guild_id
            The guild id of the desired guild
        """
        
        guild = self.HTTPClient.get_guild(id)
        return guild


    async def get_channel(self, id):
        """
        This function returns a channel object.
        
        Parameters
        ----------
        Required: guild_id
            The channel id of the desired channel
        """

        channel = self.HTTPClient.get_channel(id)
        return channel


    async def get_guilds(self) -> list[Guild]:
        """
        This function will return a list with all guilds your client is in.
        """
        
        return self.guilds


    async def get_guild_count(self) -> int:
        """
        This function will return an integer that represents how many guilds the bot is currently in.
        """
        
        guilds = len(self.guilds)

        return guilds


    async def get_uptime(self) -> int:
        """
        This function will return an integer that represents how many seconds the bot has been online.
        """

        return self.uptime
