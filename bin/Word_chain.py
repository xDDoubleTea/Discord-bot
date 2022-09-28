from math import ceil
from typing import List, Tuple, Union
import discord
from discord import Interaction, Message
from discord.ext import commands
from discord.ui import Modal, Button, View, Select, button, select
import asyncio
first_words = [
'習慣',
'今年',
'希望',
'食物',
'廁所',
'容易',
'以後',
'參加',
'暑假',
'請問',
'房間',
'下雨',
'走路',
'科學',
'冰箱',
'上午',
'小心',
'杯子',
'介紹',
'汽水',
'足球'
]

class word_chain(View):
    def __init__(self, message:Message, words:list,  players:list, now_page:int = 1,totalPages:int = 1, now_player:int = 0):
        super().__init__(timeout = 600)
        self.message:Message = message
        self.words:List[Tuple[Union[discord.User,discord.ClientUser],str]] = words
        self.now_page:int = now_page
        self.totalPages:int = totalPages
        self.players:List[discord.User] = players
        self.now_player:int = now_player
        self.inputting = False
    
    async def on_timeout(self):
        embed = self.message.embeds[0]
        embed.title += '(遊戲已結束)'
        await self.message.edit(embed = embed, view = None)
        return await self.message.reply('閒置過久！遊戲自動結束。')


    async def game_embed_update(self, word:str, user:discord.User):
        embed = self.message.embeds[0]
        if int(ceil(len(self.words)/10)) <= self.now_page:
            embed.add_field(name = f'{user.display_name}', value = word, inline = False)
            if len(self.players) -1 > self.now_player:
                self.now_player += 1
            else:
                self.now_player = 0
            embed = embed.to_dict()
            embed['title'] = f'現在是{self.players[self.now_player].display_name}的回合ouo'
            embed = discord.Embed.from_dict(embed)
        else:
            if len(self.players) -1 >= self.now_player:
                self.now_player += 1
            else:
                self.now_player = 0
            self.now_page += 1
            self.totalPages = int(ceil(len(self.words)/10))
            embed.clear_fields()
            embed.add_field(name = f'{user.display_name}', value = word, inline = False)
            embed = embed.to_dict()
            embed['footer']['text'] = f'第{self.now_page}/{self.totalPages}頁'
            embed['title'] = f'現在是{self.players[self.now_player].name}的回合ouo'
            embed = discord.Embed.from_dict(embed)
        return await self.message.edit(embed = embed)

    async def turn_page(self):
        embed = self.message.embeds[0]
        gnd = 0
        if len(self.words) < 10:
            pass
        else:
            gnd = 10*(self.now_page - 1)
            if len(self.words) - gnd >= 10:
                lim = int(gnd+10)
            else:
                lim = len(self.words)
            embed.clear_fields()
            for i in range(gnd, lim):
                embed.add_field(name = self.words[i][0].display_name, value = self.words[i][0], inline = False)
            embed = embed.to_dict()
            embed['footer']['text']= f'第{self.now_page}/{self.totalPages}頁'
            embed = discord.Embed.from_dict(embed)

        return embed

    async def is_valid_input(self, new_word:str):
        if new_word[0] == self.words[len(self.words)-1][1][len(self.words[len(self.words)-1][1])-1]:
            self.words.append((self.players[self.now_player], new_word))
            return True
        else:
            return False


    @button(label = '輸入回答ouo', emoji = '⌨️', style = discord.ButtonStyle.blurple)
    async def input_callback(self, interaction:Interaction, button:Button):
        if interaction.user == self.players[self.now_player]:
            self.inputting = True
            return await interaction.response.send_modal(input_Modal(self))
        else:
            has_user = False
            for user in self.players:
                if interaction.user == user:
                    has_user = True
                    break
            if has_user:
                return await interaction.response.send_message('現在不是你的回合!', ephemeral=True)
            else:
                return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)
    

    @button(label = '上一頁', style = discord.ButtonStyle.blurple, emoji = '◀️', row = 1)
    async def pre_callback(self, interaction:Interaction, button:Button):
        if not self.inputting:
            page = int(self.message.embeds[0].footer.text.split('/')[0][1])
            if page > 1:
                page -= 1
            else:
                pass
            self.now_page = page
            await interaction.message.edit(view = self)
            return await interaction.response.edit_message(embed = await self.turn_page())
        else:
            return await interaction.response.send_message('有人正在輸入!', ephemeral = True)
         

    @button(label = '下一頁', style = discord.ButtonStyle.blurple, emoji = '▶️',row = 1)
    async def next_callback(self, interaction:Interaction, button:Button):
        if not self.inputting:
            page = int(self.message.embeds[0].footer.text.split('/')[0][1])
            if page < self.totalPages:
                page += 1
            else:
                pass
            self.now_page = page
            await interaction.message.edit(view = self)
            return await interaction.response.edit_message(embed = await self.turn_page())
        else:
            return await interaction.response.send_message('有人正在輸入!', ephemeral = True)

    @button(label = '重新傳送訊息', style = discord.ButtonStyle.green, emoji = '↪️', row = 2)
    async def resend_callback(self, interaction:Interaction, button:Button):
        if not self.inputting:
            await interaction.message.delete()
            new_msg = await interaction.message.channel.send(embed = interaction.message.embeds[0])
            return await new_msg.edit(view = word_chain(message = new_msg, words = self.words, players = self.players, now_page = self.now_page, totalPages = self.totalPages, now_player = self.now_player))
        else:
            return await interaction.response.send_message('有人正在輸入!', ephemeral = True)

    @button(label = '停止遊戲', style = discord.ButtonStyle.red, emoji='⏹️')
    async def stop_callback(self,interaction:Interaction, button:Button):
        has_user = False
        for user in self.players:
            if interaction.user == user:
                has_user = True
                break
        if has_user:
            await interaction.message.edit(view = None)
            return await interaction.response.send_message(f'{interaction.user}強制結束了遊戲!')
        else:
            return await interaction.response.send_message('你不在遊戲中!',ephemeral=True)

    

class input_Modal(Modal):
    text_column = discord.ui.TextInput(label = '輸入區', style=discord.TextStyle.short, placeholder='神奇海螺')
    def __init__(self, main:word_chain):
        super().__init__(title = '輸入回答ouo', timeout = None)
        self.main = main
    
    async def on_submit(self, interaction: Interaction) -> None:
        if await self.main.is_valid_input(new_word = self.text_column.value):
            await interaction.response.defer()
            self.main.inputting = False
            return await self.main.game_embed_update(word = self.text_column.value, user = interaction.user)
        else:
            return await interaction.response.send_message('你沒有遵守規則！ouo', ephemeral=True)