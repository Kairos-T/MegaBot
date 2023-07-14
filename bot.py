import discord 
import os
import random
import requests
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import HelpCommand
from decouple import Config

# ============================= HELP COMMAND =============================
class MyHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"help": "Shows help for the bot commands"})

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="MegaBot Help", description="Here's a list of all the available commands:", color=0xeee657)
        for cog, commands in mapping.items():
            if cog is None:
                name = "General"
            else:
                name = cog.qualified_name
            value = "\n".join([f"`{cmd.name}` - {cmd.short_doc}" for cmd in commands])
            if value:
                embed.add_field(name=name, value=value, inline=False)
        await self.get_destination().send(embed=embed)

# ============================= END HELP COMMAND =============================

config = Config('megabot.env')
BOT_TOKEN  = config.get('DISCORD_TOKEN')

BOT_CHANNEL = config.get('DISCORD_CHANNEL')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"), intents=intents)
bot.help_command = MyHelpCommand()

mygroup = app_commands.Group(name="greetings", description="Welcomes users")
blockedwords = ["kms"]

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
    await channel.send("Goodbye {}!".format(member))
    
@bot.event
async def on_message(message):
    author = message.author
    content = message.content
    await bot.process_commands(message)
    print("{}: {}".format(author,content))
    
    if author != bot.user:
        for text in blockedwords:
            if "Megabot" not in str(author.roles) and text.lower() in str(content.lower()):
                await message.channel.send("Please do not use that word.")
                await message.delete()
                break
            

@bot.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    print("{}: {}".format(author,content))

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
    ping.short_doc = "Plays ping pong with MegaBot"

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="MegaBot", description="Hi! I'm a bot created by Kairos to make your Discord server more fun and interactive.", color=0xeee657)
    embed.add_field(name="Commands", value="Type `!help` to see a list of all the available commands.")
    embed.add_field(name="Source Code", value="You can find my source code on [GitHub](https://github.com/Kairos-T/MegaBot).")
    embed.set_footer(text="Thanks for using MegaBot!")
    await ctx.send(embed=embed)
    about.short_doc = "Shows information about MegaBot"

@bot.command()
async def coinflip(ctx):
    result = random.choice(["heads", "tails"])
    await ctx.send(f"The coin landed on **{result}**!")
    coinflip.short_doc = "Flips a coin, landing on either heads or tails"

@bot.command()
async def roll(ctx, sides: float = 6.0):
    try:
        sides = int(sides)
    except ValueError:
        await ctx.send("The number of sides must be an integer.")
        return
    if sides < 2:
        await ctx.send("The dice must have at least 2 sides.")
        return
    result = random.randint(1, sides)
    await ctx.send(f"The dice rolled **{result}**!")
    roll.short_doc = "Roll a dice with the specified number of sides (default is 6)"

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
    cute.short_doc = "Sends a cute image of Mega"

@bot.command()
async def sleep(ctx):
    sleep_folder = "sleep"
    sleep_files = os.listdir(sleep_folder)
    sleep_file = random.choice(sleep_files)
    with open(os.path.join(sleep_folder, sleep_file), "rb") as f:
        sleep_image = discord.File(f)
        await ctx.send("Here's sleepy Mega!", file=sleep_image)
    sleep.short_doc = "Sends an image of sleepy Mega"


@bot.command()
async def goofy(ctx):
    goofy_folder = "goofy"
    goofy_files = os.listdir(goofy_folder)
    goofy_file = random.choice(goofy_files)
    with open(os.path.join(goofy_folder, goofy_file), "rb") as f:
        goofy_image = discord.File(f)
        await ctx.send("Here's a goofy image of Mega!", file=goofy_image)
    goofy.short_doc = "Sends a goofy image of Mega"

# ============================= END COMMANDS (MEGA) =============================
 

# ============================= COMMANDS (MODERATION) =============================
@bot.command()
@commands.has_any_role("alexander", "Megabot")
async def ban(ctx, user:discord.Member):
    if user in ctx.guild.members:
        await user.ban()
        await ctx.send(f"{user.display_name} has been banned.")
    else:
        await ctx.send("User not found.")

@bot.command()
@commands.has_any_role("alexander", "Megabot")
async def unban(ctx, name:str):
    notFound = True
    entryName = user.display_name
    async for entry in ctx.guild.bans(limit = None):
        user = entry.user
        entryName = user.display_name
        if entryName == name:
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned user: {user.display_name}")
            notFound = False
    if notFound:
        await ctx.send("User not found.")
# ============================= END COMMANDS (MODERATION) =============================

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