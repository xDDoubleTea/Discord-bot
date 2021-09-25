import discord
from discord.ext import commands


class role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def giverole(self, ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        await ctx.channel.purge(limit = 1)
        await ctx.send(f"{user.name} has been given a role called: {role.name}")

    @commands.command(pass_context = True)
    async def removerole(self, ctx, user : discord.Member, role: discord.Role):
        await discord.Role.delete(role)
        await ctx.channel.purge(limit = 1)
        await ctx.send(f"{user.name} has the {role.name} role removed ")

    @commands.command(pass_context = True)
    async def rolelist(self, ctx, type = 1):
        if type == 2:
            role = "\n".join([str(r.name) for r in ctx.guild.roles])
            await ctx.send(role)
        elif type == 1:
            role = "\n".join([str(r.id) for r in ctx.guild.roles])
            await ctx.send(role)    
    

def setup(client):
    client.add_cog(role(client))