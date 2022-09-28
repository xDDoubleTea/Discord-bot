from logging import exception
from optparse import Values
from attr import has
import discord
from discord.ext import commands
import random
import json
from bin.nick_cnl_msg_handling import *

from config.Mysql_info import MySqlDataBase
from bin.Latex_handling import Latex_render_for_dc, latex_msg_options
from config.bot_info import My_user_id
message_recieve = False

Me = 398444155132575756


class message(commands.Cog):
    def __init__(self, client):
        self.client:discord.Client = client

    async def latex_rendering(self,message:discord.Message):
        renderer = Latex_render_for_dc()
        img = await renderer.Latex_dvipng(string = message.content)
        if img != None:
            msg = await message.reply(file = img, mention_author = False)
            return await msg.edit(view = latex_msg_options(attached_msg = msg, latex_data=message.content))
        else:
            msg = await message.reply(mention_author = False, content = 'Falied to render! Please check if the input has any possible error!')
            await msg.edit(view = await renderer.fail_rendering(msg = msg))
            return await msg.add_reaction('❗')

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        global message_recieve
        ctx = message.content
        if message.author == self.client.user:
            return 
        

        elif self.client.user.mentioned_in(message) and ctx.endswith('婆'):
            if message.author.id == 398444155132575756:
                return await message.channel.send('❤️')
                    
        elif ctx.startswith('=='):
            return await message.channel.send('!=')
        
        elif len(message.mentions) > 0:
            has_me = False
            for mention in message.mentions:
                if mention == self.client.get_user(My_user_id):
                    has_me = True
                    break
            me = self.client.get_user(My_user_id)
            my_stats = me.mutual_guilds[0].get_member(My_user_id).status.name
            if has_me and my_stats == 'offline':
                return await message.reply('您撥的電話無人接聽，請稍後再撥', mention_author = False)
            else:
                pass
        
        elif ctx.startswith('台中市立文華高級中學是一所積極新創、學科齊全、學術實力雄厚、辦學特色鮮明，在國際上具有重要影響力與競爭力的綜合性高中，在多個學術領域具有非常前瞻的科技實力，擁有世界一流的實驗室與師資力量，各種排名均位於全球前列。歡迎大家報考台中市立文華高中。'):
            return await message.delete()

        elif (ctx.startswith('$') and ctx.endswith('$')) or (ctx.startswith('```latex') and ctx.endswith('```')):
            if ctx.startswith('```latex'):
                message.content = message.content[8:]
                message.content = message.content[:-3]
            with open('nick_channel.json', 'r') as file:
                data = json.load(file)
            has_guild = False
            guild_nick_channel_id = 0
            for channel in data["channels"]:
                if channel["guild_id"] == message.guild.id:
                    has_guild = True
                    guild_nick_channel_id = channel["channel_id"]
            
            if has_guild and message.channel.id == guild_nick_channel_id:
                await message.delete()
                return await self.latex_rendering(message = message)
            else:
                return await self.latex_rendering(message = message)   


        else:
            if message.guild != None:
                with open("nick_channel.json", 'r') as file:
                    data = json.load(file)
                in_cnl = False
                for cnl in data["channels"]:
                    if message.channel.id == cnl["channel_id"]:
                        in_cnl = True
                        break
                if in_cnl:
                    handler = nick_channel_msg_handling(main = self)
                    await message.delete()
                    return await handler.send_message(message = message, content = message.content)

            if message_recieve:
                if message.guild != None:
                    if message.guild.id == 910150769624358914:
                        me = self.client.get_user(Me)
                        msg = 0
                        if len(message.stickers) != 0:
                            msg = await me.send(f'{message.author.display_name} 在 {message.channel.name}中說 ： \n{message.content}並傳送了貼圖:{message.stickers[0].url}')
                        else:
                            msg = await me.send(f'{message.author.display_name} 在 {message.channel.name}中說 ： \n{message.content}')
                        if len(message.attachments)>0:
                            for i in message.attachments:
                                file = await i.to_file()
                                return await msg.add_files(file)

                        if len(message.embeds)>0:
                            return await msg.edit(embeds=message.embeds)

    '''
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.channel.id == 910383297123713034:
    '''
    @commands.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        has_msg = False
        cnl = before.channel
        get_msg = discord.Message
        with open('latex_tmp.json', 'r') as file:
            data = json.load(file)
        for msg in data["messages"]:
            try:
                get_msg = await cnl.fetch_message(msg["message_id"])
                if get_msg.reference.message_id == before.id:
                    has_msg = True
                    break
            except:
                pass

        if has_msg:
            async with cnl.typing():
                renderer = Latex_render_for_dc()
                if after.content.startswith('a!latex'):
                    after.content = after.content[8:]
                elif after.content.startswith('```latex'):
                    after.content = after.content[8:]
                    after.content = after.content[:3]
                else:
                    pass
                img = await renderer.Latex_dvipng(string = after.content)
                if img != None:
                    msg = await get_msg.edit(content = None, attachments = [img])
                    if len(msg.reactions) >0:
                        await get_msg.clear_reactions()
                    return await msg.edit(view = latex_msg_options(attached_msg = msg, latex_data=after.content))
                else:
                    msg = await get_msg.edit(content = 'Falied to render! Please check if the input has any possible error!')
                    if len(get_msg.attachments)>0:
                        await msg.edit(attachments=[])

                    await msg.edit(view = await renderer.fail_rendering(msg = after))
                    return await msg.add_reaction('❗')

        

    @commands.command(name='toggle_message_recieve',aliases=['tmr'])
    @commands.dm_only()
    async def toggle_message_recieve(self, ctx):
        global message_recieve
        if ctx.message.author.id == Me:
            if message_recieve:
                message_recieve = False
            else:
                message_recieve = True
            
            await ctx.message.author.send(f'Message recieving is now {message_recieve}')
            

    @commands.command(name='set_welcome_message', aliases = ['set_wm'])
    async def set_welcome_message(self, ctx, channel_id, *, message):
        sql = 'SELECT * FROM welcome_channel'
        mydb = MySqlDataBase()
        wel_channel_info = mydb.get_db_data(sql_cmd = sql)
        has_guild = False
        for x in wel_channel_info:
            if str(ctx.guild.id) == x[0]:
                has_guild = True
                break
        
        if has_guild:
            sql = 'DELETE FROM welcome_channel WHERE guild_id = %s'
            val = (str(ctx.guild.id),)
            mydb = MySqlDataBase()
            mydb.del_data(sql_cmd = sql, values = val)
            sql = 'INSERT INTO welcome_channel(guild_id, welcome_channel_id, welcome_msg) VALUES (%s, %s, %s)'
            val = (str(ctx.guild.id), str(channel_id), str(message))
            mydb.insert_data(sql_cmd = sql, values = val)
            await ctx.channel.send('Welcome channel set!')
        else:
            sql = 'INSERT INTO welcome_channel (guild_id, welcome_channel_id, welcome_msg) VALUES (%s, %s, %s)'
            val = (str(ctx.guild.id), str(channel_id), str(message))
            mydb.insert_data(sql_cmd = sql, values = val)
            await ctx.channel.send('Welcome channel set!')


async def setup(client):
    await client.add_cog(message(client))