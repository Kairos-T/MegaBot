import os
import random
import discord
from discord.ext import commands

from decouple import Config

config = Config('megabot.env')
api_token = config.get('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True
BOT_CHANNEL = 1097083507710369862

client = commands.Bot(command_prefix='!', intents=intents)

def get_image(image_type):
    if image_type == 'cute':
        image_dir = os.path.join('megabot', 'cute')
        image_files = os.listdir(image_dir)
        image_file = random.choice(image_files)
        return os.path.join(image_dir, image_file)
    elif image_type == 'sleep':
        image_dir = os.path.join('megabot', 'sleep')
        image_files = os.listdir(image_dir)
        image_file = random.choice(image_files)
        return os.path.join(image_dir, image_file)
    elif image_type == 'goofy':
        image_dir = os.path.join('megabot', 'goofy')
        image_files = os.listdir(image_dir)
        image_file = random.choice(image_files)
        return os.path.join(image_dir, image_file)
    else:
        return 'default_dog.jpg'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# EVENTS

@client.event
async def on_member_join(member):
    channel = client.get_channel(BOT_CHANNEL)
    await channel.send(f'Welcome {member.name}! Please introduce yourself!')
    """name = member.name
    pfp = member.display.avatar
    embed = discord.Embed(title = "Welcome :D", description = f"Hello {name}. Please introduce yourself!", color = discord.Colour.random())
    embed.set_thumbnail(url = pfp)
    embed.set_author(name)
    embed.add.field(name = "This is a field :P", value="This is a value :D", inline=False)
    embed.set.footer(text = "This is a footer :D")
    await channel.send(embed=embed)"""

@client.event
async def on_member_remove(member):
    author = member.name
    content = f'{author} has left the server.'
    await client.get_channel(BOT_CHANNEL).send(content)

@client.event
async def on_message(message):
    author = message.author.name
    content = message.content
    await client.get_channel(BOT_CHANNEL).send(f'{author}: {content}')

@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel.content
    await client.get_channel(BOT_CHANNEL).send(f'{author} deleted "{content}" from {channel}')

@client.event
async def on_message_edit(message):
    author = message.author
    before_content = before_content
    after_content = after_content
    channel = message.channel.content
    await client.get_channel(BOT_CHANNEL).send(f'{author} edited "{before_content}" to "{after_content}" in {channel}')

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send(f'{user} reacted with {emoji} to "{content}"')

@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send(f'{user} removed their {emoji} reaction from "{content}"')


# COMMANDS

@client.command()
async def cute(ctx):
    # Call the get_image() function with the 'cute' argument and send the image to the channel
    image_path = get_image('cute')
    await ctx.send(file=discord.File(image_path))

@client.command()
async def sleep(ctx):
    # Call the get_image() function with the 'sleep' argument and send the image to the channel
    image_path = get_image('sleep')
    await ctx.send(file=discord.File(image_path))

@client.command()
async def goofy(ctx):
    # Call the get_image() function with the 'goofy' argument and send the image to the channel
    image_path = get_image('goofy')
    await ctx.send(file=discord.File(image_path))

client.run(api_token)
