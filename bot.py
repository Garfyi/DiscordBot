import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTI2NTMwNDc5Mzk4Mzc1MDE2NA.GJ8Z23.wSj1ACyLxdBwho0v2vnNleOjhU-WMB9-MBoWTM')