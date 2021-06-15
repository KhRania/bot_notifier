# near the top of your file with the rest of your imports
from discord.ext import aiohttp
from io import BytesIO

# in an async function, such as an on_message handler or command
async with aiohttp.ClientSession() as session:
    # note that it is often preferable to create a single session to use multiple times later - see below for this.
    async with session.get("http://151.253.224.74:3008/axis-cgi/jpg/image.cgi?&compression=25&camera=quad") as resp:
        buffer = BytesIO(await resp.read())

await client.send_file(message.channel, fp=buffer, filename="something.png")


# using a predefined ClientSession on the Client instance
client.session = aiohttp.ClientSession(loop=client.loop)  # then use client.session.get similar to above


# using a predefined ClientSession within a cog
def __init__(self, bot, ...):
    ...
    self.session = aiohttp.ClientSession(loop=bot.loop)
    ...
    # then use self.session.get similar to above


# 3.4 syntax
resp = yield from session.get(url)

try:
    content = yield from resp.read()
finally:
    resp.close()
buffer = BytesIO(content)

yield from client.send_file(message.channel, fp=buffer, filename="something.png")