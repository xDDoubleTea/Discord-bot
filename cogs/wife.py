import discord 
import random
from discord.ext import commands


version = 1.0
MyDiscordID = "星詠み#6942"
default_footer = f"Developed by {MyDiscordID} version:{version}"
default_footer_icon = "https://cdn.discordapp.com/avatars/398444155132575756/77db70f07858b08a72896f248e2ffcaf.webp?size=4096"
me = 398444155132575756

class wife(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["girlfriend"], help = f"I'm {MyDiscordID}'s wife")
    async def wife(self, ctx, *, input):
        input = input.lower()
        if input.startswith("do you love me") and ctx.author.id == me:
            await ctx.send("Yes!!!Daisuki dayo!")
        else:
            await ctx.send("No...I'm already in love with someone else. And I will never betray him because he's my only one.")
    
    @commands.command(aliases = ['pic'], help = "Wife's picture")
    async def picture(self, ctx):
        if ctx.author.id == me:
            pictures_url = ["https://i.imgur.com/MFQsnNi",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713934692761681/20211004_061750.jpg",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713935120588810/20211004_061746.jpg",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713935514837072/20210913_123754.jpg",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713935992995850/20211101_100306.jpg",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713936366297098/20211104_164524.jpg",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713936978645063/20211018_110910.jpg",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713937402286090/20211014_160923.jpg",
                            "https://cdn.discordapp.com/attachments/672102728469577785/906713937653956618/20211004_122815.jpg"]
            await ctx.author.send(f'{random.choices(pictures_url)[0]}')
        else:
            await ctx.author.send("https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173")
    @commands.command(aliases = [], help = "")
    async def a(self, ctx):
        print("a")











        
def setup(client):
    client.add_cog(wife(client))
        