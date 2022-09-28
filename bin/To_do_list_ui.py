from typing import Union
import discord
from discord import Message, TextChannel, Client, Interaction, ButtonStyle, TextStyle, User
from discord.ui import Button, button, Select, select, Modal, View, TextInput
import json
from bin.Page_turning_ui import PageTurningSys
from config.bot_info import get_embed
from config.bot_info import pre

class TodoListNotAvailable(Exception):
    def __init__(self):
        super().__init__()


class append_Modal(Modal):
    def __init__(self):
        super().__init__(title = '新增待辦事項', timeout = 600)
    
    new = TextInput(label = '待辦事項', style = TextStyle.long, max_length = '1000', placeholder = '明天要寫完化學講義P.34~P.50', required = True)
    status = TextInput(label = '狀態(選填，預設值為【未完成】)', style = TextStyle.short, max_length = '50', placeholder = '目前進度到P.43', required = False)

    async def on_submit(self, interaction: Interaction):
        stats = '【未完成】'
        if self.status.value != '':
            stats = self.status.value
        append_to_do(data = self.new.value, stats = stats, dc_user = interaction.user)
        embed = await get_embed(client = interaction.client, title = '✅完成動作', desc = '**加入待辦事項**')
        await interaction.message.edit(embed = embed)
        tmp = await get_page_turning_view(client = interaction.client, user = interaction.user)
        return await interaction.response.send_message(f'已將`{self.new.value}`加入到待辦清單內！目前的待辦清單', ephemeral = True, embed = tmp[1], view = tmp[0])

class edit_Modal(Modal):
    def __init__(self):
        super().__init__(title = '編輯事項狀態', timeout = 600)
    
    index = TextInput(label = '事項編號', style = TextStyle.short, max_length = '10', placeholder = '3', required = True)
    stats = TextInput(label = '狀態', style = TextStyle.short, max_length = '50', placeholder = '✅已完成', required = True)

    async def on_submit(self, interaction: Interaction):
        try:
            await edit_stats(user = interaction.user, index = self.index.value, stats = self.stats.value)
        except IndexError:
            return await interaction.response.send_message('❌你的待辦清單沒有那麼多項！', ephemeral=True)
        except TypeError:
            return await interaction.response.send_message('❌索引值必須是一個整數！', ephemeral=True)
        except TodoListNotAvailable:
            return await interaction.response.send_message('❌你還沒有創建一個待辦清單！', ephemeral=True)
        embed = await get_embed(client = interaction.client, title = '✅完成動作', desc = '**編輯待辦事項**')
        await interaction.message.edit(embed = embed)
        tmp = await get_page_turning_view(client = interaction.client, user = interaction.user)
        return await interaction.response.send_message(f'✅已將編號第`{int(self.index.value)}`個事項之狀態設為`{self.stats.value}`', embed = tmp[1],ephemeral=True, view = tmp[0])

class del_Modal(Modal):
    def __init__(self):
        super().__init__(title = '移除事項', timeout = 600)

    index = TextInput(label = '事項編號', style = TextStyle.short, max_length = '10', placeholder = '3', required = True)

    async def on_submit(self, interaction: Interaction):
        try:
            await del_item(user = interaction.user, index = self.index.value)
        except IndexError:
            return await interaction.response.send_message('❌你的待辦清單沒有那麼多項！', ephemeral=True)
        except TypeError:
            return await interaction.response.send_message('❌索引值必須是一個整數！', ephemeral=True)
        except TodoListNotAvailable:
            return await interaction.response.send_message('❌你還沒有創建一個待辦清單！', ephemeral=True)
        embed = await get_embed(client = interaction.client, title = '✅完成動作', desc = '**移除待辦事項**')
        await interaction.message.edit(embed = embed)
        tmp = await get_page_turning_view(client = interaction.client, user = interaction.user)
        return await interaction.response.send_message(f'✅已將編號第`{int(self.index.value)}`個事項移除', embed = tmp[1], ephemeral=True, view = tmp[0])

class todolist_edit(View):
    def __init__(self):
        super().__init__(timeout = 600)

    async def on_timeout(self):
        try:
            self.clear_items()
        except:
            pass
    
    @button(label = '新增待辦事項', emoji = '❔', style = ButtonStyle.blurple)
    async def append_callback(self, interaction:Interaction, button:Button):
        return await interaction.response.send_modal(append_Modal())

    @button(label = '查看待辦清單', emoji = '📝', style = ButtonStyle.blurple)
    async def output_list_callback(self, interaction:Interaction, button:Button):
        tmp = await get_page_turning_view(client = interaction.client, user = interaction.user)
        return await interaction.response.send_message(embed = tmp[1], ephemeral = True, view = tmp[0])

    @button(label = '編輯事項狀態', emoji = '⌨️', style = ButtonStyle.green, row =1)
    async def edit_callback(self, interaction:Interaction, button:Button):
        return await interaction.response.send_modal(edit_Modal())
    
    @button(label = '移除事項', emoji = '🚮', style = ButtonStyle.danger, row = 1)
    async def del_callback(self, interaction:Interaction, button:Button):
        return await interaction.response.send_modal(del_Modal())


async def output_list(client:Client, user:Union[discord.User, discord.Member]):
    with open('to_do_list.json', 'r') as file:
        data = json.load(file)

    user_todo_data = 0
    for todo in data['todo']:
        if todo['user_id'] == user.id:
            user_todo_data = todo
            break
    if user_todo_data != 0:
        embed = await get_embed(client = client, title = f'{user.display_name}的待辦事項')
        #Check length of to-do list, if length == 0 then return '✅沒有待辦事項'
        for x,i in enumerate(user_todo_data['list']):
            if x < min(len(user_todo_data['list']), 10):
                embed.add_field(name = f"事項編號：{x+1}\n事項狀態：{i['stats']}", value = f"📑📝**{i['content']}**", inline = False)
            else:
                break
        return embed
    else:
        return await get_embed(client = client, title = f'❌ | 你還沒新增待辦事項！', desc = f'利用`{pre}add_td [事項]`來新增選項，可直接輸入`{pre}add_td`或`{pre}td`來呼叫ui介面')

def append_to_do(data:str,stats:str, dc_user:Union[discord.User, discord.Member]):
    with open('to_do_list.json', 'r') as file:
        to_do = json.load(file)
        
    has_user = False
    idx = 0
    for i, user in enumerate(to_do['todo']):
        if user['user_id'] == dc_user.id:
            has_user = True
            idx = i
            break
    
    if has_user:
        to_do['todo'][idx]['list'].append({'content':data ,'stats':stats})
    else:
        to_do['todo'].append({'user_id':dc_user.id ,'list':[{'content':data ,'stats':stats}]})
    
    with open('to_do_list.json', 'w') as file:
        json.dump(to_do, file, indent = 4)


async def edit_stats(user:Union[discord.User,discord.Member], index, stats:str):
    try:
        index = int(index)
        index -= 1
    except:
        raise TypeError
        
    with open('to_do_list.json', 'r') as file:
        td = json.load(file)
    user_td_data = None
    for i,u in enumerate(td['todo']):
        if u['user_id'] == user.id:
            user_td_data = i
            break
    if user_td_data == None:
        raise TodoListNotAvailable()
    elif len(td['todo'][user_td_data]['list']) >= index+1:
        td['todo'][user_td_data]['list'][index]['stats'] = stats
    else:
        raise IndexError

    with open('to_do_list.json', 'w') as file:
        json.dump(td, file, indent = 4)


async def del_item(user:Union[discord.User,discord.Member], index):
    try:
        index = int(index)
        index -= 1
    except:
        raise TypeError
    
    with open('to_do_list.json', 'r') as file:
        td = json.load(file)
    user_td_data = None
    for i,u in enumerate(td['todo']):
        if u['user_id'] == user.id:
            user_td_data = i
            break
    if user_td_data == None:
        raise TodoListNotAvailable()
    elif len(td['todo'][user_td_data]['list']) >= index+1:
        td['todo'][user_td_data]['list'].pop(index)
    else:
        raise IndexError
    
    with open('to_do_list.json', 'w') as file:
        json.dump(td, file, indent = 4)


async def get_page_turning_view(client:Client, user:User):
    embed = await output_list(client = client, user = user)
    with open('to_do_list.json', 'r') as file:
        raw_data = json.load(file)
    for i in raw_data["todo"]:
        if i["user_id"] == user.id:
            user_data = i
            break
    data = []
    for x,i in enumerate(user_data["list"]):
        data.append(
            {
                "name":f"事項編號：{x+1}\n事項狀態：{i['stats']}", 
                "value":f"📑📝**{i['content']}**"
            }
    )
    v = PageTurningSys(data = data)
    tup = (v,embed)
    return tup