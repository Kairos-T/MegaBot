import discord 
import os
import random
from discord.ext import commands
from discord import app_commands
from decouple import Config

config = Config('megabot.env')
BOT_TOKEN  = config.get('DISCORD_TOKEN')

BOT_CHANNEL = config.get('DISCORD_CHANNEL')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"), intents=intents)

mygroup = app_commands.Group(name="greetings", description="Welcomes users")

# ============================= EVENTS =============================
@bot.event
async def on_ready():
    print("Bot is ready")

    bot.tree.add_command(mygroup)

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} Command(s)')
    except Exception as e:
        print(e)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(BOT_CHANNEL)
    await channel.send("Welcome to the server {}".format(member.mention))
    
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(BOT_CHANNEL)
    await channel.send("Goodbye, you will be deeply missed :(")
    
@bot.event
async def on_message(message):
    author = message.author
    content = message.content
    await bot.process_commands(message)
    print("{}: {}".format(author,content))

@bot.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await channel.send("{}: {}".format(author,content))

@bot.event
async def on_message_edit(before,after):
    if before.author == bot.user:
        return;
    before_content = before.content
    after_content = after.content
    channel = before.channel
    await channel.send("Before: {}".format(before_content))
    await channel.send("After: {}".format(after_content))

@bot.event
async def on_reaction_add(reaction,user):
    if user == bot.user:
        return;
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send("{} has reacted with {} to the message {}".format(name,emoji, content))


@bot.event
async def on_reaction_remove(reaction,user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send("{} has removed their reaction of {} to the message {}".format(name,emoji, content))

# ============================= COMMANDS (GENERAL) =============================

@bot.command()
async def ping(ctx):    
    message = await ctx.send("Pong!")
    await ctx.message.add_reaction("🏓")
    
@bot.command()
async def delete(ctx, user:discord.User):
    async for message in ctx.channel.history(limit = None):
        if message.author == user and message.id != ctx.message.id:
            await message.delete()  
            break

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="MegaBot", description="Hi! I'm a bot created by Kairos to make your Discord server more fun and interactive.", color=0xeee657)
    embed.add_field(name="Commands", value="Type `!help` to see a list of all the available commands.")
    embed.add_field(name="Source Code", value="You can find my source code on [GitHub](https://github.com/Kairos-T/MegaBot).")
    embed.set_footer(text="Thanks for using MegaBot!")
    await ctx.send(embed=embed)

@bot.command()
async def coinflip(ctx):
    result = random.choice(["heads", "tails"])
    await ctx.send(f"The coin landed on **{result}**!")

@bot.command()
async def roll(ctx, sides: int = 6):
    if sides < 2:
        await ctx.send("The dice must have at least 2 sides.")
        return
    result = random.randint(1, sides)
    await ctx.send(f"The dice rolled **{result}**!")

# ============================= END COMMANDS (GENERAL) =============================

        
        
# ============================= COMMANDS (Mega) =============================

@bot.command()
async def cute(ctx):
    cute_folder = "cute"
    cute_files = os.listdir(cute_folder)
    cute_file = random.choice(cute_files)
    with open(os.path.join(cute_folder, cute_file), "rb") as f:
        cute_image = discord.File(f)
        await ctx.send("Here's a cute image of Mega!", file=cute_image)

@bot.command()
async def sleep(ctx):
    sleep_folder = "sleep"
    sleep_files = os.listdir(sleep_folder)
    sleep_file = random.choice(sleep_files)
    with open(os.path.join(sleep_folder, sleep_file), "rb") as f:
        sleep_image = discord.File(f)
        await ctx.send("Here's sleepy Mega!", file=sleep_image)

@bot.command()
async def goofy(ctx):
    goofy_folder = "goofy"
    goofy_files = os.listdir(goofy_folder)
    goofy_file = random.choice(goofy_files)
    with open(os.path.join(goofy_folder, goofy_file), "rb") as f:
        goofy_image = discord.File(f)
        await ctx.send("Here's a goofy image of Mega!", file=goofy_image)

# ============================= END COMMANDS (MEGA) =============================


@bot.tree.command(description="Greets user")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")

@mygroup.command(description="Pings user")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Ping {interaction.user.mention}!")

@mygroup.command(description="Pongs user")
async def pong(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong {interaction.user.mention}!")

bot.run(BOT_TOKEN)