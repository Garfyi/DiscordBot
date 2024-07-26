# bot.py
import os
import os.path
from collections import OrderedDict

import discord
from discord.ext import commands
from dotenv import load_dotenv

import googletrans
from googletrans import Translator

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

BOT = commands.Bot(command_prefix='g.', intents=discord.Intents.all())
TRANSLATOR = Translator()

# When bot is online
@BOT.event
async def on_ready():
    await BOT.tree.sync()
    print(f'logged in as {BOT.user} (ID: {BOT.user.id})')


# Anytime a message is sent in any channel
@BOT.event
async def on_message(ctx):
    if ctx.author == BOT.user:
        return
    
    if "g.kill" == ctx.content:
        print(f'Some dude killed the bot')
        await BOT.close()

    if "g.shame" == ctx.content:
        await shame_chat(ctx)
        return


#
#  SHAME SECTION
#

# Shames user function when used as chat message

async def shame_chat(ctx):

    try:
        message = await ctx.channel.fetch_message(ctx.reference.message_id)
    except:
        await ctx.channel.send('You must reply to the message you want to shame')
        return

    shamed = f'{message.author} was shamed after saying: {message.content}'
    
    f = open(f'Shame_data/data.txt', "a")
    f.write(f'{shamed} {message.jump_url} \n')
    f.close()

    await ctx.channel.send(shamed)
    return


@BOT.tree.context_menu(name="shame")
async def shame(interaction:discord.Interaction, message:discord.Message):

    shamed = f'{message.author} was shamed after saying: {message.content}'
    
    f = open(f'Shame_data/data.txt', "a")
    f.write(f'{shamed} {message.jump_url} \n')
    f.close()

    await interaction.response.send_message(shamed)


#
# TRANSLATION SECTION
#

# Translate the message to english from the context menu
@BOT.tree.context_menu(name="translate")
async def translate(interaction:discord.Interaction, message:discord.Message):

    src = TRANSLATOR.detect(message.content)
    text = TRANSLATOR.translate(message.content, dest='en').text

    await interaction.response.send_message(f'{message.author} said : "{text}" in {googletrans.LANGUAGES[f'{src.lang}']}')


#
# GOOD BOY POINTS SECTION
#

# Adds gbp to a user if they have a profile
@BOT.tree.command(name="givegbp",description="give good boy points to member min:-3 max:3")
async def givegbp(interaction:discord.Interaction, member: discord.Member, amount : int):

    if interaction.user == member:
        await interaction.response.send_message(f'kys')
        return

    if amount > 3 or amount < -3:
        await interaction.response.send_message(f'The amount of Good Boy Points given/taken has to be between -3 and 3')
        return

    if os.path.isfile(f'GBP_data/{member.id}.txt'):
        f = open(f'GBP_data/{member.id}.txt', "r")
        gbp = int(f.read())
        f.close()
        f = open(f'GBP_data/{member.id}.txt', "w+")
        f.write(f'{gbp + amount}')
        f.close()
    else:
        await interaction.response.send_message(f'{member} does not have a GPB profile')
        return
        
    f = open(f'GBP_data/{member.id}.txt', "r")
    if amount < 0:
        await interaction.response.send_message(f'{interaction.user} has taken away {amount * -1} Good Boy Points from {member}. They now have {f.read()} Good Boy Points!')
        f.close()
        return
    
    await interaction.response.send_message(f'{interaction.user} has given {amount} Good Boy Points to {member}. They now have {f.read()} Good Boy Points!')
    f.close()

# Shows how many good boy points a user has
@BOT.tree.command(name="showgbp",description="show member's good boy points")
async def showgbp(interaction:discord.Interaction, member: discord.Member):

    if os.path.isfile(f'GBP_data/{member.id}.txt'):
        f = open(f'GBP_data/{member.id}.txt', "r")
        gbp = int(f.read())
        f.close()
    else:
        await interaction.response.send_message(f'{member} does not have a GPB profile')
        return
    
    await interaction.response.send_message(f'{member} currently has {gbp} Good Boy Points')
    

# Adds member text file to store profile info
@BOT.tree.command(name="creategbp",description="creates gbp profile for command caller")
async def creategbp(interaction:discord.Interaction):

    if os.path.isfile(f'{interaction.user.id}.txt') is False:
        f = open(f'GBP_data/{interaction.user.id}.txt', "w+")
        f.write(f'0')
        f.close()
    else:
        await interaction.response.send_message(f'{interaction.user} already has a GPB profile')
        return
        
    await interaction.response.send_message(f'Good Boy Point profile successfully created for {interaction.user}')


# Displays everybody's numbre of Good Boy Points as a leaderboard
@BOT.tree.command(name="leaderboard",description="shows gbp leaderboard")
async def leaderboard(interaction:discord.Interaction):

    files = os.listdir('./GBP_data')
    dict = OrderedDict()
    board = 'Good Boy Point leaderboard\n'

    for file in files :
        amount = open(f'GBP_data/{file}', 'r')
        dict[BOT.get_user(int(file.removesuffix('.txt'))).name] = int(amount.read())
        amount.close()

    sortedDict  = OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))

    for user, gbp in sortedDict.items():
        board += str(f'{user} : {gbp} \n')

    await interaction.response.send_message(f'{board}')


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
BOT.run(TOKEN)