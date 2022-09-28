from re import I
import re
import discord 
import random
from discord import Reaction, ButtonStyle, User, Interaction
from discord.ext import commands
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import emoji
import time
from pytube.__main__ import YouTube
from discord.ui import View, button, Modal, Button
import random
import os, psutil
import io
import chat_exporter
from discord.ext.commands import Context
from typing import List
from config.bot_info import *
  

Me = My_user_id


    

class choice(View):
    def __init__(self, user:User, client:discord.Client):
        super().__init__(timeout = None)
        self.user:User = user
        self.client:discord.Client = client


    @button(label = '確認', emoji = '✔️', style = ButtonStyle.green)
    async def confirm_callback(self, interaction:Interaction, button:Button):
        if interaction.user == self.user:
            return await interaction.response.send_modal(choice_Modal(client = self.client))
        else:
            return await interaction.response.send_message('這不是你能按的', ephemeral=True)
    
    @button(label = '取消', emoji = '❎', style = ButtonStyle.red)
    async def cancel_callback(self, interaction:Interaction, button:Button):
        if interaction.user == self.user:
            embed:discord.Embed = await get_embed(client = self.client, title = '已取消動作!')
            return await interaction.response.edit_message(embed = embed, view = None)

        else:
            return await interaction.response.send_message('這不是你能按的', ephemeral=True)


class choice_Modal(Modal):
    def __init__(self, client:discord.Client):
        super().__init__(title = '讓我來為你做決定吧!', timeout = None)
        self.client:discord.Client = client

    theme = discord.ui.TextInput(label = '主題', placeholder = '晚餐吃啥(可不填)', style = discord.TextStyle.short, custom_id = 'main',  required=False)
    choices = discord.ui.TextInput(label = '選項', placeholder = '屋馬\n海底撈(以換行區隔)', style = discord.TextStyle.long, custom_id = 'choices')
    
    async def output_embed(self, choices:list ,result:str, theme:str = None):
        for i,j in enumerate(choices):
            if i == len(choices)-1:
                pre = '__'
                pre += j
                pre += '__'
                j = pre
                choices[i] = j
            else:
                pre = '__'
                pre += j
                pre += '__、'
                j = pre
                choices[i] = j
        
        choices:str = "".join(choices)
        embed:discord.Embed = await get_embed(title = result, desc = f'從{choices}中選出：\n__{result}__\nouo', client = self.client)
        if theme != None:
            embed.set_author(name = theme, icon_url=self.client.user.avatar.url)
        return embed

    
    async def on_submit(self, interaction: Interaction):
        input_choices = self.choices.value.splitlines()
        if len(input_choices) < 2:
            return await interaction.response.send_message('太少選項了!', ephemeral=True)
        else:
            await interaction.response.defer()

            result = random.choice(input_choices)

            embed = await self.output_embed(theme = self.theme.value ,choices = input_choices, result = result)
            org = await interaction.channel.fetch_message(interaction.message.reference.message_id)
            await org.reply(embed = embed, mention_author = False)
            return await interaction.message.delete()
        

class rickroll(discord.ui.Button):
    async def callback(self, interaction):
        await interaction.message.edit(view=None)
        await interaction.response.defer()
        embed = discord.Embed(
            title = '神奇海螺',
            description='太酷了',
            url = 'https://youtu.be/DPUqYPVoQik?t=124',
            color = discord.Colour.blue()
        )
        await interaction.channel.send(embed=embed)


class others(commands.Cog):
    def __init__(self, client:discord.Client):
        self.client = client
    

    @commands.command(name = 'choice', aliases = ['choose', 'choices'])
    async def choice(self, ctx:Context, *,choices:str=' '):
        temp = choices.split()
        choice_view = choice(user = ctx.author, client = self.client)
        if len(temp) <= 1:
            embed = await get_embed(title = '太少選項了!', desc = '新增選項?', client = self.client)
            await ctx.message.reply(embed = embed, view = choice_view, mention_author = False)
        else:
            tmp = choice_Modal(client = self.client)
            embed = await tmp.output_embed(choices = temp, result=random.choice(choices.split()))
            await ctx.message.channel.send(embed = embed)


    @commands.command(name = 'help', aliases = ['hp', 'h'])
    async def help(self, ctx:Context):
        embed = await help_msg_embed(client = self.client)
        return await ctx.send(embed = embed)
    
    @commands.command(name='save_channel', aliases =['save_cnl'])
    async def save_channel(self, ctx:Context, channel_id = -1, limit:int = None):
        async with ctx.channel.typing():
            channel = discord.TextChannel
            if channel_id != -1:
                channel = self.client.get_channel(channel_id)

            if channel != None:
                pass
            else:
                channel = ctx.message.channel
            msg = await ctx.send('Processing...')
            transcript = await chat_exporter.export(channel, limit = limit)
            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"{channel.name}.html"
            )
            new_msg = await msg.reply('Done!')
            return await new_msg.edit(attachments=[transcript_file])

    @commands.command(name = 'Ram',aliases = ['ram'])
    async def Ram(self, ctx:Context):
        process = psutil.Process(os.getpid())
        embed = discord.Embed(
            title = 'RAM usage',
            description = f'The RAM usage is:`{(process.memory_info().rss)/(1024*1024)}`MB',
            color=discord.Colour.blue()
        )
        await ctx.channel.send(embed=embed)
    
    @commands.command(name='CPU',aliases=['cpu'])
    async def CPU(self, ctx:Context):
        embed = discord.Embed(
            title = 'CPU usage',
            description = '💤 | testing...',
            color=discord.Colour.blue()
        )
        msg = await ctx.channel.send(embed=embed)
        test_cpu = psutil.cpu_percent(2)
        if test_cpu > 70:
            desc = f'❗ | The CPU usage is:`{test_cpu}`%'
        else:
            desc = f'✅ | The CPU usage is:`{test_cpu}`%'
        embed = discord.Embed(
            title = 'CPU usage',
            description = desc,
            color=discord.Colour.blue()
        )
        await msg.edit(embed=embed)

    @commands.command(name='kowai', aliases=['kowa','ko'])
    async def kowai(self, ctx:Context, *, cool=0):
        if cool==0:
            cool = ''
        await ctx.message.reply('看看我掌握了你多少資訊')
        await ctx.channel.send(f'訊息ID=`{ctx.message.id}`, 訊息內容=`{cool}`, 訊息傳送者={ctx.message.author.mention}')
        await ctx.channel.send(f'觸發指令頻道= {ctx.message.channel.mention}, 觸發指令伺服器= {ctx.message.guild}, 觸發指令伺服器之人數= `{len(ctx.message.guild.members)}`')
        embed = discord.Embed(
            title = '我甚至還有你的頭像喔',
            description = '這是你的頭像',
            color = discord.Colour.blue(),
            url='https://youtu.be/ddrlucEtC5M?t=124'
        )
        embed.set_image(url = ctx.message.author.avatar.url)
        v=View(timeout=None)
        rick = rickroll(
            style=discord.ButtonStyle.red,
            label = '禁止點擊我',
            disabled=False
        )
        v.add_item(rick)
        await ctx.channel.send(embed=embed, view = v)
        await ctx.channel.send('很恐怖對吧?')


        #await ctx.send('目前此功能被下架')
        
    @commands.command(name='pick')
    async def pick(self, ctx:Context, *, dicestuff):
        percentage = abs((random.randint(0,100))*100-(random.randint(3,241)))%100
        yes = False
        reply='abc'
        zeroorone = (random.randint(0,1481))%2

        if zeroorone == 1:
            reply = f'我覺得好像`{percentage}%`是'
        elif zeroorone == 0:
            reply = f'我覺得好像`{percentage}%`不是'

        embed = discord.Embed(
            title = dicestuff,
            description=reply,
            color = discord.Colour.blue()
        )
        embed.set_footer(text = '免責聲明\n此結果皆為亂數生成，若有人當真並依此攻擊，本機器人作者一概不負責任。', icon_url = self.client.user.avatar.url)
        embed.set_author(name = f"{ctx.message.author}", icon_url = ctx.message.author.avatar.url)
        msg = await ctx.message.reply(embed=embed)
        await msg.add_reaction('❓')



    @commands.Cog.listener()
    async def on_reaction(self, reaction:Reaction, user):
        global _role
        print(reaction.emoji)
        if user != self.client.user:
            print(reaction.emoji)
            if str(reaction.emoji) == "1️⃣":
                t = time.localtime()
                today = date.today()
                today_date = today.strftime("%Y/%m/%d")
                current_time = time.strftime("%H:%M:%S", t)
        
                helpmenu= discord.Embed(
                    title = "Help menu",
                    description = "Click on this link to see list of commands",
                    url = "https://hackmd.io/@Kawaii-kanataso/ry_w9QXVK",
                    colour = discord.Color.blue()
                )
                helpmenu.set_author(name = f"{self.client.user}", icon_url = self.client.user.avatar.url)
                helpmenu.add_field(
                    name = "If you need any help you can message me on Discord" , 
                    value = f"{MyDiscordID}", 
                    inline = True)
                helpmenu.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.user.avatar.url)
                await reaction.message.channel.send(embed = helpmenu)
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
            if str(reaction.emoji) == "2️⃣":
                await reaction.message.channel.send("Enter a!play <url> to play a song.(Availiable source: Youtube)")
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
            if str(reaction.emoji) == "3️⃣":
                await reaction.message.channel.send("3")
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
            if str(reaction.emoji) == "4️⃣":
                await reaction.message.channel.send("4")
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
            if str(reaction.emoji) == "5️⃣":
                await reaction.message.channel.send("5")
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
            if str(reaction.emoji) == emoji.emojize(":raised_hand:"):
                print("a")
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
                await user.add_roles(_role)
            '''
            if str(reaction.emoji) == "▶️":
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
                try:
                    await MusicManager.resume(ctx=user)
                except:
                    return
            if str(reaction.emoji) == "⏸️":
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
                try:
                    await MusicManager.pause(ctx=user)
                except:
                    return
            if str(reaction.emoji) == "⏭️":
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
                try:
                    await MusicManager.skip(ctx=user)
                except:
                    return
            if str(reaction.emoji) == "⏮️":
                await reaction.message.channel.send("This function is still under developing")
                await reaction.message.remove_reaction(emoji = reaction.emoji, member = user)
            '''
    @commands.command(aliases = ["cusemb"], help = "Allows you to make custom embed messages Like typing cmd")
    async def custom_embed(self, ctx:Context,*,data:str):
        new = data.split("-",(len(data)-1))
        fields = []
        field_values = []
        inline = []
        for i in new:
            if i.startswith("title"):
                output_title = i[-(len(i)-6):]
            
            elif i.startswith("desc"):
                output_desc = i[-(len(i)-5):]
            
            #elif i.startswith("color"):
                #output_color = i[-(len(i)-6):]
            
            elif i.startswith("field"):
                fields.insert(len(fields),i[-(len(i)-6):])

            elif i.startswith('value'):
                field_values.insert(len(field_values), i[-(len(i)-6)])

            elif i.startswith('inline'):
                inline.insert(len(inline), i[-(len(i)-7):])
                
        
        
        output_color = discord.Colour.blue()
        

        embed = discord.Embed(
            title = output_title,
            description = output_desc,
            colour = output_color
        )

        for i,x in enumerate(fields):
            embed.add_field(name = x, value = f"{field_values[i]}", inline = False)

        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        embed.set_author(name = f"{self.client.user}", icon_url = self.client.user.avatar.url)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.user.avatar.url)
        await ctx.send(embed = embed)


    @commands.command(aliases = ["rrole"], help = "Creates a message and you can react with the emoji that the bot reacted with to get certain role")
    @commands.has_permissions(administrator = True)
    async def reactionrole(self , ctx:Context, *, role):
        global _role

        requested_guild = ctx.message.guild
        _role = requested_guild.get_role(role)
        embed = discord.Embed(
            title = f"React with the emoji to get role {_role}",
            description = "a",
            colour = discord.Colour.blue()
        )
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        
        embed.set_author(name = f"{self.client.user}", icon_url = self.client.user.avatar.url)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.user.avatar.url)
        await ctx.channel.purge(limit = 1)
        message = await ctx.send(embed = embed)
        emojis = emoji.emojize(":raised_hand:")
        await message.add_reaction(emojis)

    @commands.command(aliases = ["poll"], help = "Creates a poll that has a default 5 minutes expire time.")
    @commands.has_permissions(administrator = True)
    async def creat_poll(self, ctx:Context, *, data:str):
        user = ctx.message.author
        new = data.split(",", len(data))
        has_title = False
        has_option = False
        option_count = 0
        emojis = [":keycap_1:",":keycap_2:",":keycap_3:",":keycap_4:",":keycap_5:", ":keycap_6:", ":keycap_7:", ":keycap_8:", ":keycap_9:"]
        options = []
        i = 0 
        
        for x in new:
            if i == 0:
                embedtitle = x
            else:
                options.insert(x, len(options))
                if option_count < 10:
                    option_count += 1
            i += 1
        
        embed = discord.Embed(
            title = f"{embedtitle}",
            description = f"Poll created by {user}",
            color = discord.Colour.blue()
        )
        for x, y in options, emojis:
            embed.add_field(name = f"{x}", value = f"{y}", inline = False)

        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        
        embed.set_author(name = f"{self.client.user}", icon_url = self.client.user.avatar.url)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.user.avatar.url)
        message = await ctx.send(embed = embed)
        await message.add_reaction(emojis)

    @commands.command(aliases = ["thu","thumb"])
    async def get_yt_thumbnail(self, ctx:Context, url):
        #await ctx.message.edit(embed=None)
        yt = YouTube(url)
        message = await ctx.send(f"{yt.thumbnail_url}")
        await message.add_reaction("✅")

    @commands.command(help = "dont use it", aliases = ['s'])
    @commands.dm_only()
    async def say(self, ctx:Context, channel_id, *, sentence = '\n'):
        global Me
        cmd = ctx.message
        author = cmd.author
        channel = self.client.get_channel(int(channel_id))
        if channel == None:
            channel = self.client.get_user(int(channel_id))
        if author.id == Me:
            if len(ctx.message.attachments) > 0:
                msg = await channel.send(sentence)
                files = []
                for x in ctx.message.attachments:
                    files.append(await x.to_file())

                await msg.edit(attachments = files)
                await author.send('sent!')
            else:
                msg = await channel.send(sentence)
                await author.send('sent!')
        else:
            return


    @commands.command(name = 'get_id')
    async def get_id(self, ctx:Context, *,args):
        args = args.split('<')[1]
        args = args.split('>')[0]
        await ctx.message.channel.send(args[1:])

    @commands.command(name = 'get_avatar', aliases = ['get_photo'])
    async def get_avatar(self, ctx:Context, *, args = None):
        if args != None:
            args = args.split('<')[1]
            args = args.split('>')[0]
            user = self.client.get_user(int(args[1:]))
            if user != None:
                return await ctx.send(user.avatar)
        else:
            return await ctx.send(ctx.author.avatar)

    @commands.command(name = 'get_info', aliases = ['user_info'])
    async def get_info(self, ctx:Context, *, args = None):
        get_user_info = None
        if args!=None:
            try:
                args = args.split('<')[1]
                args = args.split('>')[0]
                user = ctx.guild.get_member(int(args[1:]))
            except:
                user = await self.client.fetch_user(int(args))

            if user != None:
                get_user_info = user
        
        else:
            get_user_info = ctx.author

        if type(get_user_info) != User:
            stats_icon = ''
            if get_user_info.status.name == 'online':
                stats_icon = '🟢'
            elif get_user_info.status.name == 'dnd':
                stats_icon = '🔴'
            elif get_user_info.status.name == 'idle':
                stats_icon = '🟡'

            embed = await get_embed(client = self.client, title = f'{stats_icon}{get_user_info}的資訊', desc = f'目前上線狀態：{get_user_info.status}')
            embed.color = get_user_info.colour
            embed.set_thumbnail(url = get_user_info.avatar.url)
            embed.add_field(name = '使用者ID', value = f'{get_user_info.id}', inline = False)
            embed.add_field(name = '加入此伺服器於', value = f'{get_user_info.joined_at.strftime("%Y/%m/%d %H:%M:%S")}', inline = True)
            embed.add_field(name = '加入discord於', value = f'{get_user_info.created_at.strftime("%Y/%m/%d %H:%M:%S")}', inline = True)
            embed.add_field(name = '身分組', value = ''.join(f"{i.mention} " for i in get_user_info.roles), inline = False)
            embed.set_footer(text = f'{embed.footer.text} | Message in {ctx.guild.name}', icon_url = embed.footer.icon_url)
        else:
            embed = await get_embed(client = self.client, title = f'{get_user_info}的資訊')
            embed.color = get_user_info.colour
            embed.add_field(name = '使用者ID', value = f'{get_user_info.id}', inline = False)
            embed.add_field(name = '加入discord於', value = f'{get_user_info.created_at.strftime("%Y/%m/%d %H:%M:%S")}', inline = True)
            
        return await ctx.send(embed = embed)

            

    @say.error
    async def say_error(self, ctx:Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title = "Error!",
                description = "This is an error message",
                colour = discord.Colour.blue()
            )
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)
            
            embed.set_author(name = f"{self.client.user}", icon_url = self.client.user.avatar.url)
            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.user.avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction(emoji.emojize(":cross_mark:"))

    @custom_embed.error
    async def custom_embed_error(self,  ctx:Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title = "Usage",
                description = " ",
                colour = discord.Colour.blue()
            )
            embed.add_field(
                name = "a!cusemb -title <title> -desc <desc> -field <field> -value <value>", 
                value = "Note that if you create a field you have to give it a value. Also you can add as many fields as you want.", 
                inline = False
            )
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)
            
            embed.set_author(name = f"{self.client.user}", icon_url = self.client.user.avatar.url)
            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.user.avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction(emoji.emojize(":cross_mark:"))  


async def setup(client):
    await client.add_cog(others(client))
        