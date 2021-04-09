import discord
from discord.ext.commands import Bot
from asyncio.tasks import sleep
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import requests
import time
import os
import time
from instaloader import Instaloader, Profile
from fortnite_python import Fortnite
import random
from youtubesearchpython import *


fortnite = Fortnite('e5e90256-cab0-4f9b-ac74-1f60d8a42c41')

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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="in " + str(len(bot.guilds)) + " servers | .commands"))

@bot.command(name = 'commands', aliases=['cog'])
async def command(ctx):
    em=discord.Embed(title="Snipe Bot Help", description=":white_check_mark: [Click here](https://github.com/MohammedAl-Rasheed/SnipeBot) to see a list of all the commands ")
    em.add_field(name=".", value="If you would like to report any issues please issue one [here](https://github.com/MohammedAl-Rasheed/SnipeBot/issues)", inline=False)
    await ctx.send(embed = em)

@bot.command(name = 'snipecat', aliases=['cat'])
async def snipecat(ctx): 
    response = requests.get('https://aws.random.cat/meow')
    data = response.json()
    await ctx.send(data['file'])
    
@bot.command(name = 'snipedog', aliases=['dog'])
async def snipedog(ctx):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    await ctx.send(data['message'])

@bot.command(name='clear')
async def clear(ctx, amount = 5):
    if ctx.message.author.name == "qtreplayz":
        await ctx.send("okay")
        await ctx.channel.purge(limit=amount)
    elif ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)
    else:
        await ctx.send("You are not admin ")

@bot.command(name = 'InstagramSnipe', aliases=['instagram', 'IG'])
async def IGSnipe(ctx, User):
    url1 = "https://www.instagram.com/" + str(User)
    L = Instaloader()
    profile = Profile.from_username(L.context, User)
    followers = profile.followers
    PFP = profile.profile_pic_url
    followees = profile.followees
    bio = profile.biography
    embed=discord.Embed(title = User + " on Instagram | " + str(followers) + " Total followers" + " | Follows " + str(followees), description=bio, color=0xdedede, url=url1)
    embed.set_thumbnail(url=PFP)
    await ctx.send(embed=embed)


@bot.command(name = "animequote", aliases=['aq'])
async def poll(ctx, *, anime = '1'):
    if anime == '1':
        response = requests.get('https://animechan.vercel.app/api/random')
        data = response.json()
        anime = data['anime']
        character = data['character']
        quote = data['quote']
        embed=discord.Embed(title="Anime: " + anime + ", " "Character: " + character, description=quote, color=0x9e9e9e)
        await ctx.send(embed=embed)
    else:
        url = 'https://animechan.vercel.app/api/quotes/anime?title=' + str(anime)
        response = requests.get(url)
        data = response.json()
        number = random.randint(0, 9)
        anime = data[number]['anime']
        character = data[number]['character']
        quote = data[number]['quote']
        embed=discord.Embed(title="Anime: " + anime + ", " "Character: " + character, description=quote, color=0x9e9e9e)
        await ctx.send(embed=embed)
        
@bot.command(name = "poll")
async def poll(ctx, *, message): 
    emb=discord.Embed(tile=" POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    
@bot.command(name = 'twitter', aliases=['tw'])
async def twitter(ctx, param):
    url = "https://twitter.com/" + str(param)
    await ctx.send(url)

@bot.command(name = 'fortniteStats', aliases=['FN'])
async def forniteIS(ctx, platform, *, username):
    URL = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + username
    req = requests.get(URL, headers={"TRN-Api-Key": 'e5e90256-cab0-4f9b-ac74-1f60d8a42c41'})
    try:
        lifetime_stats = req.json()['lifeTimeStats']
        res = lifetime_stats[7:]
        matches_played = res[0]['value']
        wins = res[1]['value']
        win_percent = res[2]['value']
        kills = res[3]['value']
        kd = res[4]['value']
        embed = discord.Embed(title="Lifetime Stats for " + str(username), color=0xdedede)

        embed.add_field(name="Matches Played", value=matches_played + '\n', inline=False)
        embed.add_field(name="Wins", value=wins + '\n', inline=False)
        embed.add_field(name="Win percent", value=win_percent + '\n', inline=False)
        embed.add_field(name="Kills", value=kills + '\n', inline=False)
        embed.add_field(name="K/D", value=kd + '\n', inline=False)
        await ctx.send(embed=embed)
    except KeyError:
        return False


@bot.command(name = 'itemshop', aliases=['IS'])
async def itemshop(ctx):
    url = "https://rocket-league.com/items/shop"
    await ctx.send(url)


@bot.command(name = 'ytV', aliases=['ytvideo'])
async def ytV(ctx, param):
    customSearch = CustomSearch(param, VideoUploadDateFilter.lastHour, limit = 1)
    await ctx.send(customSearch.result()['result'])
    link = customSearch.result()['result'][0]['link']
    title1 = customSearch.result()['result'][0]['title']
    datePUB = customSearch.result()['result'][0]['publishedTime']
    dur = customSearch.result()['result'][0]['duration']
    view = customSearch.result()['result'][0]['viewCount']['text']
    desc = "Published: " + str(datePUB) + ", " + "Duration: " + str(dur) + ", " + "Views: " + str(view)
    embed=discord.Embed(title=str(title1), url=str(link), description=desc)
    thumbnail = customSearch.result()['result'][0]['thumbnails']
    print(thumbnail)
    #embed.set_thumbnail(url="https://i.ytimg.com/vi/g3yEHlqCZaI/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLA3aMJOdKNAzO8E2IR3U6r3h4xUXQ")
    await ctx.send(embed=embed)

@bot.command(name = 'dm')
async def send_anonymous_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)


bot.run(TOKEN)
