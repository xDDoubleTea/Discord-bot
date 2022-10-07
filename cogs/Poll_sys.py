import discord
from discord import Message, TextChannel, Client, app_command, ButtonStyle
from discord.ui import Button
from discord.ext import commands
from discord.ext.commands import Context
from config.bot_info import get_embed
from typing import List

class PollSys(commands.Cog):
    def __init__(self, client:Client):
        self.client:Client = self.client

    @app_command.command(name = 'Poll', description = '創建投票')
    async def Poll(self, interaction:Interaction, title:str , option:str):
        embed = await get_embed(client = self.client, title = title)
        options = option.split()
        btns:List[Button] = []
        for i,opt in enumerate(options):
            embed.add_field(name = i+1, value = opt, inline = False)

        return await interaction.response.send_message(embed = embed)


async def setup(client):
    client.add_cog(PollSys(client = client))