# Import necessary libraries
import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_URL = "http://localhost:8000/chat"
FEEDBACK_URL = "http://localhost:8000/feedback"

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)


# -----------------------------
#  !ask command
# -----------------------------
@bot.command(name="ask")
async def ask(ctx, *, query: str):
    await ctx.trigger_typing()

    try:
        # Send query to FastAPI backend
        response = requests.post(BACKEND_URL, json={"query": query})
        data = response.json()
        answer = data.get("answer", "No response from backend.")

        # Send answer to Discord
        msg = await ctx.send(answer)

        # Add feedback reactions
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    except Exception as e:
        await ctx.send(f"Error contacting backend: {e}")


# -----------------------------
#  Reaction listener
# -----------------------------
@bot.event
async def on_reaction_add(reaction, user):
    # Ignore bot reactions
    if user.bot:
        return

    message = reaction.message

    # Only track reactions on bot messages
    if message.author != bot.user:
        return

    # Only track 👍 or 👎
    if reaction.emoji not in ["👍", "👎"]:
        return

    feedback_type = "upvote" if reaction.emoji == "👍" else "downvote"

    # Send feedback to backend
    try:
        requests.post(
            FEEDBACK_URL,
            json={
                "message_id": message.id,
                "user_id": user.id,
                "feedback": feedback_type,
                "content": message.content,
            },
        )
    except Exception as e:
        print("Error sending feedback:", e)


# -----------------------------
#  Bot startup
# -----------------------------
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

bot.run(DISCORD_TOKEN)