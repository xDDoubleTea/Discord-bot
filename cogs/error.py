import discord 
import random
from discord.ext import commands
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import emoji
import time
from pytube.__main__ import YouTube
from discord.ui import Button, View
import random


Me = 398444155132575756

class error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        global Me

        guild = ctx.message.guild
        me = self.client.get_user(Me)
        if guild == None:
            embed = discord.Embed(
                title = f'Error!',
                description=error,
                color = discord.Colour.blue()
            )
        else:
            embed = discord.Embed(
                title = f'Error! in {guild.name}',
                description=error,
                color = discord.Colour.blue()
            )

        if ctx.message.author != Me:
            await ctx.message.channel.send(embed = embed)

        await me.send(embed=embed)
    


async def setup(client):
    await client.add_cog(error(client))












