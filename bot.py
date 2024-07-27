# bot.py
import os
import os.path
from collections import OrderedDict

import random

# API for discord
import discord
from discord.ext import commands
from dotenv import load_dotenv

# API for google translate
import googletrans
from googletrans import Translator

# API for lyrics
from lyricsgenius import Genius


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')


BOT = commands.Bot(command_prefix='g.', intents=discord.Intents.all())
TRANSLATOR = Translator()
GENIUS = Genius(GENIUS_TOKEN)
GENIUS.response_format = 'plain'

BOT.duet_happening = False
BOT.duet_user = ''
BOT.duet_answer = ''

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

    if BOT.duet_happening and ctx.author == BOT.duet_user:
        BOT.duet_happening = False

        if ctx.content == BOT.duet_answer:
            await ctx.channel.send(f'Congrats! You got the right lyric!')
        else:
            await ctx.channel.send(f"That's not the right lyric! The lyric was {BOT.duet_answer}")
        return

    # Calls the shame comamnd
    if "g.shame" == ctx.content:
        await shame_chat(ctx)
        return


#
#  SHAME SECTION
#


# Shames user function when used as chat message

async def shame_chat(ctx):

    # checks if the message is a reply, if so get the original from the reply message's id
    # otherwise exception
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


@BOT.tree.context_menu(name="shame")
async def shame(interaction:discord.Interaction, message:discord.Message):

    shamed = f'{message.author} was shamed after saying: {message.content}'
    
    f = open(f'Shame_data/data.txt', "a")
    f.write(f'{shamed} {message.jump_url} \n')
    f.close()

    await interaction.response.send_message(shamed)


# TODO function to show most recent shames


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
# ALL MUSIC RELATED SECTION
#


# Search for a song and send lyrics in chat if found 
@BOT.tree.command(name="lyrics")
async def translate(interaction:discord.Interaction, song_name:str, artist_name:str):

    # if lyricsbeingsent :
    #   return

    song = GENIUS.search_song(song_name, artist_name)
    lyrics = song.lyrics

    # TODO bot can only send 2000 characters fix so it sends entire lyrics
    # IDEA: make a job that executes every second, have global bool that is true if lyrics are being sent
    # when lyrics are all sent reset bool to false

    await interaction.response.send_message(f'{lyrics[0:1999]}')


# Search for a song and send all but last lyric, user has to guess it to win 
@BOT.tree.command(name="duet")
async def duet(interaction:discord.Interaction, song_name:str, artist_name:str):

    # Code does allow for two duets to happen at the same time
    if BOT.duet_happening == True:
        await interaction.response.send_message(f'WAIT YOUR TURN')
        return

    song = GENIUS.search_song(song_name, artist_name)
    # Create list of all the lines in the lyrics
    lyrics = song.lyrics.splitlines()

    # Get a random line from the lyrics
    index = random.randint(1, len(lyrics) - 1)
    line = lyrics[index]
    
    # Get all the words in the line
    words = line.split()

    # Assign the last word as the answer and hide it
    answer = words[len(words)-1]
    line = line.replace(answer, f' _______')

    await interaction.response.send_message(f'{line}')

    BOT.duet_happening = True
    BOT.duet_user = interaction.user
    BOT.duet_answer = answer


#
# GOOD BOY POINTS SECTION
#


# Adds gbp to a user if they have a profile
@BOT.tree.command(name="givegbp",description="give good boy points to member min:-3 max:3")
async def givegbp(interaction:discord.Interaction, member: discord.Member, amount : int):

    # Check if user is trying to give himself Good Boy Points
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

    # If no file is present with for user make one and store 0
    if os.path.isfile(f'{interaction.user.id}.txt') is False:
        f = open(f'GBP_data/{interaction.user.id}.txt', "w+")
        f.write(f'0')
        f.close()
    else:
        await interaction.response.send_message(f'{interaction.user} already has a GPB profile')
        return
        
    await interaction.response.send_message(f'Good Boy Point profile successfully created for {interaction.user}')


# Displays everybody's amount of Good Boy Points as a leaderboard
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
BOT.run(DISCORD_TOKEN)