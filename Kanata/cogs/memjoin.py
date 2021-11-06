import discord
from discord.ext import commands


class memjoin(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
        
        '''
        await member.send("Welcome to our server! Hope you'll have a good time here!")
        '''

def setup(client):
    client.add_cog(memjoin(client))