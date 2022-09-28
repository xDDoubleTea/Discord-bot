import discord
from discord.ext import commands
from discord import ButtonStyle, Interaction, Message, TextChannel
from discord.ui import Button , View, Modal, button
import json
import random
from bin.nick_cnl_msg_handling import nick_channel_msg_handling
from config.bot_info import *
from discord.ext.commands import Context

Me = My_user_id



class nick_channel(commands.Cog):
    def __init__(self, client):
        self.client:discord.Client = client
    
    async def generate_nick(self):
        with open('nicks.json', 'r') as file:
            nicks = json.load(file)
        no_nick = False
        indivisual_bool = [i for i in range(len(nicks["nicks"]))]
        while not no_nick:
            nickname = random.randint(1000,9999)
            for i,x in enumerate(nicks["nicks"]):
                if nickname == x["nickname"]:
                    indivisual_bool[i] = True
                else:
                    indivisual_bool[i] = False
            all_False = True
            for i in range(len(indivisual_bool)):
                if i < len(indivisual_bool)-1:
                    if indivisual_bool[i] != indivisual_bool[i+1]:
                        no_nick = False
                        all_False = False
                else:
                    if indivisual_bool[i-1] != indivisual_bool[i]:
                        no_nick = False
                        all_False = False
            if all_False:
                no_nick = True
                nick_name = nickname
        return nickname
    

    @commands.command(name = 'set_nick_channel')
    @commands.has_guild_permissions(administrator = True)
    async def set_nick_channel(self, ctx:Context, channel_id:int = -1):
        if channel_id == -1:
            channel_id = ctx.channel.id
        with open('nick_channel.json', 'r') as file:
            data = json.load(file)
        
        channels:list = data["channels"]
        channels.append({"guild_id":ctx.guild.id ,"channel_id":channel_id})
        
        with open('nick_channel.json', 'w') as file:
            json.dump(data, file, indent = 4)

        await ctx.channel.send(f'Nick channel has been set to {self.client.get_channel(channel_id).mention}')

    @commands.command(name = 'nick_cnl_send', aliases=['ncs'])
    @commands.dm_only()
    async def nick_cnl_send(self, ctx:Context, *,content = '\n'):
        handler = nick_channel_msg_handling(main = self)
        return await handler.send_message(message = ctx.message, content = content)

    
    @commands.command(name = 'nick_set', aliases = ['ns'])
    @commands.dm_only()        
    async def nick_set(self, ctx:Context, nick_name = '\n'):
        guild_id = 910150769624358914
        with open('nicks.json', 'r') as file:
            nicks = json.load(file)
        
        has_nickname = False
        for nick in nicks["nicks"]:
            if nick["nickname"] == nick_name:
                has_nickname = True
                break
        
        if has_nickname:
            await ctx.message.channel.send('Nick name has already been used! Try another nickname!')
        else:
            has_user = False
            user_data = 0 
            for user in nicks["nicks"]:
                if user["user_id"] == ctx.message.author.id:
                    has_user = True
                    user_data = user
                    break

            if has_user:
                if nick_name != '\n':
                    nicks["nicks"].remove(user_data)
                    user_data = {"guild_id":guild_id, "user_id":ctx.message.author.id, "nickname":nick_name}
                    nicks["nicks"].append(user_data)
                elif nick_name == '\n':
                    nicks["nicks"].remove(user_data)
                    nickname = await self.generate_nick()
                    nicks["nicks"].append({"guild_id":guild_id, "user_id":ctx.message.author.id, "nickname":nickname})
                    nick_name = nickname
                await ctx.message.channel.send(f"Your nick name has been set to {nick_name}")
            else:
                if nick_name != '\n':
                    user_data = {"guild_id":guild_id, "user_id":ctx.message.author.id, "nickname":nick_name}
                    nicks["nicks"].append(user_data)
                elif nick_name == '\n':
                    nickname = await self.generate_nick()
                    nicks["nicks"].append({"guild_id":guild_id, "user_id":ctx.message.author.id, "nickname":nickname})
                    nick_name = nickname
                await ctx.message.channel.send(f"Your nick name has been set to {nick_name}")

            with open('nicks.json', 'w') as file:
                json.dump(nicks, file, indent = 4)
    
    @commands.command(name = 'nick_reveal', aliases = ['nick_rev'])
    @commands.dm_only()
    async def nick_reveal(self, ctx:Context):
        global Me
        if ctx.message.author == self.client.get_user(Me):
            with open('nicks.json', 'r') as file:
                nicks = json.load(file)

            desc = ''
            for nick in nicks["nicks"]:
                if self.client.get_user(int(nick["user_id"])) != None:
                    desc += f'{self.client.get_user(int(nick["user_id"])).name} : `{nick["nickname"]}`\n'
            embed = discord.Embed(
                title = 'Nicks',
                description=desc
            )
            return await ctx.message.channel.send(embed=embed)
        else:
            return
    
    @commands.command(name = 'nick_reply', aliases = ['n_rpl'])
    @commands.dm_only()
    async def nick_reply(self, ctx:Context, msg_id:int, *, content):
        channel_id = 910384305518297098
        nick_channel:TextChannel = self.client.get_channel(channel_id)
        rpl_msg = await nick_channel.fetch_message(msg_id)
        handler = nick_channel_msg_handling(main = self)
        await handler.reply_message(message = rpl_msg, content = content, user = ctx.author, org_msg=ctx.message)
        return await ctx.message.add_reaction('✅')

async def setup(client):
    await client.add_cog(nick_channel(client))