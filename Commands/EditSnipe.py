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
