from typing import Type
import discord
from discord.ext import commands
from discord.ext.commands import Context, Cog
from discord import Message, TextChannel, Client, app_commands, Interaction
import json
from bin.Page_turning_ui import PageTurningSys
from bin.To_do_list_ui import TodoListNotAvailable, append_to_do, del_item, edit_stats, get_page_turning_view, output_list, todolist_edit
from config.bot_info import pre
from config.bot_info import get_embed


class To_do_list(Cog):
    def __init__(self, client):
        self.client:Client = client

    @app_commands.command(name = 'add_to_do', description='加入待辦事項')
    @app_commands.describe(data = '你想要加入的事項')
    async def add_to_do(self, interaction:Interaction, *, data:str = None):
        if data != None:
            append_to_do(data = data, stats = '【未完成】', dc_user = interaction.user)
            tmp = await get_page_turning_view(client = interaction.client, user = interaction.user)
            return await interaction.response.send_message(f'已將`{data}`加入到待辦清單內！目前的待辦清單：', embed = tmp[1], ephemeral=True, view = tmp[0])
        else:
            embed = await get_embed(client = self.client, title = '❌ | 缺乏選項！', desc = '新增選項？')
            return await interaction.response.send_message(embed = embed, view = todolist_edit())

    @commands.command(name = 'edit_to_do', aliases = ['edit_td'])
    async def edit_to_do(self, ctx:Context, index= None, stats:str = None):
        if index == None or stats == None:
            return await ctx.send(f'❌輸入錯誤！使用方法：`{pre}edit_td <事項編號> <狀態>`')
        else:
            try:
                await edit_stats(user = ctx.author, index = index, stats = stats)
            except IndexError:
                return await ctx.send('❌你的待辦清單沒有那麼多項！')
            except TypeError:
                return await ctx.send('❌索引值必須是一個整數！')
            except TodoListNotAvailable:
                return await ctx.send('❌你還沒有創建一個待辦清單！')

            embed = await output_list(client = self.client, user = ctx.author)
            return await ctx.send(f'✅已將編號第`{int(index)}`個事項之狀態設為`{stats}`', embed = embed)
        
    @commands.command(name = 'del_to_do', aliases = ['del_td'])
    async def del_to_do(self, ctx:Context, index=None):
        if index != None:
            try:
                await del_item(user = ctx.author, index = index)
            except IndexError:
                return await ctx.send('❌你的待辦清單沒有那麼多項！')
            except TypeError:
                return await ctx.send('❌索引值必須是一個整數！')
            except TodoListNotAvailable:
                return await ctx.send('❌你還沒有創建一個待辦清單！')

            embed = await output_list(client = self.client, user = ctx.author)
            return await ctx.send(f'✅已將編號第`{int(index)}`個事項移除', embed = embed)
        else:
            return await ctx.send('❌請輸入你要刪除的事項編號！')

    @app_commands.command(name = 'check_to_do', description='回傳你的待辦清單')
    async def check_to_do(self, interaction:Interaction):
        embed = await output_list(client = self.client, user = interaction.user)
        with open('to_do_list.json', 'r') as file:
            raw_data = json.load(file)
        user_data = None
        for i in raw_data["todo"]:
            if i["user_id"] == interaction.user.id:
                user_data = i
                break
        if user_data != None:
            data = []
            for x,i in enumerate(user_data["list"]):
                data.append(
                    {
                        "name":f"事項編號：{x+1}\n事項狀態：{i['stats']}", 
                        "value":f"📑📝**{i['content']}**"
                    }
            )
            v = PageTurningSys(data = data)
            return await interaction.response.send_message(embed = embed, ephemeral=True, view = v)
        else:
            return await interaction.response.send_message('❌你還沒有創建一個待辦清單！', ephemeral=True)
    
    @app_commands.command(name = 'td', description='待辦清單ui介面')
    async def to_do(self, interaction:Interaction):
        embed = await get_embed(client = self.client, title = '📝 | 待辦清單功能', desc = '請選擇服務')
        return await interaction.response.send_message(embed = embed, view = todolist_edit())

async def setup(client):
    await client.add_cog(To_do_list(client))