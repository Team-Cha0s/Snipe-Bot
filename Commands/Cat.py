@bot.command(name = 'snipecat', aliases=['cat'])
async def snipecat(ctx):
    channel = ctx.channel
    response = requests.get('https://aws.random.cat/meow')
    data = response.json()
    await ctx.send(data['file'])