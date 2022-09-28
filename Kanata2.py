import discord
from discord.ext import commands, tasks
from discord import app_commands, Client
from discord import Interaction
import os
from datetime import date
from config.bot_info import pre, bot_token, application_id, MY_GUILD



intents = discord.Intents.all()

@tasks.loop(minutes=15)
async def change_stats():
    today = date.today()
    test_day = date(year = 2023, month = 1, day = 13)
    to_test_day = abs(test_day - today)
    countdown:str = f'學測倒數{to_test_day.days}天BBQ了'
    return await client.change_presence(status = discord.Status.online, activity = discord.Game(name = countdown))

class Kanata2(commands.Bot):
    def __init__(self, *, intents:discord.Intents):
        super().__init__(command_prefix = pre, intents = intents, application_id = application_id, help_command=None)

    async def setup_hook(self):
        for files in os.listdir('./cogs'):
            if files.endswith('.py'):
                await self.load_extension(f'cogs.{files[:-3]}')
        self.tree.copy_global_to(guild = MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = Kanata2(intents=intents)

@client.event
async def on_ready():
    print(f'Bot is ready{client.user}')
    await change_stats.start()

client.run(bot_token)