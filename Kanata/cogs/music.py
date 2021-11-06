import discord
import asyncio
import os
import youtube_dl

from discordSuperUtils import MusicManager

import urllib.parse, urllib.request, re
import requests

from discord.ext import commands
from discord import Embed, FFmpegPCMAudio
from discord.utils import get



queue = []
nowplaying = 0



youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)




class music(commands.Cog):
    def __init__(self, client):
        self.client = client


'''
    @MusicManager.event
    async def on_play(self, ctx, player):
        await ctx.send(f"Now playing: {player.title}")
        

    @commands.command(aliases = ["pau"],help =  "Pauses the current song playing")
    async def pause(self, ctx):
        if await MusicManager.pause(self, ctx):
            await ctx.send('Player has been paused')

    @commands.command(aliases = ["res"],help =  "Resumes the current song playing")
    async def resume(self, ctx):
        if await MusicManager.resume(self, ctx):
            await ctx.send('Player has been resumed')


    @commands.command(aliases = ["dc","disconnect"],help =  "Disconnects the bot from the voice channel")
    async def leave(self, ctx):
        if await MusicManager.leave(self, ctx):
            await ctx.send("Left Voice Channel")


    @commands.command(aliases = ['nowplaying'] , help = "Shows the song that is currently being played")
    async def np(self, ctx):
        if await MusicManager.join(ctx):
            await ctx.send("Joined Voice Channel")
        if player := await MusicManager.now_playing(self, ctx):
            await ctx.send(f"Currently playing: {player}")
        else:
            await ctx.send("Not playing anything")

    @commands.command(aliases = ['rm'] , help = 'Removes the song selected frome the queue')
    async def remove(self, ctx, index:int):
        if await MusicManager.queue_remove(self, ctx,index):
            await ctx.send(f"Successfully removed {ctx[index].title}")

    @commands.command(aliases = ['q'] , help = 'Returns the queue')
    async def queue(self, ctx):
        queue = await MusicManager.get_queue(self, ctx)
        await ctx.send(queue)

    @commands.command(help = "Skips the current song playing, if any")
    async def skip(self, ctx):
        if await MusicManager.skip(self, ctx):
            await ctx.send('Skipped!')

    @commands.command(help = "Joins the voice channel that you're currently in")
    async def join(self, ctx):
        if await MusicManager.join(self, ctx):
            await ctx.send("Joined Voice Channel")

    @commands.command(aliases = ['p'] , help = 'Plays the song')
    async def play(self, ctx, *, query: str):
        if await MusicManager.join(self, ctx):
            await ctx.send("Joined Voice Channel")
        player = await MusicManager.create_player(query,requester=ctx.message.author)
        if player:
            await MusicManager.queue_add(players=player, ctx=ctx)

            if not await MusicManager.play(self, ctx):
                await ctx.send(f'**Searching for**' + ctx + '\n' f'**Added to queue:**{player.title}')
            else :
                await ctx.send('**Searching for**' + ctx + '\n' + f'**Now Playing:**{player.title}')

        else:
            await ctx.send("Query not found.")

    @commands.command(aliases = ['vol'] , help = 'Controls the volume of the bot')
    async def volume(self, ctx, volume: int):
        await MusicManager.volume(self, ctx, volume)

    @commands.command()
    async def loop(self, ctx):
        is_loop = await MusicManager.loop(self, ctx)
        await ctx.send(f"Looping toggled to {is_loop}")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
'''

def setup(client):
    client.add_cog(music(client))
