import discord
from discord.ext import commands
import json
import requests
import os
from colorthief import ColorThief

class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setprefix(self, ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f)
        
        await ctx.send("Prefixes set!")

    # SETUP FOR ROLES
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setuproles(self, ctx):
        with open("guild_wroles.json", "r") as f:
            guilds = json.load(f)
            guildID = str(ctx.guild.id)
            if not guildID in guilds:
                guilds[guildID] = {}
        await ctx.send("Setting up...")
        guild = ctx.guild
        perms = discord.Permissions()
        perms.update(read_messages=False)
        rankcolor = [0x8f748f, 0x80587f, 0x6c417c, 0x682b7d, 0x53237a, 0x564ec4, 
        0x4d63c8, 0x52a5c7, 0x48bb8f, 0x5ec154, 0x3eb646, 0xbb9b3b, 0xc7b62d, 0xffef61, 0xffaf0f, 0xff4c11, 0xff4cff]

        for index, i in enumerate(["D", "D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+", "S-", "S", "S+", "SS", "U", "X"]):
            await guild.create_role(name=f"TRank: {i}", permissions=perms, colour=rankcolor[index])
        
        await ctx.send("Finished, roles have been created will be updated automatically!")
        return 

    # DELETES THE ROLES CREATED BY THE SETUP
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def removeroles(self, ctx):
        await ctx.send("Cleaning up...")
        guild = ctx.guild
        for i in ["D", "D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+", "S-", "S", "S+", "SS", "U", "X"]:
            role_object = discord.utils.get(guild.roles, name=f"TRank: {i}")
            await role_object.delete()
        
        await ctx.send("Finished, role functionality have been removed.")
        return 


    # REGISTER NEW USERS COMMAND
    @commands.command()
    async def register(self, ctx, arg1 = ""):
        if arg1 == "": return await ctx.send("Please include a username after the command name.")
        user = arg1
        url = f'https://ch.tetr.io/api/users/{user}'
        response = requests.get(url)
        data = response.json()
        if not data["success"]: return await ctx.send("User does not exist.")
        username = data["data"]["user"]["username"]
        userID = data["data"]["user"]["_id"]
        with open("users.json", "r") as f:
            users = json.load(f)
            discordID = str(ctx.message.author.id)
            if discordID in users: return await ctx.send("You can only have one linked account.")
            
            if userID in users[discordID]:
                return await ctx.send("You are already registered.")
            else:
                users[discordID]["username"] = username
                users[discordID]["userID"] = userID

            with open("users.json", "w") as f:
                json.dump(users, f)
        
            await ctx.send("You have been registered! \nYou can also view your profile with the command `.profile [username]`")
            #await ctx.send(url)


    @commands.command()
    @commands.guild_only()
    async def stats(self, ctx, arg1= ""):
        await ctx.send("Working...", delete_after=0.01)
        usernameT = ""
        time_list = []
        score_list = []
        level_list = []
        rank_list = []
        if arg1.lower() == "40l" or arg1 ==  "40":
            embed=discord.Embed(title="40L Rankings", description="Top 40L times in this server.", color=discord.Color.from_rgb(238, 191, 49))
            with open("users.json", "r") as f:
                users = json.load(f)
            for u in users.keys():
                usernameT = users[u]["username"]
                userTID = users[u]["userID"]
                url = f'https://ch.tetr.io/api/users/{userTID}/records'
                response = requests.get(url)
                data = response.json()
                if not data["data"]["records"]["40l"]["record"]: 
                    timeT = "No Time."
                else:
                    timeT = data["data"]["records"]["40l"]["record"]["endcontext"]["finalTime"]
                
                millis = timeT
                milliseconds= int(timeT) % 1000
                seconds=(millis/1000)%60
                seconds = int(seconds)
                minutes=(millis/(1000*60))%60
                minutes = int(minutes)
                #hours=(millis/(1000*60*60))%24     UNUSED VARIABLE, KEEPING FOR LATER
                timeT = ("%d:%d:%d" % (minutes, seconds, milliseconds))         
                time_list.append({ "time": str(timeT), "username": usernameT })
            time_list.sort(key=lambda u : u["time"] if u["time"] != "No Time" else "0")
            embed.add_field(name="Username", value="\n".join([u["username"] for u in time_list]), inline=True)
            embed.add_field(name="Times", value="\n".join([u["time"] for u in time_list]), inline=True)
            embed.set_thumbnail(url="https://i.imgur.com/l5N24oG.png")
            await ctx.send(embed=embed)

        elif arg1.lower() == "blitz" or arg1.lower() ==  "b":
            embed=discord.Embed(title="Blitz Rankings", description="Top Blitz scores in this server.", color=discord.Color.from_rgb(226, 63, 1))
            with open("users.json", "r") as f:
                users = json.load(f)
            for u in users.keys():
                usernameT = users[u]["username"]
                userTID = users[u]["userID"]
                url = f'https://ch.tetr.io/api/users/{userTID}/records'
                response = requests.get(url)
                data = response.json()
                if not data["data"]["records"]["blitz"]["record"]: 
                    scoreT = "No Score"
                else:
                    scoreT = data["data"]["records"]["blitz"]["record"]["endcontext"]["score"]

                score_list.append({ "score": str(scoreT), "username": usernameT })
            score_list.sort(key=lambda u : u["score"] if u["score"] != "No Score" else "0", reverse=True)
            embed.add_field(name="Username", value="\n".join([u["username"] for u in score_list]), inline=True)
            embed.add_field(name="Scores", value="\n".join([u["score"] for u in score_list]), inline=True)
            embed.set_thumbnail(url="https://i.imgur.com/ctIHoTk.png")
            await ctx.send(embed=embed)

        elif arg1.lower() == "zen" or arg1.lower() ==  "z":
            embed=discord.Embed(title="Zen Rankings", description="Top Zen scores in this server.", color=discord.Color.from_rgb(161, 89, 232))
            with open("users.json", "r") as f:
                users = json.load(f)
            for u in users.keys():
                usernameT = users[u]["username"]
                userTID = users[u]["userID"]
                url = f'https://ch.tetr.io/api/users/{userTID}/records'
                response = requests.get(url)
                data = response.json()
                if not data["data"]["zen"]["level"]: 
                    levelT = "User has not done Zen."
                else:
                    levelT = data["data"]["zen"]["level"]
                
                level_list.append({ "level": str(levelT), "username": usernameT })
            level_list.sort(key=lambda u : u["level"] if u["level"] != "User has not done Zen." else "0", reverse=True)
            embed.add_field(name="Username", value="\n".join([u["username"] for u in level_list]), inline=True)
            embed.add_field(name="Level", value="\n".join([u["level"] for u in level_list]), inline=True)
            embed.set_thumbnail(url="https://i.imgur.com/4xbbX79.png")
            await ctx.send(embed=embed)

        elif arg1 == "":
            embed=discord.Embed(title="Player Rankings", description="Top ranking players in this server.", color=discord.Color.from_rgb(246, 150, 53))
            with open("users.json", "r") as f:
                users = json.load(f)
            for u in users.keys():
                usernameT = users[u]["username"]
                userTID = users[u]["userID"]
                url = f'https://ch.tetr.io/api/users/{userTID}'
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
                standingT = round(standingT)
                if not rankT == "Unranked": rankT = rankT.upper()
                rank_list.append({ "rank": str(rankT), "username": usernameT, "standing": str(standingT) })
            embed.add_field(name="Username", value="\n".join([u["username"] for u in rank_list]), inline=True)
            embed.add_field(name="Rank", value="\n".join([u["rank"] for u in rank_list]), inline=True)
            embed.add_field(name="Standing", value="\n".join([u["standing"] for u in rank_list]), inline=True)
            embed.set_thumbnail(url="https://i.imgur.com/fhQQUmP.png")
            await ctx.send(embed=embed)
        else:
            await ctx.send("That is not a command I offer.")





    @commands.command()
    async def profile(self, ctx, arg1 = ""):
        if arg1 == (""):
            return await ctx.send("Please specify the user.")

        usernameT = arg1
        url = f'https://ch.tetr.io/api/users/{usernameT}'
        response = requests.get(url)
        data = response.json()
        # returns if user does not exist in database
        if not data["success"]: return await ctx.send("User does not exist.")
        userTID = data["data"]["user"]["_id"]
        country = data["data"]["user"]["country"]
        gamesplayed = data["data"]["user"]["gamesplayed"]
        gameswon = data["data"]["user"]["gameswon"]
        hours = data["data"]["user"]["gametime"]
        hours=round(hours/3600)
        if "bio" in data["data"]["user"]:
            bio = data["data"]["user"]["bio"]
        else:
            bio = ""
        if not "avatar_revision" in data["data"]["user"]:
            dominant_color = (0,0,0)
            checker = False
        else:
            checker = True
            avatar_revision = data["data"]["user"]["avatar_revision"]
            image_url = f'https://tetr.io/user-content/avatars/{userTID}.jpg?rv={avatar_revision}'
            response = requests.get(image_url)
            open("images/tpfp.jpg", "wb").write(response.content)
            image_filename = ColorThief("images/tpfp.jpg")
            dominant_color = image_filename.get_color(quality=1)
        embed=discord.Embed(title=usernameT.upper() + " Profile", description=f"{bio} \n \n **Country: ** {country} \n **Hours: ** {hours} \n **Online Games Won: **  {gameswon}/{gamesplayed}", color=discord.Color.from_rgb(*dominant_color))
        if checker == True: os.remove("images/tpfp.jpg")
        if data["data"]["user"]["league"]["gamesplayed"] < 10: 
            standingT = "User needs to complete at least 10 games."
        else:
            standingT = data["data"]["user"]["league"]["rating"]
            standingT = round(standingT)

        if not "ts" in data["data"]["user"]:
            creation_date = "Very Early"
        else:
            creation_date = data["data"]["user"]["ts"]
        
        if not "avatar_revision" in data["data"]["user"]:
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/gmod/images/9/99/The_Missing_textures.png/revision/latest?cb=20210208200840")  # Source's missing texture, being pulled from a random website
        else:
            avatar_revision = data["data"]["user"]["avatar_revision"]
            embed.set_thumbnail(url=f'https://tetr.io/user-content/avatars/{userTID}.jpg?rv={avatar_revision}')
        
        rankT = data["data"]["user"]["league"]["rank"]
        if rankT == "z": rankT = "Unranked"
        xpT = data["data"]["user"]["xp"]
        apm = data["data"]["user"]["league"]["apm"]
        pps = data["data"]["user"]["league"]["pps"]
        vs = data["data"]["user"]["league"]["vs"]
        if str(apm) == "None":                          # Sets APM, PPS and VS stats to "Unknown" instead of "None"
            apm = "Unknown"
            pps = "Unknown"
            vs = "Unknown"
        embed.add_field(name="APM", value=apm)
        embed.add_field(name="PPS", value=pps)
        embed.add_field(name="VS", value=vs)
        embed.add_field(name="Rank", value=rankT.upper())
        embed.add_field(name="Standing", value=standingT)
        embed.add_field(name="XP", value=round(xpT))
        embed.set_footer(text="Account created: " + creation_date[:10])
        await ctx.send(embed=embed)



    # HELP COMMAND
    @commands.command()
    async def help(self, ctx):
        default_prefix = "tr "
        embed=discord.Embed(title="Tetra Bot's Command List", description="Here you can find the complete list of commands for Tetra.", color=discord.Color.from_rgb(100, 118, 237))
        embed.add_field(name="Register", value=f"Adds a new player to the database, required to show statistics of the player. Registering will connect your discord account to your tetr.io profile.`{default_prefix}register (username)`", inline=False)
        embed.add_field(name="Profile", value=f"Shows the user's tetr.io profile.`{default_prefix}profile (username)`", inline=False)
        embed.add_field(name="Stats", value=f"Shows all registered users TR standing and rank.`{default_prefix}stats`", inline=False)
        embed.add_field(name="40L Stats", value=f"Shows all registered users top 40L times.`{default_prefix}stats 40L`", inline=False)
        embed.add_field(name="Blitz Stats", value=f"Shows all registered users top blitz scores.`{default_prefix}stats blitz`", inline=False)
        embed.add_field(name="Zen Stats", value=f"Shows all registered users current zen levels.`{default_prefix}stats zen`", inline=False)
        embed.add_field(name="Set Prefix", value=f"*ADMIN ONLY COMMAND*, Changes the prefix of the bot for that server.`{default_prefix}setprefix (prefix)`", inline=False)
        embed.add_field(name="Setup Roles", value=f"*ADMIN ONLY COMMAND*, Adds Tetra League roles for players that are registered.`{default_prefix}setuproles`", inline=False)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(command(bot))