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
        self.BaseUrl = "https://discord.com/api/v9/"
        self.headers = {"Authorization" : "Bot {}".format(self.client.Secret)}
        self.gatewayurl = "wss://gateway.discord.gg/?v=9&encoding=json"

    def connect(self):
        Log.Debug(self.client, "Connecting client to discord gateway")
        websocket.enableTrace(False)
        self.websocket = websocket.WebSocketApp(
            url=self.gatewayurl,
            on_data=self.receive_payload,
            on_close=self.close_event
        )
        Log.Debug(self.client, "Identifying as client")
        self.websocket.run_forever()

    def receive_payload(self, websocket, message, *args, **kwargs):
        signal = json.loads(message)
        op = signal["op"]
        name = signal["t"]
        data = signal["d"]
        Log.Debug(self.client, "Received an OPCode " + str(op) + ":" + str(name))

        #Dispatch
        if op == 0:
            if name == 'READY':
                Log.Debug(self.client, "Marked as ready")
                self.HeartbeatThread = threading.Thread(target=self.HeartBeat)
                self.HeartbeatThread.setName("Heart")
                self.HeartbeatThread.start()
                self.client.call_event("on_ready")

            elif name == "GUILD_CREATE":
                Log.Debug(self.client, "Appending guild")
                self.client.guilds.append(Guild(data))

            elif name == "MESSAGE_CREATE":
                Log.Debug(self.client, "Received message")
                message = Message(data, self)
                asyncio.run(self.client.call_event("on_message", message))

        #Reconnect
        elif op == 7:
            pass

        #Invalid Session
        elif op == 9:
            pass

        elif op == 11:
            Log.Debug(self.client, "Received HeartBeat")

        elif op == 10:
            Log.Debug(self.client, "Recieved 'Hello' Payload")
            self.Interval = signal["d"]['heartbeat_interval']
            self.websocket.send(opcode.identify(self.client.Secret))

    def HeartBeat(self):
        Log.Debug(self.client, "Sending initial HeartBeat")
        self.websocket.send(opcode.heartbeat())

        while True:
            time.sleep(self.Interval/1000-1)
            Log.Debug(self.client, "Sending HeartBeat")
            self.websocket.send(opcode.heartbeat())

    def close_event(self, ws, encoded, decoded):
        Log.Debug(self.client, "Websocket closed")

#--------------------------------------------------------------------------------

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

class opcode:
    def identify(Token):
        b = {
            "op": 2,
            "d": {
                "token": str(Token),
                "intents": 513,
                "properties": {
                    "$os": "linux",
                    "$browser": "my_library",
                    "$device": "my_library"
                }
            }
        }
        return str(str(json.dumps(b)))
    
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