import discord 
import random
from discord.ext import commands
from datetime import datetime, timedelta, date
from pytz import timezone
import pytz
import emoji
import time


to_do_list_content = [[0 for i in range(1)]for j in range(1)]
to_do_list_owner = []


_role = 0
version = 1.0
MyDiscordID = "星詠み#6942"
default_footer = f"Developed by {MyDiscordID} version:{version}"
default_footer_icon = "https://cdn.discordapp.com/avatars/398444155132575756/77db70f07858b08a72896f248e2ffcaf.webp?size=4096"
me = 398444155132575756

class others(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_reaction(self, reaction, user):
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
                helpmenu.set_author(name = f"{self.client.user}", icon_url = default_footer_icon)
                helpmenu.add_field(
                    name = "If you need any help you can message me on Discord" , 
                    value = f"{MyDiscordID}", 
                    inline = True)
                helpmenu.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
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
    async def custom_embed(self, ctx,*,data):
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
        embed.set_author(name = f"{self.client.user}", icon_url = default_footer_icon)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        await ctx.send(embed = embed)
    
    @commands.command(aliases = ["addtodo"], help = "Add something to your to-do list")
    async def addtodolist(self ,ctx,*,data):
        global to_do_list_content
        global to_do_list_owner
        user = ctx.message.author
        has_user = False
        index = 0
        if len(to_do_list_owner) > 1:
            for x in to_do_list_owner:
                index += 1
                if x == user.name:
                    has_user = True
                    break
            if not has_user:
                to_do_list_owner.insert(len(to_do_list_owner), user.name)
            else:
                print("yay")
        else:
            to_do_list_owner.insert(len(to_do_list_owner), user.name)
        
        #list = [[content],[content]] , list[index] = [user's contents]
        

        embed = discord.Embed(
            title = "Added to your to-do list!",
            description = f"({user.mention}'s to-do list)",
            colour = discord.Colour.blue()
        )
        embed.add_field(name = "To-do", value = f"{data}", inline = False)
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        
        embed.set_author(name = f"{self.client.user}", icon_url = default_footer_icon)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        await ctx.send(embed = embed)
        print(to_do_list_content)
        print(to_do_list_owner)

    @commands.command(aliases = ["rrole"], help = "Creates a message and you can react with the emoji that the bot reacted with to get certain role")
    @commands.has_permissions(administrator = True)
    async def reactionrole(self , ctx, *, role):
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
        
        embed.set_author(name = f"{self.client.user}", icon_url = default_footer_icon)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        await ctx.channel.purge(limit = 1)
        message = await ctx.send(embed = embed)
        emojis = emoji.emojize(":raised_hand:")
        await message.add_reaction(emojis)

    @commands.command(aliases = ["poll"], help = "Creates a poll that has a default 5 minutes expire time.")
    @commands.has_permissions(administrator = True)
    async def creat_poll(self, ctx, *, data):
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
        
        embed.set_author(name = f"{self.client.user}", icon_url = default_footer_icon)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        message = await ctx.send(embed = embed)
        await message.add_reaction(emojis)



    @custom_embed.error
    async def custom_embed_error(self,  ctx, error):
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
            
            embed.set_author(name = f"{self.client.user}", icon_url = default_footer_icon)
            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
            message = await ctx.send(embed = embed)
            await message.add_reaction(emoji.emojize(":cross_mark:"))  







def setup(client):
    client.add_cog(others(client))
        