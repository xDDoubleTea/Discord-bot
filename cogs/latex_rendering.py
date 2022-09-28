import discord
from discord import Interaction
from discord.ui import button, select, View, Button
from discord.ext import commands

from IPython.display import Latex, display_latex
from IPython.lib import latextools
import matplotlib.pyplot as plt
import io
from bin.Latex_handling import Latex_render_for_dc, latex_msg_options



class latex_rendering(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def latex_rendering(self,message:discord.Message, data:str):
        renderer = Latex_render_for_dc()
        img = await renderer.Latex_dvipng(string = data)
        if img != None:
            msg = await message.reply(file = img, mention_author = False)
            return await msg.edit(view = latex_msg_options(attached_msg = msg, latex_data=data))
        else:
            msg = await message.reply(mention_author = False, content = 'Falied to render! Please check if the input has any possible error!')
            await msg.edit(view = await renderer.fail_rendering(msg = msg))
            return await msg.add_reaction('❗')

    @commands.command(name = 'latex')
    async def latex(self, ctx, *, data):
        return await self.latex_rendering(message = ctx.message, data = data)

async def setup(client):
    await client.add_cog(latex_rendering(client))