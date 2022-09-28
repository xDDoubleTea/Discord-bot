import discord
from discord.ext import commands
from discord import Interaction, app_commands
from discord.ext.commands import Context 
from discord.ui import Button , View, Modal

from config.bot_info import MY_GUILD

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name = 'ping', description='pings the bot')
    async def ping(self, interaction:Interaction):
        return await interaction.response.send_message(f'✅延遲：{round(interaction.client.latency*1000)}ms')

async def setup(client):
    await client.add_cog(test(client), guilds = [MY_GUILD])