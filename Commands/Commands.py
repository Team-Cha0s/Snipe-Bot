@bot.command(name = 'commands', aliases=['cog'])
async def commands(ctx):
    channel = ctx.channel
    em=discord.Embed(title="Snipe Bot Help", description=":white_check_mark: [Click here](https://github.com/MohammedAl-Rasheed/SnipeBot) to see a list of all the commands ")
    em.add_field(name=".", value="If you would like to report any issues please issue one [here](https://github.com/MohammedAl-Rasheed/SnipeBot/issues)", inline=False)
    await ctx.send(embed = em)
