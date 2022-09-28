import discord
from discord.ext import commands
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import time
from config.bot_info import *


UTC = pytz.utc

class Time(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ["wldt","wt"], help = "Returns (EST,PST,UTC,GMT,CTT)")
    async def worldtime(self, ctx):
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        embed = discord.Embed(
            title = "World time",
            description = "The world time",
            color = discord.Colour.blue()
        )
        datetime_utc = datetime.now(UTC)
        embed.add_field(
            name = "UTC",
            value = f"{datetime_utc.strftime('%Y:%m:%d %H:%M:%S %Z %z')}",
            inline = False
        )
        embed.set_author(name = f"{self.client.user}", icon_url = self.client.get_user(My_user_id).avatar.url)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
        await ctx.send(embed = embed)

async def setup(client):
    await client.add_cog(Time(client))