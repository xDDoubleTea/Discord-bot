import discord
from discord.ext import commands
from config.bot_info import *
from config.Mysql_info import *
from discord.ext.commands import Context


class role(commands.Cog):
    def __init__(self, client):
        self.client:discord.Client = client


    @commands.command(name='set_default_role', aliases = ['s_default_role'])
    async def set_default_role(self, ctx:Context, role_id):
        mydb = MySqlDataBase()
        sql = 'SELECT * FROM default_role'
        role_info = mydb.get_db_data(sql_cmd = sql)
        role = discord.Role
        for x in ctx.guild.roles:
            if role_id == str(x.id):
                role = x
                break
        has_guild = False
        for x in role_info:
            if str(ctx.guild.id) == x[0]:
                has_guild = True
                break
            
        if has_guild:
            sql = 'DELETE FROM default_role WHERE guild_id = %s'
            val = (str(ctx.guild.id),)
            mydb = MySqlDataBase()
            mydb.del_data(sql = sql, values = val)
            sql = 'INSERT INTO default_role(guild_id, role_id) VALUES (%s, %s)'
            val = (str(ctx.guild.id), str(role_id))
            mydb.insert_data(sql = sql, values = val)
            await ctx.channel.send(f'Default role set to {role.name}!')
            for member in ctx.guild.members:
                if len(member.roles) == 1:
                    await member.add_roles(role)
        else:
            sql = 'INSERT INTO default_role(guild_id, role_id) VALUES (%s, %s)'
            val = (str(ctx.guild.id), str(role_id))
            mydb.insert_data(sql = sql, values = val)
            await ctx.channel.send(f'Default role set to {role.name}!')
            for member in ctx.guild.members:
                if len(member.roles) == 1:
                    await member.add_roles(role) 

async def setup(client):
    await client.add_cog(role(client))