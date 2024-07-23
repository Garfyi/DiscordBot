# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
#import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$allo'):
        await message.channel.send('oui?')

client.run(TOKEN)