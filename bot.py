import os
from dotenv import load_dotenv
import discord
from printer_connection import Bambu
from discord.ext import commands
from io import BytesIO

load_dotenv()
bambu = Bambu()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents) # prefix is deprecated - only slash commands are supported by discord

__CONNECTION_FAILED_RESPONSE = "Failed to connect to printer!"
def ensure_connection():
    if bambu.is_connected():
        return True
    if bambu.try_reconnect():
        return True
    return False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()  # tells discords the current bot commands
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    if ensure_connection():
        print("Connected to bambu-printer")
    else:
        print("Failed to connect to bambu-printer")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Ready to observe!"))

@bot.tree.command(name="status", description="Get the current printer status!")
async def status(interaction: discord.Interaction):
    if not ensure_connection():
        await interaction.response.send_message(__CONNECTION_FAILED_RESPONSE)
        return

    await interaction.response.defer()  # Defer the response to avoid timeout
    try:
        status = await bambu.get_status()
        await interaction.followup.send(f"The printer is currently{"" if status.online else " not" } printing!")
    except Exception as _:
        await interaction.followup.send(content="Sorry, i crashed :(")

@bot.tree.command(name="cam", description="Get a realtime screenshot of the current print!")
async def cam(interaction: discord.Interaction):
    if not ensure_connection():
        await interaction.response.send_message(__CONNECTION_FAILED_RESPONSE)
        return

    await interaction.response.defer()  # Defer the response to avoid timeout
    try:
        frame = bambu.get_camera_frame()
        image_bytes = BytesIO(frame)
        file = discord.File(image_bytes, filename="frame.png")
        await interaction.followup.send(file=file)
    except Exception as e:
        print(e)
        await interaction.followup.send(content="Sorry, i crashed :(")

bot.run(os.getenv('BOT_TOKEN'))

