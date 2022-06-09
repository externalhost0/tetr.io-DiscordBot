import discord
from discord.ext import commands
import json
import requests
import os


class channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # SETUP FOR CHANNEL NOTIFICATIONS
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setupchannel(self, ctx, arg1 = ""):
        await ctx.send("Setting up...")
        guild = ctx.guild
        if arg1 == "":
            return await ctx.send("Please include the ID of the channel at the end of the command.")
        #discord.utils.get(guild.channels, name="T Notifs")


        await ctx.send("Finished, channel will now be automatically updated!")
        return 









def setup(bot):
    bot.add_cog(channels(bot))