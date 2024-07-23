# bot.py
import os
import os.path
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

@bot.tree.command(name="addgbp",description="add good boy points to member")
async def addgbp(interaction:discord.Interaction, member: discord.Member, amount : int):
    if amount > 3 or amount < -3:
        await interaction.response.send_message(f'The amount of Good Boy Points added has to be between -3 and 3')
        return

    if os.path.isfile(f'{str(member.id)}.txt'):
        f = open(f'{str(member.id)}.txt', "r")
        gbp = int(f.read())
        f.close()
        f = open(f'{str(member.id)}.txt', "w+")
        f.write(str(gbp + amount))
    else:
        await interaction.response.send_message(f'{member} does not have a GPB profile')
        return
        
    await interaction.response.send_message(f'{member} now has {f.read()} Good Boy Points!')
    f.close()

@bot.tree.command(name="showgbp",description="show member's good boy points")
async def showgbp(interaction:discord.Interaction, member: discord.Member):
    if os.path.isfile(f'{str(member.id)}.txt'):
        f = open(f'{str(member.id)}.txt', "r")
        gbp = int(f.read())
    else:
        await interaction.response.send_message(f'{member} does not have a GPB profile')
        return
        
    await interaction.response.send_message(f'{member} currently has {gbp} Good Boy Points!')
    f.close()

# If users are added dynamically it's going to take up a lot of space
""""
@bot.tree.command(name="addgbp",description="add good boy points to member")
async def addgbp(interaction:discord.Interaction, member: discord.Member, amount : int):
    if os.path.isfile(f'{str(member.id)}.txt'):
        f = open(f'{str(member.id)}.txt', "r")
        gbp = int(f.read())
        f.close()
        f = open(f'{str(member.id)}.txt', "w+")
        f.write(str(gbp + amount))
    else:
        f = open(f'{str(member.id)}.txt', "w+")
        f.write(str(0 + amount))
        
    await interaction.response.send_message(f'{member} now has {f.read()} Good Boy Points!')
    f.close()
"""
bot.run(TOKEN)