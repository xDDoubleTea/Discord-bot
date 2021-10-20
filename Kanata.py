import discord
from discord import channel
from discord.colour import Color
from discord.voice_client import VoiceClient
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discordSuperUtils import Music
import youtube_dl
import random
import math
import os
import discordSuperUtils
from discordSuperUtils import MusicManager
import asyncio
import json
import pytube
#import time

Me = 398444155132575756
Member = 489568072483471372

Pi = math.pi


version = 1.0


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

'''
def get_prefix(client , message):
    with open("prefixes.json", "r")as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]
'''



pre = 'a!'
#intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = pre) #, help_command=None
#client.remove_command('help')
MusicManager = MusicManager(client, client_id=client_id, client_secret=client_secret)

status = cycle([f'{pre}h' , 'かわいいかなたそ!!'])




queue = []
queue_url = []
queueadd = []
nowplaying = 0
loop_state = False
joined = False
default_footer = "Bot Developed by Hoshiyomi#6942"
default_footer_icon = "https://cdn.discordapp.com/avatars/398444155132575756/77db70f07858b08a72896f248e2ffcaf.webp?size=4096"





#background task

@tasks.loop(seconds = 30)
async def change_status():
    await client.change_presence(status = discord.Status.dnd, activity = discord.Game(next(status)))

'''
Events
'''

@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready', client.user)
    #base = f'{pre}help'
    #await client.change_presence(status=discord.Status.idle, activity=discord.Game(base))

'''@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r")as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = pre

    with open("prefixes.json","w") as f:
        json.dump(prefixes,f, indent-4)

@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r")as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json","w") as f:
        json.dump(prefixes,f, indent-4)'''

@client.event
async def on_member_join(member):
    joined_guild = member.guild
    channel = joined_guild.get_channel(489439897267077131)
    await channel.send(f'Welcome to {joined_guild.name}!!')


@client.event
async def on_message(message):
    ctx = message.content
    if message.author == client.user:
        return 


    elif ctx.startswith('Hello!!'):
            await message.channel.send('Hello!!')
        
    elif ctx.startswith('hi'):
        await message.channel.send('Hi!!')

    elif ctx.startswith('.'):
        await message.channel.send('不要句點我啦QQ')

    elif ctx.startswith('Your chest is small'):
        responses = ['You wanna die huh?' ,'Ill kill you', 'I thoght you love me!' , 'No. Im boing boing', 'Whatever you say.' ,'大嫌い!!']
        await message.channel.send(random.choice(responses))
        
    elif ctx.startswith('yay') or ctx.startswith('Ya') or ctx.startswith('YA'):
        responses = ["I'm glad that you're happy!" , "yay!!!", 'Yay!!!', "I'm happy too!!" ]
        await message.channel.send(random.choice(responses))
    
        #elif message.content.startswith(''):
            



    await client.process_commands(message)


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')

'''
commands
'''

@client.command(aliases = ["hlep"], help='Returns help menu')
async def h(ctx):
    
    helpmenu= discord.Embed(
        title = "Click me to see list of commands",
        description = "Help menu",
        url = "https://hackmd.io/@Kawaii-kanataso/ry_w9QXVK",
        colour = discord.Color.blue()
    )
    helpmenu.set_author(name = f"{client.user}")
    helpmenu.set_thumbnail(url = 
    "https://cdn.discordapp.com/attachments/672102728469577785/891721492671389696/20210710_223830.jpg")
    helpmenu.add_field(
        name = "If you need any help you can message me on Discord" , 
        value = "Hoshiyomi#6942", 
        inline = True)
    helpmenu.set_footer(text = "Bot Developed by Hoshiyomi#6942" ,icon_url= "https://cdn.discordapp.com/avatars/398444155132575756/77db70f07858b08a72896f248e2ffcaf.webp?size=4096")
    await ctx.send(embed=helpmenu)

@client.command(help = 'Returns the latency of the bot')
async def ping(ctx):
    await ctx.send(f'Ping: {round(client.latency * 1000)} ms.')

@client.command(help = 'Sends random hi messages')
async def hello(ctx):
    responses = ['Hello!' ,'Hi!', 'Hi ! How are you today?', "Hi ! What's up?"]
    await ctx.send(random.choice(responses))

'''@client.command(help = 'Returns the prefix of this server')
async def prefix(ctx):
    await ctx.send(f'prefix is "{pre}"')'''

@client.command(aliases=['8ball' , 'test'], help = 'Returns completly random messages')
async def _8ball(ctx, *, question): 
    responses = ['It is certain.',
                'For sure',
                'without a doubt', 
                'Yes definitely', 
                'Chances are low', 
                'Wouldnt count on it.', 
                'Nope', 
                'Try again', 
                'Think hard and try again', 
                'Go away before I eat your cat', 
                'I thought too hard and died.'
                ,'I love you!'
                ,'Hi Im good']
    await ctx.send(f'{random.choice(responses)}')

@client.command(help = 'Returns a random number')
async def dice(ctx, ground :int, limit :int):
    await ctx.send(random.randint(ground,limit))

@client.command(aliases = ["crd","crds"], help = "Returns the credits")
async def credits(ctx):
    embed = discord.Embed(
        title = "Bot coded by ImHoshiyomi#6942",
        description = f"Version {version}",
        color = discord.Colour.blue()
    )
    embed.set_footer(text="Do not abuse it or I might kill you.")
    await ctx.send(embed = embed)
    

@client.command(aliases = ["info"], help = "Returns the bot information")
async def information(ctx):
    
    info = discord.Embed(
        title = f"{client.user}",
        description = f"Version {version}",
        color = discord.Colour.blue()
    )
    info.set_thumbnail(url = 
    "https://cdn.discordapp.com/attachments/672102728469577785/891721492671389696/20210710_223830.jpg")
    info.add_field(name = "Author", value = "Hoshiyomi#6942")
    await ctx.send(embed=info)



'''@client.command()
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r")as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json","w") as f:
        json.dump(prefixes,f, indent-4)'''


@client.command(aliases = ["embed","em"], help = "test")
async def displayembed(ctx):
    embed = discord.Embed(
        title = "title",
        description = "This is a DESC",
        colour = discord.Colour.blue()
    )
    embed.set_footer(text = 'This is a footer')
    embed.set_image(url = 'https://media.discordapp.net/attachments/860187581445439500/891252962733719562/92644823_p0.png?width=410&height=701')
    embed.set_thumbnail(url = 'https://images-ext-2.discordapp.net/external/upKX3R0FBGs2uJ3fx5Gq43Fwbjo_L08acmFHsX7S_Is/https/pbs.twimg.com/media/FAHXajtUcAQ-p4m.jpg%3Alarge?width=953&height=702')
    embed.set_author(name = 'Author name',icon_url = 'https://cdn.discordapp.com/attachments/860187581445439500/891037312937504809/image0.jpg')
    embed.add_field(name = 'field name', value = 'field value', inline = False)
    embed.add_field(name = 'field name', value = 'field value', inline = True)
    embed.add_field(name = 'field name', value = 'field value', inline = True)

    
    await ctx.send(embed=embed)
    

@client.command(help = "dont use it")
async def say(ctx,*,sentence):
    await ctx.channel.purge(limit = 1)
    await ctx.send(sentence)



'''
Music
'''


@MusicManager.event
async def on_play(ctx, player):
    await ctx.send(f"Now playing: {player.title}")

@client.command(aliases = ["pau"],help =  "Pauses the current song playing")
async def pause(ctx):
    user = ctx.message.author.id
    if await MusicManager.pause(ctx):
        await ctx.send(f'Player paused by <@!{user}>')

@client.command(aliases = ["res"],help =  "Resumes the current song playing")
async def resume(ctx):
    user = ctx.message.author.id
    if await MusicManager.resume(ctx):
        await ctx.send(f'Player resumed by <@!{user}>')


@client.command(aliases = ["dc","disconnect"],help =  "Disconnects the bot from the voice channel")
async def leave(ctx):
    global joined
    if await MusicManager.leave(ctx):
        await ctx.send("Left the Voice Channel")
        joined = False


@client.command(aliases = ['nowplaying'] , help = "Shows the song that is currently being played")
async def np(ctx):
    if player := await MusicManager.now_playing(ctx):
        i = 0
        for x in queue:
            if x.title == player:
                break
            else:
                i+=1
        await ctx.send(f"Currently playing: \n {player}")
    else:
        await ctx.send("Not playing anything")

@client.command(aliases = ['rm'] , help = 'Removes the song selected frome the queue')
async def remove(ctx, index:int):
    if await MusicManager.queue_remove(ctx, index):
        queue.remove(index)
        queue_url.remove(index)
        queueadd.remove(index)
        await ctx.send(f"Removed {queue[index].title}")

@client.command(aliases = ["q","queue"] , help = 'Returns the queue')
async def _queue(ctx):
    global queue_url
    global queueadd
    global queue
    if player := await MusicManager.now_playing(ctx):
        queueembed = discord.Embed(
            title = "Now playing queue:" , color = discord.Colour.blue()
        )
        queuenow = i = find = 0

        for j in queue:
            if j.title == player.title:
                queuenow = find
            find+=1
        
        for x in range(0,queuenow):
            remove = queue[x]
            queue.remove(remove)
            remove = queue_url[x]
            queue_url.remove(remove)
            remove = queueadd[x]
            queueadd.remove(remove)

        for x in queue:
            if x.title == player.title:
                queueembed.add_field(
                        name = f"(Now){x.title}", 
                        value = f"added by <@!{queueadd[i]}>",
                        inline = False
                    )
            else:
                queueembed.add_field(
                        name = f"<{(i+1)-queuenow}> {x.title}", 
                        value = f"added by <@!{queueadd[i]}>",
                        inline = False
                    )
                    
            i += 1
        
        await ctx.send(embed = queueembed)
    else:
        await ctx.send("The queue is empty. Use the play command to add some songs to queue")

@client.command(help = "Skips the current song playing, if any")
async def skip(ctx):
    if await MusicManager.skip(ctx):
        await ctx.send("Skipped!")
    else:
        await ctx.send("This is the end of the queue!")
    

@client.command(help = "Joins the voice channel that you're currently in")
async def join(ctx):
    user = ctx.message.author
    global joined
    try:
        await user.voice.channel.connect()
        await ctx.send("Joined Voice Channel")
        joined = True
    except:
        await ctx.send("An error occured. Please try again later")

@client.command(aliases = ['p'] , help = 'Plays the song')
async def play(ctx, *, url: str):
    global queue
    global queue_url
    global queueadd
    global joined
    global nowplaying

    user = ctx.message.author


    if not ctx.message.author.voice:
        await ctx.send("You're not connected to a voice channel")
        joined = False
        return
    elif not joined:
        channel = user.voice.channel
        await channel.connect()    
        await ctx.send("Joined Voice Channel")
        await ctx.guild.change_voice_state(channel = ctx.message.author.voice.channel , self_deaf=True)
        joined = True

    player = await MusicManager.create_player(url, requester=user)
    await MusicManager.queue_add(players = player, ctx = ctx)
    player2 = await YTDLSource.from_url(url, loop=client.loop)
    yt = pytube.YouTube(url)
    queue.insert(len(queue),player2)
    queue_url.insert(len(queue_url) , url)
    queueadd.insert(len(queueadd), user.id)
    await MusicManager.play(ctx)

    '''
    embed
    '''

    nowplayingembed = discord.Embed(
                title = f"{player2.title}",
                description = "**Added to queue** ",
                url = f'{url}',
                colour = discord.Colour.blue()
                )
    nowplayingembed.set_image(url = f'{yt.thumbnail_url}')
    nowplayingembed.add_field(name = f"Requested by", value = f'{user.mention}')
    #nowplayingembed.add_field(name = f"Video:", value = '')
    #await ctx.send(f'**Now Playing:**  {player2.title}, added by <@!{user}>')
            
    await ctx.send(embed = nowplayingembed)


@client.command(aliases = ['vol'] , help = 'Controls the volume of the bot')
async def volume(ctx, volume: int):
    if await MusicManager.volume(ctx, volume):
        await ctx.send(f"Volume has been set to {volume}")

@client.command(aliases = ["l"], help = "Loops the current queue")
async def loop(ctx):
    global loop_state
    loop_state = await MusicManager.loop(ctx)
    if loop_state:
        await ctx.send(f"Now looping the queue")
    else:
        await ctx.send(f"Looping was toggled off")

@client.command(aliases = ["stp"], help = "Stops the current player and disconnects")
async def stop(ctx):
    global joined
    global queue
    global queue_url
    global queueadd
    queue.clear()
    queueadd.clear()
    queue_url.clear()
    user = ctx.message.author
    ctx.voice_client.pause()
    await ctx.send(f"Player has been stopped by <@!{user.id}>")
    await ctx.voice_client.disconnect()
    joined = False


'''
Admin commands
'''

@client.command(aliases = ["ld"], help = "<ADMIN only command> Load extension")
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    try:
        if str(extension) == "all" or str(extension) == "All":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.load_extension(f'cogs.{filename[:-3]}')
        else:
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} was loaded successfully!')
    except:
        await ctx.send(f"{extension} has already been loaded or doesn't exsit")

@client.command(aliases = ["unld"], help = "<ADMIN only command> Unload extension")
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    try:
        if str(extension) == "all" or str(extension) == "All":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'cogs.{filename[:-3]}')
        else:
            client.unload_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} was unloaded successfully!')
    except:
        await ctx.send(f"{extension} has already been unloaded or doesn't exsit")

@client.command(aliases = ["reld"], help = "<ADMIN only command> Reload extension")
@commands.has_permissions(administrator = True)
async def reload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} was reloaded successfully!')
    except:
        await ctx.send(f"{extension} doesn't exsit")




'''
Errors

Dear towa : A friend of mine , who is currently in love with suisei, and i had a bet that if i could have towasama mention him in stream, he will start watching you and giving you support. So can towasama please say his name "rrwww4"?
I would be very much appreciated. He will start giving you support. Thank you towasama i love you!

'''





@dice.error
async def dice_error(ctx, error):
    global default_footer
    global default_footer_icon
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "ERROR!",description = "This is an error message"
        )
        embed.add_field(name = "Appropraite usage:" , value = f"{pre}dice <value 1> <value 2>")
        embed.set_footer(text = default_footer, icon_url = default_footer_icon)
        await ctx.send(embed = embed)

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author} has no access to this command')

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author} has no access to this command')

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author} has no access to this command')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run('')