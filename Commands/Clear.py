@bot.command(name='clear')
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)