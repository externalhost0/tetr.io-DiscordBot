import os
import discord
from discord.ext import commands
import json

# prefix
default_prefix = 'tr '
activity = discord.Activity(type=discord.ActivityType.watching, name= default_prefix + "help")

async def determine_prefix(bot, message):
    #Only allow custom prefixs in guild
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    if not str(message.guild.id) in prefixes:
        return default_prefix
    return prefixes[str(message.guild.id)]

intents = discord.Intents().all()

bot = commands.Bot(command_prefix= determine_prefix, activity=activity, status=discord.Status.online, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}')
    print(f'Successfully logged in and booted...!')

initial_extentions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extentions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extentions:
        bot.load_extension(extension)


bot.run(os.getenv('TOKEN'))
