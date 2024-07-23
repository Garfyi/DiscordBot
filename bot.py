# bot.py
import os
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv
#import random

description = "garfy's little bot guy thing"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'logged in as {bot.user} (ID: {bot.user.id})')


@bot.tree.command(name="addgbp",description="add two numbers")
async def pp(interaction:discord.Interaction, member: discord.Member, amount : int):
    f = open(str(member.id) + '.txt', "r")
    
            
    await interaction.response.send_message(f'{member}')

bot.run(TOKEN)