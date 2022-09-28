from typing import List
import discord
from discord import Interaction
from discord.ext import commands
from discord.ext.commands import Context
from discord.ui import Modal, Button, View, Select, button, select
from bin.Word_chain import word_chain, first_words
from config.bot_info import *
import random
import asyncio

class TicTacToe:
    class gamedata:
        def __init__(self, players:list,now_game:list,now_player:int, game_win:int):
            self.players = players
            self.now_game = now_game
            self.now_player = now_player
            self.game_win = game_win
            #game_win is the state of the game, 0 for no winner, 1 for circle win, 2 for cross win
    
    def __init__(self, message:discord.Message, client:discord.Client, players:list):
        self.message = message
        self.client = client
        self.now_player = 0
        self.players = players
        self.now_game:List[self.gamedata] = [[0 for j in range(3)] for i in range(3)]
        self.game_win = 0

class tic_tac_toe_buttons(View):
    def __init__(self, main:TicTacToe):
        super().__init__(timeout=None)
        self.main = main

    async def to_embed(self, msg: discord.Message):
        raw_embed = discord.Embed.to_dict(msg.embeds[0])
        emoji = ' '
        if self.main.now_player == 0:
            emoji = '⭕'
        else:
            emoji = '❎'
        raw_embed['title'] = f'遊戲結束!'
        raw_embed['description'] = f'獲勝玩家:({emoji}){self.main.players[self.main.now_player]}'
        raw_embed['color'] = discord.Colour.green().value
        return discord.Embed.from_dict(raw_embed)

    async def if_win(self, msg:discord.Message):
        ng = self.main.now_game
        won = False
        draw = False
        # 橫向
        if (ng[0][0] != 0 and ng[0][1] != 0 and ng[0][2] != 0):
            if (ng[0][0] == ng[0][1] and ng[0][1] == ng[0][2]):
                won = True
        elif (ng[1][0] != 0 and ng[1][1] != 0 and ng[1][2] != 0):
            if (ng[1][0] == ng[1][1] and ng[1][1] == ng[1][2]):
                won = True
        elif (ng[2][0] != 0 and ng[2][1] != 0 and ng[2][2] != 0):
            if (ng[2][0] == ng[2][1] and ng[2][1] == ng[2][2]):
                won = True

        # 縱向
        if (ng[0][0] != 0 and ng[1][0] != 0 and ng[2][0] != 0):
            if (ng[0][0] == ng[1][0] and ng[1][0] == ng[2][0]):
                won = True
        elif (ng[0][1] != 0 and ng[1][1] != 0 and ng[2][1] != 0):
            if (ng[0][1] == ng[1][1] and ng[1][1] == ng[2][1]):
                won = True
        elif (ng[0][2] != 0 and ng[1][2] != 0 and ng[2][2] != 0):
            if (ng[0][2] == ng[1][2] and ng[1][2] == ng[2][2]):
                won = True

        # 斜角
        if (ng[0][0] != 0 and ng[1][1] != 0 and ng[2][2] != 0):
            if (ng[0][0] == ng[1][1] and ng[1][1] == ng[2][2]):
                won = True
        elif (ng[0][2] != 0 and ng[1][1] != 0 and ng[2][0] != 0):
            if (ng[0][2] == ng[1][1] and ng[1][1] == ng[2][0]):
                won = True
        if not won:
            # 是否平手
            all_true = []
            for i in range(3):
                for j in range(3):
                    if (not won) and ng[i][j]!=0:
                        all_true.append(1)
                    else:
                        all_true.append(0)

            won = True
            draw = True
            for i in all_true:
                if i == 0:
                    won = False
                    draw = False
            
        if won:
            if not draw:
                if self.main.now_player == 0:
                    who_won = 1
                elif self.main.now_player == 1:
                    who_won = 2
            else:
                who_won = 3
            self.now_game = [[0 for j in range(3)] for i in range(3)]
            for i in self.children:
                i.disabled = True
            await msg.edit(view = self)
            return who_won

    async def displaying(self, msg:discord.Message, button:Button):
        #0 for circle player, 1 for cross player
        row = int(button.custom_id.split(', ')[0])
        col = int(button.custom_id.split(', ')[1])
        button.disabled = True
        if self.main.now_player == 0:
            button.emoji = '⭕'
            button.style = discord.ButtonStyle.green
            self.main.now_game[row][col] = 1

        else:
            button.emoji = '❎'
            button.style = discord.ButtonStyle.red
            self.main.now_game[row][col] = 2
        
        return await msg.edit(view = self)

    async def whose_turn_embed(self, msg:discord.Message):
        raw_embed = discord.Embed.to_dict(msg.embeds[0])
        emoji = ' '
        if self.main.now_player == 0:
            emoji = '⭕'
        else:
            emoji = '❎'
        raw_embed['title'] = f'{emoji} | 現在是{self.main.players[self.main.now_player].name}的回合'
        return discord.Embed.from_dict(raw_embed)

    async def all_callback(self, interaction:Interaction, button:Button):
        if interaction.user == self.main.players[self.main.now_player]:
            await self.displaying(interaction.message, button)
            if await self.if_win(msg = interaction.message) == 1 or await self.if_win(msg = interaction.message) == 2:
                return await interaction.response.send_message(view = GameSelect(client = self.main.client, players = []), embed = await self.to_embed(msg = interaction.message))
            elif await self.if_win(msg = interaction.message) == 3:
                raw_embed = discord.Embed.to_dict(interaction.message.embeds[0])
                raw_embed['title'] = '遊戲結束!'
                raw_embed['description'] = f'平手!'
                raw_embed['color'] = discord.Colour.yellow().value
                embed = discord.Embed.from_dict(raw_embed)
                return await interaction.response.send_message(view = GameSelect(client = self.main.client, players = []), embed = embed)
            else:
                if self.main.now_player == 0:
                    self.main.now_player = 1
                else:
                    self.main.now_player = 0
                return await interaction.response.edit_message(embed = await self.whose_turn_embed(msg = interaction.message),view = self)
        else:
            return await interaction.response.send_message('現在不是你的回合', ephemeral=True)

    def has_user(self, interaction:discord.Interaction):
        has_user = False
        for user in self.main.players:
            if interaction.user == user:
                has_user = True
                break
        return has_user

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '0, 0', row = 0)
    async def zero_zero_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '0, 1', row = 0)
    async def zero_one_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '0, 2', row = 0)
    async def zero_two_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '1, 0', row = 1)
    async def one_zero_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '1, 1', row = 1)
    async def one_one_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)
    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '1, 2', row = 1)
    async def one_two_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '2, 0', row = 2)
    async def two_zero_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '2, 1', row = 2)
    async def two_one_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = None, emoji = '⏹️', style = discord.ButtonStyle.gray, disabled = False, custom_id = '2, 2', row = 2)
    async def two_two_callback(self, interaction, button:Button):
        if self.has_user(interaction = interaction):
            return await self.all_callback(interaction, button)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral=True)

    @button(label = '⛔結束遊戲', style = discord.ButtonStyle.red, disabled = False, row = 3)
    async def end_callback(self, interaction, button:Button):
        has_user = False
        for user in self.main.players:
            if interaction.user == user:
                has_user = True
                break
        
        if has_user:
            await interaction.message.edit(view = None)
            return await interaction.response.send_message(f'{interaction.user}強制結束了遊戲!')
        else:
            return await interaction.response.send_message(f'你不在遊戲中!', ephemeral= True)

class BlackJack:
    class gameOptions:
        def __init__(self, author:discord.User, client:discord.Client, players:list):
            self.author = author
            self.client = client
            self.players = players
    
    def __init__(self, cards:list, msg :discord.Message ):
        self.cards = cards
        self.msg = msg

class BlackJack_buttons(View):
    def __init__(self, main:BlackJack):
        super().__init__(timeout = None)
        self.main = main

class GameSelect(View):
    def __init__(self, client, players:list):
        super().__init__(timeout = None)
        self.players:List[discord.User] = players
        self.client:discord.Client = client


    @select(
        placeholder ='選擇遊戲', 
        options = [
            discord.SelectOption(label = 'Tic Tac Toe', description = '圈圈叉叉', emoji = '⭕',value = '⭕Tic Tac Toe'),
            discord.SelectOption(label = 'Black Jack', description = '21點', emoji = '♦️',value = '♦️Black Jack'),
            discord.SelectOption(label = 'Word Chain', description = '文字接龍', emoji = '🔁', value = '🔁Word Chain')
        ],
        custom_id='game_selection',
        min_values=1,
        max_values=1
    )
    async def game_callback(self, interaction:Interaction, select:Select):
        if select.custom_id == 'game_selection':
            await interaction.response.defer()
            select.disabled = True
            await interaction.message.edit(view = self)
            desc = f'玩家列表:\n還沒有玩家加入!'
            for i in self.players:
                desc += i

            embed = discord.Embed(
                title = f'遊戲{select.values[0]}',
                description = desc,
                color=discord.Colour.dark_red()
            )
            msg = await interaction.channel.send(embed = embed)
            joinGame_view = joinGame(selection = self, game = select.values[0], msg = msg)
            await msg.edit(view = joinGame_view)
    

class joinGame(View):
    def __init__(self, selection:GameSelect, game:str, msg:discord.Message):
        super().__init__(timeout = None)
        self.selection = selection
        self.game = game
        self.msg = msg

    async def to_embed(self, msg:discord.Message):
        embed_raw = msg.embeds[0].to_dict()
        embed_raw['description'] = '玩家列表:'
        for player in self.selection.players:
            embed_raw['description'] += f'\n{player.display_name}'
        if len(self.selection.players) == 0:
            embed_raw['description'] += '\n還沒有玩家加入!'
            embed_raw['color'] = discord.Colour.dark_red().value
        else:
            embed_raw['color'] = discord.Colour.blue().value
        return discord.Embed.from_dict(embed_raw)

    async def start_game(self, interaction:discord.Interaction):
        msg:discord.Message = interaction.message
        if self.game == '⭕Tic Tac Toe':
            if len(self.selection.players) == 2:
                await msg.delete()
                raw_embed = discord.Embed.to_dict(msg.embeds[0])
                raw_embed['title'] = f'⭕ | 現在是{self.selection.players[0].display_name}的回合'
                embed = discord.Embed.from_dict(raw_embed)
                return await msg.channel.send(
                    embed = embed, 
                    view = tic_tac_toe_buttons(
                        main = TicTacToe(
                            message=msg, 
                            client = self.selection.client, 
                            players = self.selection.players
                        )
                    )
                )
            elif len(self.selection.players) > 2:
                return await interaction.response.send_message('太多人了!', ephemeral= True)
            elif len(self.selection.players) < 2:
                return await interaction.response.send_message('太少人了!', ephemeral= True)
        elif self.game == '♦️Black Jack':
            return await interaction.response.send_message('此遊戲還在開發中!請耐心等候!', ephemeral= True)
        elif self.game == '🔁Word Chain':
            embed = discord.Embed(
                title = f'文字接龍Word Chain(由{self.selection.players[0].display_name}開始)',
                description = '有沒有合規定自由心證啦ouo',
                colour = discord.Colour.blue()
            )
            dev:discord.User = interaction.client.get_user(My_user_id)
            word = random.choice(first_words)
            embed.add_field(name = '電腦ouo', value = word)
            embed.set_author(name = f"{interaction.client.user}", icon_url=interaction.client.user.avatar.url)
            embed.set_footer(text = f"第1/1頁", icon_url=dev.avatar.url)
            await interaction.response.edit_message(view = None)
            msg = await interaction.message.channel.send(embed = embed)
            return await msg.edit(view = word_chain(message = msg, words = [(interaction.client.user, word)], players = self.selection.players))


    async def has_user(self, interaction:Interaction):
        has_user = False
        for i in self.selection.players:
            if i == interaction.user:
                has_user = True
                break
        return has_user


    @button(label = '✔️加入遊戲', style = discord.ButtonStyle.green, disabled = False)
    async def join_callback(self, interaction:Interaction, button:Button):
        if not await self.has_user(interaction = interaction):
            self.selection.players.append(interaction.user)
            return await interaction.response.edit_message(embed = await self.to_embed(msg = interaction.message), view = self)
        else:
            return await interaction.response.send_message(content = '你已經在遊戲中!', ephemeral= True)


    @button(label = '🔄️退出遊戲', style = discord.ButtonStyle.red, disabled = False)
    async def leave_callback(self, interaction:Interaction, button:Button):
        if await self.has_user(interaction = interaction):
            self.selection.players.remove(interaction.user)
            return await interaction.response.edit_message(embed = await self.to_embed(msg = interaction.message), view = self)
        else:
            return await interaction.response.send_message(content = '你不在遊戲中!', ephemeral= True)


    @button(label = '✅開始遊戲', style = discord.ButtonStyle.green, disabled = False, row = 1)
    async def start_callback(self, interaction:Interaction, button:Button):
        if await self.has_user(interaction = interaction):
            return await self.start_game(interaction = interaction)
        else:
            return await interaction.response.send_message('你不在遊戲內!', ephemeral= True)


    @button(label = '⛔結束遊戲', style = discord.ButtonStyle.red, disabled = False, row = 1)
    async def end_callback(self, interaction:Interaction, button:Button):
        if await self.has_user(interaction = interaction):
            await interaction.message.edit(view = None)
            return await interaction.response.send_message(f'{interaction.user}強制結束了遊戲!')
        else:
            return await interaction.response.send_message(f'你不在遊戲中!', ephemeral= True)


class games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'game')
    async def game(self, ctx:Context):
        return await ctx.send(view = GameSelect(client=self.client, players=[]))

async def setup(client):
    await client.add_cog(games(client))