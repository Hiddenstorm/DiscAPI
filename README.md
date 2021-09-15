# DiscAPI
## _An easy to use Python Library to make unique discord bots._

## Installation

Only tested with python 3.9. 
Every other version might not work!

Install this library with pip.

```sh
pip install DiscAPI
```

## Example

.. code:: py
    
    import DiscAPI
    
    client = DiscAPI.Client()
    
    @client.event("on_ready")
    async def on_ready():
        await client.set_status("online", "Counting sheep.. zzz")
        
    @client.event("on_message")
    async def on_message(mess):
        if mess.content=="!hey":
            await mess.channel.send("Hi {}!".format(mess.author.name))
            
    client.run(Token, Secret)

## Developement

You want to submit bugs or new features? Add #HiddenStorm#4300 on discord.

## License

MIT