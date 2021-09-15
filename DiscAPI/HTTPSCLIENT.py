import threading
import websocket
import json
import asyncio
import time
import requests

from .Log import Log
from .Guild import Guild
from .Message import Message

class HTTPClient:
    def __init__(self, client):
        #done
        self.client = client
        self.websocket = websocket.WebSocket()
        self.BaseUrl = "https://discord.com/api/v9/"
        self.headers = {"Authorization" : "Bot {}".format(self.client.Secret)}
        self.gatewayurl = "wss://gateway.discord.gg/?v=9&encoding=json"

    def connect(self):
        #done
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

    def HeartBeat(self):
        Log.Debug(self.client, "Sending initial HeartBeat")
        self.websocket.send(op.heartbeat())

        #Looping Heartbeat
        while True:
            time.sleep(self.Interval/1000-1)
            Log.Debug(self.client, "Sending HeartBeat")
            self.websocket.send(op.heartbeat())

    def Receive_API(self):
        #not done
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
                message = Message(data, self)
                asyncio.run(self.client.call_event("on_message", message))

        #Reconnect
        elif op == 7:
            pass

        #Invalid Session
        elif op == 9:
            pass

        elif signal["op"] == 11:
            Log.Debug(self.client, "Received HeartBeat")

    def Send_API(self, dict):
        #done
        self.websocket.send(dict)
        return

    def send_message(self, ChannelID, strcontent):
        #done
        Url = self.BaseUrl + "channels/" + str(ChannelID) + "/messages"
        payload = json.dumps({"Content-Type": "application/json", "content":strcontent})
        headers = { "Authorization":"Bot {}".format(self.client.Token), "Content-Type":"application/json", }
        requests.post(Url, headers=headers, data=payload)
        return

    def get_guild(self, id):
        #Done
        Url = self.BaseUrl + "guilds/" + str(id)
        header = {"Authorization": "Bot {}".format(self.client.Token)}
        raw = requests.get(Url, headers=header)
        info = raw.json()
        return info

    def get_channel(self, id):
        #Done
        Url = self.BaseUrl + "channels/" + str(id)
        header = {"Authorization": "Bot {}".format(self.client.Token)}
        raw = requests.get(Url, headers=header)
        info = raw.json()
        return info

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

    def Status_update(status, activity):
        dict = '''
        {
            "op": 3,
            "d": {
                "since": null,
                "status": "'''+status+'''",
                "afk": false,
                "activities": [{
                    "name": "'''+activity+'''",
                    "type": 0
                }]
            }
        }
        '''
        return str(dict)