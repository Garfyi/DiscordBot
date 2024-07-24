# bot.py
import os
import os.path
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

description = "garfy's little bot guy thing"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='g.', description=description, intents=intents)

# When bot is online
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'logged in as {bot.user} (ID: {bot.user.id})')


# Anytime a message is sent in any channel
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "g.kill" in message.content:
        await bot.close()

    if message.author == 781574003264716800:
        randInt = random.randint(0,15)
        if randInt == 15:
            await message.channel.send(f'stfu gio')

# Adds gbp to a user if they have a profile
@bot.tree.command(name="addgbp",description="add good boy points to member min:-3 max:3")
async def addgbp(interaction:discord.Interaction, member: discord.Member, amount : int):

    if interaction.user == member:
        await interaction.response.send_message(f'kys')
        return

    if amount > 3 or amount < -3:
        await interaction.response.send_message(f'The amount of Good Boy Points added has to be between -3 and 3')
        return

    if os.path.isfile(f'GPB_data/{member.id}.txt'):
        f = open(f'GPB_data/{member.id}.txt', "r")
        gbp = int(f.read())
        f.close()
        f = open(f'GPB_data/{member.id}.txt', "w+")
        f.write(f'{gbp + amount}')
        f.close()
    else:
        await interaction.response.send_message(f'{member} does not have a GPB profile')
        return
        
    f = open(f'GPB_data/{member.id}.txt', "r")
    if amount < 0:
        await interaction.response.send_message(f'{interaction.user} has taken away {amount * -1} Good Boy Points from {member}. They now have {f.read()} Good Boy Points!')
        f.close()
        return
    
    await interaction.response.send_message(f'{interaction.user} has given {amount} Good Boy Points to {member}. They now have {f.read()} Good Boy Points!')
    f.close()

# Shows how many good boy points a user has
@bot.tree.command(name="showgbp",description="show member's good boy points")
async def showgbp(interaction:discord.Interaction, member: discord.Member):
    if os.path.isfile(f'GPB_data/{member.id}.txt'):
        f = open(f'GPB_data/{member.id}.txt', "r")
        gbp = int(f.read())
        f.close()
    else:
        await interaction.response.send_message(f'{member} does not have a GPB profile')
        return
    
    await interaction.response.send_message(f'{member} currently has {gbp} Good Boy Points')
    

# Adds member text file to store profile info
@bot.tree.command(name="creategbp",description="creates gbp profile for command caller")
async def creategbp(interaction:discord.Interaction):
    if os.path.isfile(f'{interaction.user.id}.txt') is False:
        f = open(f'GPB_data/{interaction.user.id}.txt', "w+")
        f.write(f'0')
        f.close()
    else:
        await interaction.response.send_message(f'{interaction.user} already has a GPB profile')
        return
        
    await interaction.response.send_message(f'Good Boy Point profile successfully created for {interaction.user}')

# If users are added dynamically it's going to take up a lot of space
""""
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
        f = open(f'{str(member.id)}.txt', "w+")
        f.write(str(0 + amount))
        
    await interaction.response.send_message(f'{member} now has {f.read()} Good Boy Points!')
    f.close()
"""
bot.run(TOKEN)