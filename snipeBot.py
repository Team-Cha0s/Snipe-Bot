
import discord
from discord.ext.commands import Bot
from asyncio.tasks import sleep
import pytz
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import requests
from bs4 import BeautifulSoup


f = open("TOKEN.txt", "r")

bot = Bot(command_prefix='.')
TOKEN = f.read()

@bot.command(name='server')
async def fetchServerInfo(context):
	guild = context.guild
	
	await context.send(f'Server Name: {guild.name}')
	await context.send(f'Server Size: {len(guild.members)}')
	await context.send(f'Server Owner Name: {guild.owner.display_name}')

# Command that returns the persons avatar
@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member=None):
    try:
        await ctx.send('{}'.format(member.avatar_url))
    except: 
        await ctx.send('{}'.format(ctx.message.author.avatar_url))
    

snipe_message_author = {}
snipe_message_authorID = {}
snipe_message_content = {}
snipe_message_time = {}
snipe_message_pfp = {}

@bot.event
async def on_message_delete(message):
    if message.author.bot == False:
        snipe_message_authorID[message.channel.id] = message.author.id
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content
        hours = message.created_at.strftime("%H")
        fHours = int(hours) - 4
        current_timezone_time = message.created_at.strftime(str(fHours) + ":" + "%M" + " %p")
        snipe_message_time[message.channel.id] = current_timezone_time
        snipe_message_pfp[message.channel.id] = message.author.avatar_url

    await sleep(60)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]
    del snipe_message_time[message.channel.id]
    del snipe_message_pfp[message.channel.id]

@bot.command(name = 'snipe')
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id], color=0xdedede)
        em.set_footer(text = str("Today at " + snipe_message_time[channel.id]))
        em.set_author(name=snipe_message_author[channel.id], icon_url=snipe_message_pfp[channel.id])
        await ctx.send(embed = em)
    except:
        await ctx.send(f"There are no recently deleted messages by in #{channel.name}")
        
snipeE_message_author = {}
snipeE_message_content = {}
snipeE_message_time = {}
snipeE_message_pfp = {}

@bot.event
async def on_message_edit(before, message):
    if message.author.bot == False:
        snipeE_message_author[message.channel.id] = message.author
        snipeE_message_content[message.channel.id] = before.content
        hours = message.created_at.strftime("%H")
        fHours = int(hours) - 4
        current_timezone_time = message.created_at.strftime(str(fHours) + ":" + "%M" + " %p")
        snipeE_message_time[message.channel.id] = current_timezone_time
        snipeE_message_pfp[message.channel.id] = message.author.avatar_url

    await sleep(60)
    del snipeE_message_author[message.channel.id]
    del snipeE_message_content[message.channel.id]
    del snipeE_message_time[message.channel.id]
    del snipeE_message_pfp[message.channel.id]
    
@bot.command(name = 'editsnipe')
async def snipeE(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(name = f"Last edited message in #{channel.name}", description = snipeE_message_content[channel.id], color=0xdedede)
        em.set_footer(text = str("Today at " + snipeE_message_time[channel.id]))
        em.set_author(name=snipeE_message_author[channel.id], icon_url=snipeE_message_pfp[channel.id])
        await ctx.send(embed = em)
    except:
        await ctx.send(f"There are no recently edited messages in #{channel.name}")

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'you at night'))

@bot.command(brief="Plays a single video, from a youtube URL", aliases=['p'])
async def play(ctx, url):
    channel = ctx.author.voice.channel
    await channel.connect()
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {'format': 'bestaudio'}
    if not voice.is_playing():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return


@bot.command(name = 'commands', aliases=['cog'])
async def commands(ctx):
    channel = ctx.channel
    em=discord.Embed(title="Snipe Bot Help", description=":white_check_mark: [Click here](https://github.com/MohammedAl-Rasheed/SnipeBot) to see a list of all the commands ")
    em.add_field(name=".", value="If you would like to report any issues please issue one [here](https://github.com/MohammedAl-Rasheed/SnipeBot/issues)", inline=False)
    await ctx.send(embed = em)

@bot.command(name = 'snipecat', aliases=['cat'])
async def snipecat(ctx):
    channel = ctx.channel
    response = requests.get('https://aws.random.cat/meow')
    data = response.json()
    await ctx.send(data['file'])
    
@bot.command(name = 'snipedog', aliases=['dog'])
async def snipedog(ctx):
    channel = ctx.channel
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    await ctx.send(data['message'])

@bot.command(name='clear')
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

@bot.command(name = 'TTSnipe', aliases=['tiktok', 'TT'])
async def TTSnipe(ctx, user):
    url1 = 'https://www.tiktok.com/@' + str(user)
    response = requests.get(url1)
    soup = BeautifulSoup(response.text, features="html.parser")
    images = soup.findAll('img')
    for i in images:
        if i.parent.name == 'span':
            src = i.attrs['src']
    metas = soup.find_all('meta')
    for m in metas:
        if m.get ('name') == 'description':
            desc = m.get('content')
            embed=discord.Embed(title="Tiktok User: " + str(user), description=desc, color=0xdedede, url=url1)
            embed.set_thumbnail(url=src)
            await ctx.send(embed=embed)

bot.run(TOKEN)