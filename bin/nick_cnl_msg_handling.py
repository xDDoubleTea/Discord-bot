import discord
from discord.ext import commands
from discord import Message, TextChannel, Interaction, ButtonStyle
from discord.ui import View ,Modal , button, Button
import json
import random

class ReplyModal(Modal):
    def __init__(self, rpl_msg:Message, main:commands.Cog):
        self.main:commands.Cog = main
        self.rpl_msg:Message = rpl_msg
        super().__init__(title = f'回覆', timeout = None)
    
    reply = discord.ui.TextInput(label = '回覆內容', placeholder='好耶', style = discord.TextStyle.long, required=False)

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        handler = nick_channel_msg_handling(main = self.main)
        return await handler.reply_message(message = self.rpl_msg, content = self.reply.value, user = interaction.user)

class ReplyBtn(View):
    def __init__(self, attached_msg:Message, main:commands.Cog):
        self.attached_msg:Message = attached_msg
        self.main:commands.Cog = main
        super().__init__(timeout = 600)

    @button(label = '回覆', emoji = '↪️', style = ButtonStyle.blurple)
    async def reply_callback(self, interaction:Interaction, button:Button):
        return await interaction.response.send_modal(ReplyModal(rpl_msg=self.attached_msg, main = self.main))

    async def on_timeout(self) -> None:
        return await self.attached_msg.edit(view = None)



class nick_channel_msg_handling:
    def __init__(self, main:commands.Cog):
        self.main:commands.Cog = main

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

    async def send_message(self, message:Message, content:str):
        channel:TextChannel = message.channel
        reply = False
        reply_message = Message
        guild_id = 910150769624358914
        if message.reference != None:
            reply = True
            reply_message = await channel.fetch_message(message.reference.message_id)
        else:
            reply_message = 0

        
        with open('nick_channel.json', 'r') as file:
            data = json.load(file)

        with open('nicks.json','r') as file:
            nicks = json.load(file)
        has_guild = False
        guild_nick_channel_id = 0
        for channel in data["channels"]:
            if channel["guild_id"] == guild_id:
                has_guild = True
                guild_nick_channel_id = channel["channel_id"]

        message_channel:TextChannel = self.main.client.get_channel(guild_nick_channel_id)
        if has_guild:
            stickers = message.stickers
            user_has_nick = False
            nick_name = 0
            for nick in nicks["nicks"]:
                if nick["user_id"] == message.author.id:
                    user_has_nick = True
                    nick_name = nick["nickname"]


            if user_has_nick:
                send_message = f'`{nick_name}` : {content}'
                if reply:
                    sent = await reply_message.reply(send_message, stickers = stickers)
                else:
                    sent = await message_channel.send(send_message, stickers = stickers)
                file = []
                if len(message.attachments) != 0:
                    for attachment in message.attachments:
                        file.append(await attachment.to_file())

                    await sent.edit(attachments = file)
                try:
                    await message.add_reaction('✅')
                except:
                    pass
                return 

            else:
                nickname = await self.generate_nick()
                nicks["nicks"].append({"guild_id":guild_id, "user_id":message.author.id, "nickname":nickname})
                with open('nicks.json', 'w') as file:
                    json.dump(nicks, file, indent = 4)

                send_message = f'`{nick_name}` : {content}'
                if reply:
                    sent = await reply_message.reply(send_message, stickers = stickers)
                else:
                    sent = await message_channel.send(send_message, stickers = stickers)
                file = []
                if len(message.attachments) != 0:
                    for attachment in message.attachments:
                        file.append(await attachment.to_file())

                    await sent.edit(attachments = file)
                await message.add_reaction('✅')
                return 

    async def reply_message(self, message:Message, content:str, user:discord.User, org_msg:Message=None):
        channel:TextChannel = message.channel
        guild_id = 910150769624358914
    
        with open('nick_channel.json', 'r') as file:
            data = json.load(file)

        with open('nicks.json','r') as file:
            nicks = json.load(file)

        stickers = message.stickers
        user_has_nick = False
        nick_name = 0
        for nick in nicks["nicks"]:
            if nick["user_id"] == user.id:
                user_has_nick = True
                nick_name = nick["nickname"]


        if user_has_nick:
            send_message = f'`{nick_name}` : {content}'
            
            sent = await message.reply(send_message, stickers = stickers)
            
            file = []
            if org_msg!=None:
                if len(org_msg.attachments) != 0:
                    for attachment in org_msg.attachments:
                        file.append(await attachment.to_file())
                    await sent.edit(attachments = file)
            return
        else:
            nickname = await self.generate_nick()
            nicks["nicks"].append({"guild_id":guild_id, "user_id":message.author.id, "nickname":nickname})
            with open('nicks.json', 'w') as file:
                json.dump(nicks, file, indent = 4)
            send_message = f'`{nick_name}` : {content}'
            sent = await message.reply(send_message, stickers = stickers)
            file = []
            if org_msg != None:
                if len(org_msg.attachments) != 0:
                    for attachment in org_msg.attachments:
                        file.append(await attachment.to_file())
                    await sent.edit(attachments = file)
            return 
