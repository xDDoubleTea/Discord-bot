import discord
from discord.ext import tasks, commands


from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import time

version = 1.0
MyDiscordID = "星詠み#6942"
default_footer = f"Developed by {MyDiscordID} version:{version}"
default_footer_icon = "https://cdn.discordapp.com/avatars/398444155132575756/77db70f07858b08a72896f248e2ffcaf.webp?size=4096"


UTC = pytz.utc




now = 0
after = 0

class tasks(commands.Cog):
    def __init__(self, client):
        self.client = client


    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(minutes = 5)
    async def change_channel(self):
        global now
        global after

        today = date.today()
        now = today.strftime("%Y/%m/%d")
        


    

def setup(client):
    client.add_cog(tasks(client))