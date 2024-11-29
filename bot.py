import os
from dotenv import load_dotenv
import discord
from printer_connection import Bambu
from discord.ext import commands

load_dotenv()
bambu = Bambu()

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
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Ready to serve!"))

@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.defer()  # Defer the response to avoid timeout
    try:
        status = await bambu.get_status()
        await interaction.followup.send(f"Hello, the printer is currently{"" if status.online else " not" } printing!")
    except Exception as _:
        await interaction.followup.send(content="Sorry, i crashed :(")

bot.run(os.getenv('BOT_TOKEN'))

