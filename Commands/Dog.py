@bot.command(name = 'snipedog', aliases=['dog'])
async def snipedog(ctx):
    channel = ctx.channel
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    await ctx.send(data['message'])