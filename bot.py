import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variable
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Replace with your server and channel IDs
GUILD_ID = 913372558693396511
VOICE_CHANNEL_ID = 994447006741299280

# List of song URLs or file paths
SONG_LIST = [
    'https://www.youtube.com/watch?v=omfz62qu_Bc',
    'https://www.youtube.com/watch?v=41qC3w3UUkU',
    # Add more songs as needed
]

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def play_songs(voice_client):
    for song in SONG_LIST:
        voice_client.play(discord.FFmpegPCMAudio(song))
        while voice_client.is_playing():
            await asyncio.sleep(1)
    await voice_client.disconnect()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if guild:
        voice_channel = discord.utils.get(guild.voice_channels, id=VOICE_CHANNEL_ID)
        if voice_channel:
            voice_client = await voice_channel.connect()
            await play_songs(voice_client)
        else:
            print('Voice channel not found.')
    else:
        print('Guild not found.')

bot.run(TOKEN)
