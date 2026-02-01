import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_URL = "http://localhost:8000/chat"

# Enable message content
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Bot ready event
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

# Handle messages
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Only respond to "!ask"
    if not message.content.startswith("!ask "):
        return

    query = message.content[len("!ask "):].strip()

    await message.channel.send("Thinking...")

    # Send query to FastAPI backend
    resp = requests.post(BACKEND_URL, json={"message": query})
    answer = resp.json().get("answer", "Error.")

    await message.channel.send(answer)

# Run bot
if __name__ == "__main__":
    client.run(DISCORD_TOKEN)