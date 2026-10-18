import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks



import feed
from feed import get_entries


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
seen_links = set()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    check_feed.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!Get":
        await message.channel.send(feed)


@tasks.loop(minutes=1)
async def check_feed():

    entries = get_entries()
    channel_id = int(os.getenv("CHANNEL_ID"))
    channel = client.get_channel(channel_id)
    for entry in entries:
        if entry.link not in seen_links:
            seen_links.add(entry.link)
            await channel.send(f"{entry.title}\n{entry.link}")
    print("Checking feed")


client.run(TOKEN)