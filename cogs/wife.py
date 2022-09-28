import discord 
import random
from discord.ext import commands
from config.bot_info import *


class wife(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["girlfriend"], help = f"I'm {MyDiscordID}'s wife")
    async def wife(self, ctx, *, input):
        input = input.lower()
        if input.startswith("do you love me") and ctx.author.id == My_user_id:
            await ctx.send("Yes!!!Daisuki dayo!")
        else:
            await ctx.send("No...I'm already in love with someone else. And I will never betray him because he's my only one.")
        
async def setup(client):
    await client.add_cog(wife(client))
        