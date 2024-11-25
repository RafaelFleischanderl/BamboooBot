import os
from dotenv import load_dotenv
import discord
from printer_connection import Bambu
from discord.ext import commands

load_dotenv()
# bambu = Bambu()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents) # prefix is deprecated - only slash commands are supported by discord

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # tells discords the current bot commands
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user}!")

bot.run(os.getenv('BOT_TOKEN'))
# TODO: set bot private
