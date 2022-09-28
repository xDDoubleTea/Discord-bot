from itertools import cycle
import discord
from discord.ext import tasks

pre = 'a!'

bot_token = 'TOKEN'

application_id = 865465022264377376

MyDiscordID = "星詠み#6942"
default_footer = f"Developed by {MyDiscordID}"

MY_GUILD = discord.Object(id = 2)

My_user_id = 1

items = [
    {"name":"她喜歡我", "rarity":"Impossible", "price":"∞"},
    {"name":"神奇海螺", "rarity":"Legendary", "price":"2"}
]

cmds = [
    {
        "catagory":"待辦清單功能",
        "list":
        [
            {"name":"add_to_do", "aliases":["`add_td`"], "usage":f"`{pre}add_td <事項內容>`", "help":"新增一個待辦事項"},
            {"name":"edit_to_do", "aliases":["`edit_td`"], "usage":f"`{pre}edit_td <事項編號> <事項狀態>`", "help":"編輯待辦事項的狀態"},
            {"name":"del_to_do", "aliases":["`del_td`"], "usage":f"`{pre}del_td <事項編號>`", "help":"移除某個待辦事項"},
            {"name":"Check_to_do", "aliases":["`check_td`, ", "`Check_td`"], "usage":f"`{pre}check_td`", "help":"查詢待辦清單"}
        ]
    },
    {
        "catagory":"數學計算功能",
        "list":
        [
            {"name":"add", "aliases":[], "usage":f"{pre}add <數字a> <數字b>","help":"將兩個數相加"}
        ]
    }
]


async def get_embed(client:discord.Client, title:str, desc:str=None):
    embed = discord.Embed(
        title = title,
        description = desc,
        color=discord.Colour.blue()
    )
    dev = client.get_user(My_user_id)
    embed.set_author(name = client.user.name, icon_url = client.user.avatar.url)
    embed.set_footer(text = f'Developed by {dev.name}', icon_url = dev.avatar.url)
    return embed

async def help_msg_embed(client:discord.Client):
    embed = await get_embed(client = client, title = '指令清單', desc = f'使用`{pre}help [指令名稱]`來取得更完整的指令說明！')
    for elements in cmds:
        output = ''
        for i in elements["list"]:
            output += f'指令名稱：`{i["name"]}`'
            if len(i["aliases"]) > 0:
                output += f'，別名：{"".join(ali for ali in i["aliases"])}\n'
            else:
                output += '\n'
        embed.add_field(name = f"===={elements['catagory']}====", value = output, inline = False)
    return embed