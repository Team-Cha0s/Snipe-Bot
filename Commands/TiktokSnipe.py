@bot.command(name = 'TTSnipe', aliases=['tiktok'])
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