@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member=None):
    try:
        await ctx.send('{}'.format(member.avatar_url))
    except: 
        await ctx.send('{}'.format(ctx.message.author.avatar_url))