import requests
import discord
from discord.ext import commands, tasks
import json


class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @tasks.loop(minutes=10)
    async def update_roles(self):
        with open("guild_wroles.json", "r") as f:
            guilds = json.load(f)
        with open("users.json", "r") as f:
            users = json.load(f)
        for u in users.keys():
            usernameT = users[u]["username"]
            userTID = users[u]["userID"]
            url = f'https://ch.tetr.io/api/users/{usernameT}'
            response = requests.get(url)
            data = response.json()
            
            if data["data"]["user"]["league"]["gamesplayed"] < 10: 
                standingT = "User needs to complete at least 10 games."
            elif data["data"]["user"]["league"]["rank"] == "z":
                standingT = data["data"]["user"]["league"]["rating"]
                rankT = "Unranked"
            else:
                standingT = data["data"]["user"]["league"]["rating"]
                rankT = data["data"]["user"]["league"]["rank"]            
            
        
    



def setup(bot):
    bot.add_cog(event(bot))