import discord
from discord.ext import commands
import random
import os

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def delmes(self, ctx, amount = 2):
        await ctx.channel.purge(limit = amount + 1)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx ,member : discord.Member ,* , reason = None):
        await member.kick(reason = reason)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx ,member : discord.Member ,* , reason = None):
        await member.ban(reason = reason)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def mute(self, ctx, member:discord.Member):
        await member.add_roles(member.guild.get_role(873154403060809768))
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'{member} has been muted')

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unmute(self, ctx, member:discord.Member):
        await member.remove_roles(member.guild.get_role(873154403060809768))
        await ctx.channel.purge(limit = 1)
        await ctx.send(f'{member} has been unmuted')

    @commands.command()
    async def car(self, ctx,number=1, ground = 150000, lim = 370000, amount = 1):
        if number!=1:
            await ctx.send(f'https://nhentai.net/g/{number}')
        else:
            await ctx.channel.purge(limit = amount)
            randomint = random.randint(ground, lim)
            if randomint == 228922:
                randomint = random.randint(ground, lim)
            await ctx.send(f'https://nhentai.net/g/{randomint}')


    @delmes.error
    async def delmes_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author} has no access to this command')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author} has no access to this command')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author} has no access to this command')

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author} has no access to this command')

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author} has no access to this command')

    @car.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author} has no access to this command')














def setup(client):
    client.add_cog(admin(client))