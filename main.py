from discord.ext import commands
import os
import discord
from dotenv import load_dotenv
from responses import convert_video

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='?', intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN')

@bot.command()
async def c(ctx, url: str, format_choice: str):
    await convert_video(ctx, url, format_choice)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print('Bot is ready.')

bot.run(TOKEN)
