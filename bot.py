import os
import random
import discord
from discord.ext import commands
#import requests
#import json

from decouple import Config
config = Config('megabot.env')
api_token = config.get('DISCORD_TOKEN')

client = discord.Client()
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


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def cute(ctx):
    # Call the get_image() function with the 'cute' argument and send the image to the channel
    image_path = os.path.join('megabot', 'cute', get_image('cute'))
    await ctx.send(file=discord.File(image_path))

@client.command()
async def sleep(ctx):
    # Call the get_image() function with the 'sleep' argument and send the image to the channel
    image_path = os.path.join('megabot', 'sleep', get_image('sleep'))
    await ctx.send(file=discord.File(image_path))

@client.command()
async def goofy(ctx):
    # Call the get_image() function with the 'goofy' argument and send the image to the channel
    image_path = os.path.join('megabot', 'goofy', get_image('goofy'))
    await ctx.send(file=discord.File(image_path))


client.run(api_token)
