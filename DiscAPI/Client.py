import asyncio
import time
import threading

from .HTTPSCLIENT import HTTPClient
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
        self.HTTPClient = HTTPClient(self)
        self.HTTPClient.connect()
        self.UptimeThread = threading.Thread(target=self.counttime)
        self.UptimeThread.start()
        asyncio.run(self.call_event("on_ready"))
        self.Loop.run_forever()
        
    def event(self, method):
        """
        Putting
        @client.event("event")
        above a function will make it get called everytime that specific event happens.

        Events
        ------

        on_ready: gets called when the client is ready to interact with discord.

        on_message: gets called when a message gets posted into a discord guild.

        Example
        -------

        >>> @client.event("on_ready")
        >>> async def my_function():
        >>>     print("Bot is logged in.")
        """
        
        Log.Debug(self, "Registered " + method + " as an event.")
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

    async def call_event(self, type, *args, **kwargs):
        """
        This is not meantto be used outside the package!
        """

        Log.Debug(self, "Calling " + type + " event.")
        if type in self.handlers:
            for Method in self.handlers[type]:
                await Method(*args, **kwargs)

    async def get_guilds(self) -> list[Guild]:
        #: :type: list of Guild
        """
        This function will return a list with all guilds your client is in.
        """
        
        return self.guilds

    async def get_guild_count(self) -> int:
        """
        This function will return an integer that represents how many guilds the bot is currently in.
        """
        
        guilds = 0
        for guild in self.guilds:
            guilds+=1

        return guilds

    async def get_uptime(self) -> int:
        """
        This function will return an integer that represents how many seconds the bot has been online.
        """

        return self.uptime