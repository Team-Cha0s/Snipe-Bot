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