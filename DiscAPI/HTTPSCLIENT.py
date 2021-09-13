import threading
import websocket
import json
import asyncio
import time

from .Log import Log
from .Guild import Guild

class HTTPClient:
    def __init__(self, client):
        self.client = client
        self.websocket = websocket.WebSocket()
        self.BaseUrl = "https://discord.com/api/v9/"
        self.headers = {"Authorization" : "Bot {}".format(self.client.Secret)}
        self.gatewayurl = "wss://gateway.discord.gg/?v=9&encoding=json"

    def connect(self):
        #connecting
        self.websocket.connect(self.gatewayurl)
        Log.Debug(self.client, "Connected to Websocket")
        
        self.Interval = json.loads(self.websocket.recv())["d"]["heartbeat_interval"]
        Log.Debug(self.client, "Received GateWay Info.")
        Log.Debug(self.client, "Heartbeat Interval set to " + str(self.Interval) + "ms")

        #send identifying OP
        self.websocket.send(op.identify(self.client.Token))

        #receiving info
        self.StartInfo = self.websocket.recv()
        Log.Debug(self.client, "Successfully identified GateWay and received Start info.")
        Log.Debug(self.client, "Collecting guild info in the process...")
        api = threading.Thread(target=self.Receive_API)
        api.start()
        self.HeartBeatThread = threading.Thread(target=self.HeartBeat)
        self.HeartBeatThread.start()
        return

    def Receive_API(self):
        raw = self.websocket.recv()
        
        #Start new Receiving threads
        api = threading.Thread(target=self.Receive_API)
        api.start()
        
        signal = json.loads(raw)
        op = signal["op"]

        Log.Debug(self.client, "Received an OPCode " + str(op))

        #Dispatch
        if op == 0:
            name = signal["t"]
            data = signal["d"]

            if name == "GUILD_CREATE":
                self.client.guilds.append(Guild(data))

            if name == "MESSAGE_CREATE":
                asyncio.run(self.client.call_event("on_message"))

        #Heartbeat
        elif op == 1:
            pass

        #Identify
        elif op == 2:
            pass

        #Presence Update
        elif op == 3:
            pass
        
        #Voice State Update
        elif op == 4:
            pass

        #Resume
        elif op == 6:
            pass

        #Reconnect
        elif op == 7:
            pass

        #Request Guild Members
        elif op == 8:
            pass

        #Invalid Session
        elif op == 9:
            pass

        #Hello
        elif op == 10:
            pass

        elif signal["op"] == 11:
            Log.Debug(self.client, "Received HeartBeat")

    def HeartBeat(self):
        Log.Debug(self.client, "Sending initial HeartBeat")
        self.websocket.send(op.heartbeat())

        #Looping Heartbeat
        while True:
            time.sleep(self.Interval/1000-1)
            Log.Debug(self.client, "Sending HeartBeat")
            self.websocket.send(op.heartbeat())

class op:
    def identify(Token):
        dict = '''
        {
            "op": 2,
            "d": {
                "token" : "''' + Token + '''",
                "intents":513,
                "properties":{
                    "$os":"linux",
                    "$browser":"my_library",
                    "$device":"my_library"
                    }
                }
            }
        '''
        return str(dict)
    
    def heartbeat():
        dict = '''
        {
            "op": 1,
            "d": null
        }
        '''
        return str(dict)