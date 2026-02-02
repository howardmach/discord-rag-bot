import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Set up Discord bot configuration
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
    async with ctx.channel.typing():
        # Send request to backend using the correct field name
        response = requests.post(BACKEND_URL, json={"message": query})

        # Debug print to see raw backend output
        print("Backend raw response:", response.text)

        # Parse JSON safely
        try:
            data = response.json()
            answer = data.get("answer", "No response from backend.")
        except Exception as e:
            answer = f"Error parsing backend response: {e}"

    # Send answer to Discord
    msg = await ctx.send(answer)

# -----------------------------
#  Reaction listener
# -----------------------------
@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message

    # Ignore ANY reaction added by the bot
    if user.id == bot.user.id:
        return

    # Ignore reactions that the bot added to its own message
    # (Discord sometimes fires these as if a user added them)
    if message.author.id == bot.user.id and reaction.me:
        return

    # Only track reactions on bot messages
    if message.author.id != bot.user.id:
        return

    # Only track 👍 or 👎
    if reaction.emoji not in ["👍", "👎"]:
        return

    # Determine feedback type
    feedback_type = "upvote" if reaction.emoji == "👍" else "downvote"

    # Remove the opposite reaction from this user
    opposite = "👎" if reaction.emoji == "👍" else "👍"

    for r in message.reactions:
        if r.emoji == opposite:
            try:
                await r.remove(user)
            except Exception as e:
                print("Error removing opposite reaction:", e)

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

# Run the bot
bot.run(DISCORD_TOKEN)