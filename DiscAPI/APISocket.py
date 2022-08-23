from ast import match_case
import threading
import websocket
import json
import asyncio
import time
import requests

from .Log import Log
from .Guild import Guild
from .Message import Message

class Connection:
    def __init__(self, client):
        """
        DiscAPI Websocket and request class
        Not meant to be used outside of this package
        handles url calls and the general websocket
        """

        self.client = client
        self.BaseUrl = "https://discord.com/api/v9/"
        self.headers = {"Authorization" : "Bot {}".format(self.client.Secret)}
        self.gatewayurl = "wss://gateway.discord.gg/?v=9&encoding=json"


    def connect(self):
        """
        Connects to the discord API via Websocket
        """

        websocket.enableTrace(False)
        self.websocket = websocket.WebSocketApp(
            url=self.gatewayurl,
            on_data=self.receive_payload,
            on_close=self.close_event
        )
        
        self.websocket.run_forever()


    def receive_payload(self, websocket, message, *args, **kwargs):
        """
        Matches opcode with proper function
        """

        signal = json.loads(message)
        op = signal["op"]
        name = signal["t"]
        data = signal["d"]

        # Only acknowledges receivable opcodes such as 0, 1, 7, 9, 10 and 11
        match op:

            # Dispatch
            case 0:

                match name:

                    case "READY":
                        self.client.call_event("on_ready")

                    case "MESSAGE_CREATE":
                        message = Message(data, self)
                        asyncio.run(self.client.call_event("on_message", message))
            
            # Heartbeat
            case 1:
                pass

            # Reconnect
            case 7:
                pass

            # Invalid
            case 9:
                pass

            # Initial hello payload
            case 10:
                pass

            # Heartbeat acknowledged
            case 11:
                pass

            case _:
                pass


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