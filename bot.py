import os
import random
import discord
from discord.ext import commands
#from discord.ext import app_commands

from decouple import Config

config = Config('megabot.env')
api_token = config.get('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True
#intents.members_content = True
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

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} Command(s)")
    except Exception as e:
        print(e)

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
    channel = client.get.channel(BOT_CHANNEL)
    await channel.send(f'{member.name} has left the server.')

@client.event
async def on_message(message):
    author = message.author
    content = message.content
    await client.process_commands(message)
    print(f'{author}: {content}')
    #await client.get_channel(BOT_CHANNEL).send(f'{author}: {content}')

@client.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await client.channel.send(f'{author} deleted "{content}" from {channel}')

@client.event
async def on_message_edit(before, after):
    author = before.author
    channel = before.channel
    before_content = before_content
    after_content = after_content
    await channel.send(f"Before: {before_content}\nAfter: {after_content}")
    #await client.get_channel(BOT_CHANNEL).send(f'{author} edited "{before_content}" to "{after_content}" in {channel}')

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return;

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send(f'{name} reacted with {emoji} to "{content}"')

@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send(f'{name} removed their {emoji} reaction from "{content}"')


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
