import discord
import asyncio
import os
import youtube_dl

import urllib.parse, urllib.request, re
import requests

from discord.ext import commands
from discord import Embed, FFmpegPCMAudio
from discord.utils import get
from discord.ui import Button, View
import mysql.connector






class leave(discord.ui.Button):
    async def callback(self, interaction):
        await interaction.response.defer()
        if interaction.guild.voice_client != None:
            if interaction.guild.voice_client.channel == interaction.user.voice.channel:
                await interaction.guild.voice_client.disconnect()
                await interaction.channel.send('Left the voice channel!')





class music(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        Kanatadb = mysql.connector.connect(
            host='localhost',
            database='kanata',
            password='ImSingleDog1',
            user='root'
            )
        if not member.bot:
            if before.channel == None:
                if after.channel == None:
                    #no way that this happenes
                    return
                else:
                    #user joined a channel
                    #see if it's a dynamic channel
                    cursor = Kanatadb.cursor()
                    sql = 'SELECT * FROM custom_channel'
                    cursor.execute(sql)
                    channel_info = cursor.fetchall()
                    has_channel = False
                    for x in channel_info:
                        if x[1] == str(after.channel.id):
                            has_channel = True
                            break
                    if has_channel:
                        #it's a dynamic channel
                        #create new voice channel and move member into it
                        new_vc = await after.channel.clone(name = f"{member.name}'s small room")
                        await new_vc.edit(user_limit = None)
                        cursor = Kanatadb.cursor()
                        sql = 'SELECT * FROM new_channel'
                        cursor.execute(sql)
                        new = cursor.fetchall()
                        sql = 'INSERT INTO new_channel (new_channel_index, new_channel_id) VALUES (%s, %s)'
                        val = (str(len(new)),str(new_vc.id))
                        cursor.execute(sql, val)
                        Kanatadb.commit()
                        await member.move_to(new_vc)


            else:
                #user is from another channel
                if after.channel == None:
                    #user is not in any voice channel
                    #see if before channel was one of the new channels
                    cursor = Kanatadb.cursor()
                    sql = 'SELECT * FROM new_channel'
                    cursor.execute(sql)
                    new_channel = cursor.fetchall()
                    was_new = False
                    for x in new_channel:
                        if x[1] == str(before.channel.id):
                            was_new = True
                            break
                    if was_new:
                        #if all members was disconnected from before channel then delete
                        if len(before.channel.members) >0:
                            return
                        else:
                            #delete the new channel
                            await before.channel.delete()
                            cursor = Kanatadb.cursor()
                            sql = 'DELETE FROM new_channel WHERE new_channel_id = %s'
                            val = (str(before.channel.id),)
                            cursor.execute(sql, val)
                            Kanatadb.commit()
                else:
                    #user connects to another channel
                    #check if after is dynamic
                    cursor = Kanatadb.cursor()
                    sql = 'SELECT * FROM custom_channel'
                    cursor.execute(sql)
                    channel_info = cursor.fetchall()
                    has_channel = False
                    for x in channel_info:
                        if x[1] == str(after.channel.id):
                            has_channel = True
                            break                
                    if has_channel:
                        #it's dynamic
                        #see if before channel is new channel, if yes then delete and create another one
                        cursor = Kanatadb.cursor()
                        sql = 'SELECT * FROM new_channel'
                        cursor.execute(sql)
                        new_channel = cursor.fetchall()
                        was_new = False
                        for x in new_channel:
                            if x[1] == str(before.channel.id):
                                was_new = True
                                break
                            
                        if was_new:
                            #move back to before channel
                            await member.move_to(before.channel)
                        else:
                            #not new but its dynamic so create a new voice
                            #create new voice channel and move member into it
                            new_vc = await after.channel.clone(name = f"{member.name}'s small room")
                            await new_vc.edit(user_limit = None)
                            cursor = Kanatadb.cursor()
                            sql = 'SELECT * FROM new_channel'
                            cursor.execute(sql)
                            new = cursor.fetchall()
                            sql = 'INSERT INTO new_channel (new_channel_index, new_channel_id) VALUES (%s, %s)'
                            val = (str(len(new)),str(new_vc.id))
                            cursor.execute(sql, val)
                            Kanatadb.commit()
                            await member.move_to(new_vc)
                    else:
                        #not dynamic
                        #see if before channel is new channel, if yes then delete
                        cursor = Kanatadb.cursor()
                        sql = 'SELECT * FROM new_channel'
                        cursor.execute(sql)
                        new_channel = cursor.fetchall()
                        was_new = False
                        for x in new_channel:
                            if x[1] == str(before.channel.id):
                                was_new = True
                                break
                        if was_new:
                            #see if all members was disconnected
                            if len(before.channel.members)>0:
                                return
                            else:
                                #delete the new channel
                                await before.channel.delete()
                                cursor = Kanatadb.cursor()
                                sql = 'DELETE FROM new_channel WHERE new_channel_id = %s'
                                val = (str(before.channel.id),)
                                cursor.execute(sql, val)
                                Kanatadb.commit()
                        else:
                            #not new not dynamic
                            return
        else:
            return



    @commands.command(name='join',aliases=['connect'])
    async def join(self, ctx):
        if ctx.message.author.voice:
            await ctx.message.author.voice.channel.connect(self_deaf = True)
            async with ctx.channel.typing():
                v = View(timeout = 180)
                leavebtn = leave(
                    style=discord.ButtonStyle.red,
                    label='Disconnect',
                    emoji='⏹️'
                )
                v.add_item(leavebtn)
                msg = await ctx.message.channel.send(f'Voice connected! by{ctx.message.author.mention}',view = v)
                await msg.add_reaction('✅')
        else:
            msg = await ctx.message.channel.send(f"You're not connected to a Voice channel!{ctx.message.author.mention}")
            await msg.add_reaction('❌')
            

    @commands.command(name='leave',aliases=['dc'])
    async def leave(self, ctx):
        if ctx.message.guild.voice_client != None:
            await ctx.message.guild.voice_client.disconnect()
            msg = await ctx.message.channel.send(f'{ctx.message.author.mention} made left the voice channel')
            await msg.add_reaction('👋')
        else:
            await ctx.message.channel.send("I'm not in a voice channel!")


    @commands.command(name='set_channel',aliases=['set_ch'])
    async def set_channel(self, ctx, vc_id):
        Kanatadb = mysql.connector.connect(
        host='localhost',
        database='kanata',
        password='ImSingleDog1',
        user='root'
        )
        cursor = Kanatadb.cursor()
        sql = 'SELECT * FROM custom_channel'
        cursor.execute(sql)
        channel_data = cursor.fetchall()

        index = 0
        has_guild = False
        if len(channel_data)>0:
            for i,x in enumerate(channel_data):
                if x[0] == str(ctx.guild.id):
                    has_guild = True
                    index = i
                    break

        v_channel = self.client.get_channel(int(vc_id))
        if has_guild:
            if str(vc_id) == channel_data[index][1]:
                await ctx.message.channel.send(f'`{v_channel.name}`已加入動態語音頻道中!你想要更改嗎?')
            elif str(vc_id) != channel_data[index][1]:
                cursor = Kanatadb.cursor()
                sql = "DELETE FROM custom_channel WHERE guild_id = %s"
                val = (str(ctx.guild.id), )
                cursor.execute(sql, val)
                Kanatadb.commit()
                sql = 'INSERT INTO custom_channel (guild_id, guild_channel_id) VALUES (%s, %s)'
                val = (str(ctx.guild.id), vc_id)
                cursor.execute(sql, val)
                Kanatadb.commit()
                await ctx.message.channel.send(f'已將`{v_channel.name}`加入動態語音頻道中!')
        else:
            cursor = Kanatadb.cursor()
            sql = 'INSERT INTO custom_channel (guild_id, guild_channel_id) VALUES (%s, %s)'
            val = (str(ctx.guild.id), vc_id)
            cursor.execute(sql, val)
            Kanatadb.commit()
            await ctx.message.channel.send(f'已將`{v_channel.name}`加入動態語音頻道中!')

    @commands.command(name='delete_channel', aliases=['del_ch'])
    async def delete_channel(self, ctx, vc_id):
        Kanatadb = mysql.connector.connect(
            host='localhost',
            database='kanata',
            password='ImSingleDog1',
            user='root'
        )
        cursor = Kanatadb.cursor()
        sql = 'SELECT * FROM custom_channel'
        cursor.execute(sql)
        channel_data = cursor.fetchall()        
        index = 0
        has_guild = False
        if len(channel_data)>0:
            for i,x in enumerate(channel_data):
                if x[0] == str(ctx.guild.id):
                    has_guild = True
                    index = i
                    break
        
        v_channel = self.client.get_channel(int(vc_id))
        if has_guild:
            cursor = Kanatadb.cursor()
            sql = "DELETE FROM custom_channel WHERE guild_id = %s"
            val = (str(ctx.guild.id), )
            cursor.execute(sql, val)
            Kanatadb.commit()
            await ctx.message.channel.send(f'已將`{v_channel.name}`移出動態語音頻道資料庫!')        
        else:
            await ctx.message.channel.send(f'這個伺服器還未設置動態語音頻道!')


async def setup(client):
    await client.add_cog(music(client))
