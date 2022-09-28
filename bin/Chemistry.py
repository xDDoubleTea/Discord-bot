from discord import Interaction, Message, TextChannel, User, Client, SelectOption, Embed, ButtonStyle
from discord.ui import TextInput, Select, select, Modal, button, View, Button
from typing import List

class Chemical_type(View):
    def __init__(self, attached_msg:Message):
        self.attached_msg:Message = attached_msg
        self.Chemical_type:str = 'Not Selected'
        super().__init__(timeout = 600)
    
    @select(
        placeholder = '選擇溶質種類(電解質、有機化合物...)',
        options = [
            SelectOption(label = '電解質', value = 'ion_Chemicals', description = '放入水中會解離出陰陽離子'),
            SelectOption(label = '有機化合物', value = 'Orgainic_Chemicals', description = '含碳的化合物且非(碳的氧化物或氰化物)'),
        ],
        max_values=1,
        min_values=1
    )
    async def chemical_type_callback(self, interaction:Interaction, select:Select):
        await interaction.response.defer()
        select.disabled = True
        msg:Message = await interaction.channel.send(content = 'ouo')
        v = Concentration_choice(attached_msg=msg)
        return await msg.edit(view = v)



class Concentration_choice(View):
    def __init__(self, attached_msg:Message):
        self.concentration_type:str = 'Not Selected'
        self.attached_msg:Message = attached_msg
        super().__init__(timeout = 600)
    

    async def on_timeout(self):
        return await self.attached_msg.edit(view = None)


    @select(
        placeholder='請選擇濃度種類',
        options = [
            SelectOption(label = '重量百分率濃度', value='P%', description = '(某溶質質量÷溶液總質量)×100%'),
            SelectOption(label = '體積百分率濃度', value='V%', description = '(某溶質體積÷溶液體積)×100%'),
            SelectOption(label = '重量莫耳濃度', value='C_m', description = '某溶質莫耳數(mol)÷溶液總質量(kg)'),
            SelectOption(label = '體積莫耳濃度', value='C_M', description = '某溶質莫耳數(mol)÷溶液體積(L)'),
            SelectOption(label = '百萬分濃度', value='ppm', description = '某溶質毫克數(mg)÷溶液體積(L)'),
            SelectOption(label = '莫耳分率', value='X', description = '某溶質莫耳數÷溶液中各種溶質莫耳數')
        ],
        min_values=1,
        max_values=1,
        custom_id = 'concentration_type'
    )
    async def type_callback(self, interaction:Interaction, select:Select):
        self.concentration_type = select.values[0]
        select.disabled = True
        await interaction.response.defer()
        msg = await self.attached_msg.reply('new')
        return await msg.edit(view = ion_Chemicals_choice(con_type=self.concentration_type, attached_msg = msg))



class ion_Chemicals_choice(View):
    def __init__(self, con_type:str, attached_msg:Message):
        self.attached_msg:Message = attached_msg
        self.con_type:str = con_type
        self.pos_ion = None
        self.neg_ion = None
        super().__init__(timeout = 600)

    @select(
        placeholder = '請選擇陽離子種類'
    )
    async def pos_ion_type_callback(self, interaction:Interaction, select:Select):
        self.pos_ion = select.values[0]
        return await interaction.response.edit_message()

    @select(
        placeholder = '請選擇陰離子種類'
    )
    async def neg_ion_type_callback(self, interaction:Interaction, select:Select):
        self.neg_ion = select.values[0]
        return await interaction.response.edit_message()

    @button(label = '確認送出', style = ButtonStyle.green, emoji = '✅')
    async def confirm_callback(self, interaction:Interaction, button:Button):
        button.disabled = True
        return await interaction.response.send_modal()