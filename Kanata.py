import discord
from discord import channel
from discord import colour
from discord.colour import Color
from discord.voice_client import VoiceClient
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discordSuperUtils import MusicManager
import youtube_dl
import random
import math
import os
import discordSuperUtils
from pytube.__main__ import YouTube
from discordSuperUtils import MusicManager
import asyncio
import json
import emoji
import pytube
import time
from datetime import date

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
intents = discord.Intents.default()
intents.members = True 
client = commands.Bot(command_prefix = pre, help_command=None) 
#client.remove_command('help')
MusicManager = MusicManager(client, client_id=client_id, client_secret=client_secret)

status = cycle([f'{pre}h' , 'かわいいかなたそ!!'])




queue = []
queue_url = []
queueadd = []
queue_source = []
queue_image_url = []
nowplaying = 0
help_message = 0
playmessages = 0
queuemessages = 0
loop_state = False
voice_joined = False
MyDiscordID = "星詠み#6942"
default_footer = f"Developed by {MyDiscordID} version:{version}"
default_footer_icon = "https://cdn.discordapp.com/avatars/398444155132575756/77db70f07858b08a72896f248e2ffcaf.webp?size=4096"





#background task

@tasks.loop(seconds = 30)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))

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
    channel = discord.utils.get(member.guild.channels, name='機器人刷頻區')
    embed = discord.Embed(
        title = "Welcome to our server!",
        description = f"{member.mention}"
    )
    embed.add_field(name = "Looking for help?", value = "Type a!h to see list of commands!", inLine = False)
    embed.set_footer(text = default_footer, icon_url = default_footer_icon)
    await channel.send(embed = embed)


@client.event
async def on_message(message):
    global help_message
    ctx = message.content
    if message.author == client.user:
        return 


    elif ctx.startswith('Hello!!'):
        await message.channel.send('Hello!!')

    elif ctx.startswith('.') and ctx.endswith("."):
        await message.channel.send('不要句點我啦QQ')

    elif ctx.startswith('Your chest is small'):
        responses = ['You wanna die huh?' ,'Ill kill you', 'I thoght you love me!' , 'No. Im boing boing', 'Whatever you say.' ,'大嫌い!!']
        await message.channel.send(random.choice(responses))
        
    elif ctx.startswith('yay') or ctx.startswith('Ya') or ctx.startswith('YA'):
        responses = ["I'm glad that you're happy!" , "yay!!!", 'Yay!!!', "I'm happy too!!" ]
        await message.channel.send(random.choice(responses))
    
    elif message.content.startswith('kanata') or message.content.startswith("kanatan"):
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        embed = discord.Embed(
            title = f"Hi! \nAmane kanata desu! \nIs there anything I can help?",
            description = "React with the reactions below to choose.",
            color = discord.Colour.blue()
        )
        embed.add_field(name = "1", value = "Help menu", inline = False)
        embed.add_field(name = "2", value = "Play music", inline = False)
        embed.add_field(name = "3", value = "still thinking", inline = False)
        embed.add_field(name = "4", value = "still thinking", inline = False)
        embed.add_field(name = "5", value = "still thinking", inline = False)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        embed.set_author(name = f"{client.user}", icon_url = default_footer_icon)
        sent_message = await message.channel.send(embed = embed)
        help_message = sent_message
        emojis = [":keycap_1:",":keycap_2:",":keycap_3:",":keycap_4:",":keycap_5:"]
        for x in emojis:
            emojib = x
            await sent_message.add_reaction(emoji.emojize(emojib))


    await client.process_commands(message)


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')

'''
commands
'''



#▶️⏸⏭⏮        




@client.command(aliases = ["hlep", "help"], help='Returns help menu')
async def h(ctx):
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
    helpmenu.set_author(name = f"{client.user}", icon_url = default_footer_icon)
    helpmenu.add_field(
        name = "If you need any help you can message me on Discord" , 
        value = f"{MyDiscordID}", 
        inline = True)
    helpmenu.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
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
        title = f"Bot coded by {MyDiscordID}",
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
    info.add_field(name = "Author", value = f"{MyDiscordID}")
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
        title = f"Welcome to our server, {ctx.message.author}!",
        color = discord.Colour.blue()
    )
    embed.set_author(name = client.user, icon_url = default_footer_icon)
    embed.add_field(name = "Looking for help?", value = "Type a!h to see list of commands!",inline = False)
    embed.set_footer(text = default_footer, icon_url = default_footer_icon)
    await ctx.send(embed=embed)
    

@client.command(help = "dont use it")
async def say(ctx,*,sentence):
    a = random.randint(1,5)
    await ctx.channel.purge(limit = 1)
    message = await ctx.send(sentence)
    if a == 4 or a == 3:                                  ##pleading face                 ##smiling face with hearts
        emojis = ["\N{thinking face}","\N{crying face}","\U0001F97A","\N{flushed face}","\U0001F970"]
        emoji = str(random.choices(emojis))
        await message.add_reaction(emoji[2])

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
        message = await ctx.send(f'Player paused by <@!{user}>')
        ##emoji = "\U00023f8" ##pause button
        ##await message.add_reaction(emoji)

@client.command(aliases = ["res"],help =  "Resumes the current song playing")
async def resume(ctx):
    user = ctx.message.author.id
    if await MusicManager.resume(ctx):
        message = await ctx.send(f'Player resumed by <@!{user}>')
        ##emoji = "\u00025b6" ##play button
        ##await message.add_reaction(emoji)


@client.command(aliases = ["dc","disconnect"],help =  "Disconnects the bot from the voice channel")
async def leave(ctx):
    global voice_joined
    if await MusicManager.leave(ctx):
        await ctx.send("Left the Voice Channel")
        voice_joined = False

@client.command(aliases = ['nowplaying'] , help = "Shows the song that is currently being played")
async def np(ctx):
    if player := await MusicManager.now_playing(ctx):
        i = 0
        for x in queue:
            if x.title == player:
                break
            else:
                i+=1
        currently_playing = discord.Embed(
            title = "Currently playing",
            description = "",
            color = discord.Colour.blue()
        )
        currently_playing.add_field(name = "Video title", value = f"{player}", inline = False)
        currently_playing.set_image(url = queue_image_url[i-1])
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)

        currently_playing.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        message = await ctx.send(embed = currently_playing)
        emojie = "\N{BLACK RIGHT-POINTING TRIANGLE}" ##play button
        await message.add_reaction(emojie)
    else:
        await ctx.send("Not playing anything")

@client.command(aliases = ['rm'] , help = 'Removes the song selected frome the queue')
async def remove(ctx, index:int):
    t = time.localtime()
    today = date.today()
    today_date = today.strftime("%Y/%m/%d")
    current_time = time.strftime("%H:%M:%S", t)
    user = ctx.message.author
    if await MusicManager.queue_remove(ctx, index):
        
        embed = discord.Embed(
            title = f"Removed {queue[index].title}",
            descrpition = f"Removed by <@!{user}>",
            Color = discord.Colour.blue()
        )
        embed.set_image(url = queue_url[index].thumbnail_url())
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        queue.remove(index)
        queue_url.remove(index)
        queueadd.remove(index)
        message = await ctx.send(embed = embed)
        emoji = "\N{PUT LITTER IN ITS PLACE SYMBOL}"
        await message.add_reaction(emoji)

@client.command(aliases = ["q","queue"] , help = 'Returns the queue')
async def _queue(ctx):
    global queue_url
    global queueadd
    global queue
    global queue_source
    global queuemessages

    
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
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        queueembed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        queuemessages = await ctx.send(embed = queueembed)
        emojis =  [":play_button:", ":pause_button:", ":last_track_button:",":next_track_button:"]
        for i in emojis:
            i = emoji.emojize(i)
            await queuemessages.add_reaction(i)
    else:
        empty = await ctx.send("The queue is empty. Use the play command to add some songs to queue")
        emojie = emoji.emojize(":cross_mark:")
        await empty.add_reaction(emojie)

@client.command(help = "Skips the current song playing, if any")
async def skip(ctx):
    if await MusicManager.skip(ctx):
        message = await ctx.send("Skipped!")
        emoji = "\N{black right-pointing double triangle}"
        await message.add_reaction(emoji)
    else:
        await ctx.send("This is the end of the queue!")
        await ctx.voice_client.disconnet()
    
@client.command(aliases = ["comein, come"],help = "Joins the voice channel that you're currently in")
async def join(ctx):
    user = ctx.message.author
    global voice_joined
    try:
        await user.voice.channel.connect(timeout = 1000000)
        message = await ctx.send("Joined Voice Channel")
        emoji = "\N{WAVING HAND SIGN}"
        await message.add_reaction(emoji)
        voice_joined = True
    except:
        await ctx.send("An error occured. Please try again later")

@client.command(aliases = ['p'] , help = 'Plays the song')
async def play(ctx, *, url: str):
    global queue
    global queue_url
    global queueadd
    global queue_source
    global voice_joined
    global nowplaying
    global playmessages

    user = ctx.message.author

    if not ctx.message.author.voice:
        await ctx.send("You're not connected to a voice channel")
        voice_joined = False
        return
    elif not voice_joined:
        channel = user.voice.channel
        await channel.connect()    
        await ctx.send("Joined Voice Channel")
        await ctx.guild.change_voice_state(channel = ctx.message.author.voice.channel , self_deaf=True)
        voice_joined = True
        Loading = await ctx.send("Loading song.......This could take a few minute")
    async with ctx.channel.typing():
        player = await MusicManager.create_player(url, requester = user)
        await MusicManager.queue_add(players = player, ctx = ctx) 
        player2 = await YTDLSource.from_url(url, loop = client.loop)

        await MusicManager.play(ctx)

        
        '''
        embed
        '''
        yt = pytube.YouTube(url)
        
        nowplayingembed = discord.Embed(
                    title = f"{player2.title}",
                    description = "**Added to queue** ",
                    url = f'{url}',
                    colour = discord.Colour.blue()
                    )
        nowplayingembed.set_thumbnail(url = f'{yt.thumbnail_url}')
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        nowplayingembed.add_field(name = f"Requested by", value = f'{user.mention}')
        nowplayingembed.add_field(name = "Video source", value = f"{yt.channel_url}")
        nowplayingembed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
        #nowplayingembed.add_field(name = f"Video:", value = '')
        #await ctx.send(f'**Now Playing:**  {player2.title}, added by <@!{user}>')
        
        playmessages = await ctx.send(embed = nowplayingembed)
        emojis = [":play_button:", ":pause_button:", ":last_track_button:",":next_track_button:"]
        for i in emojis:
            i = emoji.emojize(i)
            await playmessages.add_reaction(i)
        queue.insert(len(queue),player2)
        queue_url.insert(len(queue_url) , url)
        queueadd.insert(len(queueadd), user.id)
        queue_source.insert(len(queue_source), yt.channel_url)
        queue_image_url.insert(len(queue_image_url), yt.thumbnail_url)
    
@client.command(aliases = ['vol'] , help = 'Controls the volume of the bot')
async def volume(ctx, volume: int):
    if await MusicManager.volume(ctx, volume):
        await ctx.send(f"Volume has been set to {volume}")

@client.command(aliases = ["l"], help = "Loops the current queue")
async def loop(ctx):
    global loop_state
    loop_state = await MusicManager.loop(ctx)
    if loop_state:
        message = await ctx.send(f"Now looping the queue")
        emoji = "\U0001F501" ##repeat button
        await message.add_reaction(emoji)
    else:
        message = await ctx.send(f"Looping was toggled off")
        emoji = "\N{cross mark}"
        await message.add_reaction(emoji)
        

@client.command(aliases = ["stp", "shutup"], help = "Stops the current player and disconnects")
async def stop(ctx):
    global voice_joined
    global queue
    global queue_url
    global queueadd

    queue.clear()
    queueadd.clear()
    queue_url.clear()

    user = ctx.message.author
    ctx.voice_client.pause()

    message = await ctx.send(f"Player has been stopped by <@!{user.id}>")
    ##emoji = "\U000123F9" ##stop button
    ##await message.add_reaction(emoji)
    await ctx.voice_client.disconnect()
    message = await ctx.send("Disconnected")
    ##emoji = "\U0001f44b"
    ##await message.add_reaction(emoji)
    voice_joined = False


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

@client.command(aliases = ["extlist"], help = "<ADMIN only command> Lists the extensions available")
@commands.has_permissions(administrator = True)
async def extensionlist(ctx):
    number = 0
    listembed = discord.Embed(
        title = "List of available extensions",
        description = "Returns the list",
        color = discord.Colour.blue()
    )
    t = time.localtime()
    today = date.today()
    today_date = today.strftime("%Y/%m/%d")
    current_time = time.strftime("%H:%M:%S", t)
    for filename in os.listdir('./cogs'):
        number += 1
        if filename.endswith('.py'):
            listembed.add_field(name = f"{number}", value = f"{filename[:-3]}", inline = False)
    listembed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
    await ctx.send(embed = listembed)
        


'''
Errors

Dear towa : A friend of mine , who is currently in love with suisei, and i had a bet that if i could have towasama mention him in stream, he will start watching you and giving you support. So can towasama please say his name "rrwww4"?
I would be very much appreciated. He will start giving you support. Thank you towasama i love you!

'''


@dice.error
async def dice_error(ctx, error):
    global default_footer
    global default_footer_icon
    t = time.localtime()
    today = date.today()
    today_date = today.strftime("%Y/%m/%d")
    current_time = time.strftime("%H:%M:%S", t)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title = "ERROR!"
            ,description = "This is an error message"
            ,colour = discord.Colour.blue()
        )
        embed.add_field(name = "Appropraite usage:" , value = f"{pre}dice <value 1> <value 2>")
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = default_footer_icon)
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
