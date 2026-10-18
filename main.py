import os
import discord
from dotenv import load_dotenv

import feed
from feed import get_entries

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

entries = get_entries()
first = entries[0]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel_id = int(os.getenv("CHANNEL_ID"))
    channel = client.get_channel(channel_id)
    await channel.send(f"{first.title}\n{first.link}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!Get":
        await message.channel.send(feed)

client.run(TOKEN)