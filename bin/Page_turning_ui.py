import discord
from discord import Message, TextChannel, Client, User, Member, Embed, TextStyle, Interaction, ButtonStyle
from typing import List, Union, Dict
from discord.ui import Button, button, Modal, View, TextInput
import math
from config.bot_info import get_embed

async def multiple_page_data_formating(data:list, name:str, value:str):
    #if name contains number index ,use -{i} to format.
    #if name contains indivisiual element, use -{ele} to format.
    for i,obj in enumerate(data):
        data.append({"name":name,"value":value})
    

class PageTurningSys(View):
    def __init__(self, data:List[Dict[str,str]], nowpage:int = 1, attached_msg:Message = None):
        super().__init__(timeout = 3600)
        self.attached_msg:Message = attached_msg
        self.data = data
        self.nowpage:int = nowpage
        self.totalpages = int(math.ceil(len(data)/10))

    async def on_timeout(self):
        try:
            return await self.attached_msg.edit(view = None)
        except:
            self.clear_items()
    
    async def new_page(self, client:Client):
        embed_title = self.attached_msg.embeds[0].title
        embed_desc = self.attached_msg.embeds[0].description
        embed_footer = self.attached_msg.embeds[0].footer
        embed = await get_embed(client = client, title = embed_title, desc = embed_desc)
        gnd = (self.nowpage-1)*10
        lim = 0
        if gnd + 10 > len(self.data):
            lim = len(self.data)
        else:
            lim = gnd + 10
        for i in range(gnd, lim):
            embed.add_field(name = self.data[i]["name"], value = self.data[i]["value"], inline = False)
        embed.set_footer(text = f'{embed_footer.text} \n 第{self.nowpage}/{self.totalpages}頁', icon_url = embed_footer.icon_url)
        return embed
    
    @button(label = '上一頁', emoji = '◀️', style = ButtonStyle.blurple)
    async def prev_callback(self, interaction:Interaction, button:Button):
        if self.attached_msg == None:
            self.attached_msg = interaction.message
        if self.nowpage > 1:
            self.nowpage -= 1
            embed = await self.new_page(client = interaction.client)
            return await interaction.response.edit_message(embed = embed)
        else:
            return await interaction.response.defer()
        
    
    @button(label = '下一頁', emoji = '▶️', style = ButtonStyle.blurple)
    async def next_callback(self, interaction:Interaction, button:Button):
        if self.attached_msg == None:
            self.attached_msg = interaction.message
        if self.nowpage < self.totalpages:
            self.nowpage += 1
            embed = await self.new_page(client = interaction.client)
            return await interaction.response.edit_message(embed = embed)
        else:
            return await interaction.response.defer()