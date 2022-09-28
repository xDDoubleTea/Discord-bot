import discord
from discord.ui import View, button, Button
from discord import Interaction
from IPython.lib import latextools
import io
import json


class Latex_render_for_dc:
    async def Latex_dvipng(self, string):
        img = latextools.latex_to_png_dvipng(s = string, color = 'White', wrap = False, scale=2.0)
        if img != None:
            with io.BytesIO(img) as img_render:
                img_render.seek(0)
                files = discord.File(fp = img_render, filename = 'latex.png')
            return files
        else:
            return None
    
    async def fail_rendering(self, msg:discord.Message):
        return rendering_failed_btns(attached_msg=msg)


class rendering_failed_btns(View):
    def __init__(self, attached_msg:discord.Message):
        super().__init__(timeout = None)
        self.attached_msg = attached_msg
        

        with open('latex_tmp.json', 'r') as file:
            data = json.load(file)

        has_msg = False
        for msg in data["messages"]:
            if self.attached_msg.id == msg["message_id"]:
                has_msg = True
                break
        if not has_msg:
            data["messages"].append({"message_id":self.attached_msg.id})
            with open('latex_tmp.json', 'w') as file:
                json.dump(data, file, indent = 4)

    @button(style = discord.ButtonStyle.danger, label = 'Delete message')
    async def delcallback(self, interaction:Interaction, button:Button):
        with open('latex_tmp.json', 'r') as file:
            data = json.load(file)

        has_msg = False
        for msg in data["messages"]:
            if self.attached_msg.id == msg["message_id"]:
                has_msg = True
                break
        if not has_msg:
            index = 0
            for i, msg in enumerate(data["messages"]):
                if msg["message_id"] == self.attached_msg.id:
                    index = i
            data["messages"].pop(index)
            with open('latex_tmp.json', 'w') as file:
                json.dump(data, file, indent = 4)
        return await interaction.message.delete()

class latex_msg_options(View):
    def __init__(self, attached_msg:discord.Message, latex_data:str):
        self.attached_msg = attached_msg
        self.latex_data = latex_data
        with open('latex_tmp.json', 'r') as file:
            data = json.load(file)

        has_msg = False
        for msg in data["messages"]:
            if self.attached_msg.id == msg["message_id"]:
                has_msg = True
                break
        if not has_msg:
            data["messages"].append({"message_id":self.attached_msg.id})
            with open('latex_tmp.json', 'w') as file:
                json.dump(data, file, indent = 4)
        
        super().__init__(timeout=300)

    async def on_timeout(self):
        if self.attached_msg != None :
            with open('latex_tmp.json', 'r') as file:
                data = json.load(file)
            if len(data) != 0:
                index = 0
                for i, msg in enumerate(data["messages"]):
                    if msg["message_id"] == self.attached_msg.id:
                        index = i
                try:
                    data["messages"].pop(index)
                except:
                    pass
                
                with open('latex_tmp.json', 'w') as file:
                    json.dump(data, file, indent = 4)

                return await self.attached_msg.edit(view = None)
            else:
                return

    @button(label = 'Delete message', emoji = '🚮', style = discord.ButtonStyle.red)
    async def delete_callback(self, interaction:Interaction, button:Button):
        with open('latex_tmp.json', 'r') as file:
            data = json.load(file)
        
        index = 0
        for i, msg in enumerate(data["messages"]):
            if msg["message_id"] == self.attached_msg.id:
                index = i
        data["messages"].pop(index)
        with open('latex_tmp.json', 'w') as file:
            json.dump(data, file, indent = 4)
        
        self.attached_msg = None
        return await interaction.message.delete()

    @button(label = 'Show original input', emoji = '❓', style = discord.ButtonStyle.blurple)
    async def show_callback(self, interaction:Interaction, button:Button):
        org_input = self.latex_data
        if interaction.message.content == '':
            if not org_input.startswith('```latex'):
                heading = '```latex\n'
                ending = '\n```'
                org_input = heading + org_input
                org_input = org_input + ending
            button.label = 'Hide original input'
            return await interaction.response.edit_message(content = org_input, view = self)
        else:
            button.label = 'Show original input'
            return await interaction.response.edit_message(content = None, view = self)              

    @button(label = 'Delete orginal message', emoji = '🚮', style = discord.ButtonStyle.gray)
    async def delete_org_msg_callback(self, interaction:Interaction, button:Button):
        org_msg = discord.Message
        if self.attached_msg.reference != None:
            org_msg = await self.attached_msg.channel.fetch_message(interaction.message.reference.message_id)
            if org_msg != None:
                await org_msg.delete()
                return await interaction.response.defer()
        else:
            return await interaction.response.send_message(ephemeral = True, content = 'The original message has been deleted!')