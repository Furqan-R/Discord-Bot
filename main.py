import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks

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
    entries = get_entries()
    for entry in entries:
        seen_links.add(entry.link)
    check_feed.start()


@tasks.loop(minutes=10)
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