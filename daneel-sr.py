import discord, re, random

client = discord.Client()
patt = re.compile('(?<=[rR])\d+')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    m = patt.search(message.content)
    if m is not None and message.content == 'r'+m.group(0):
        n = int(m.group(0))
        sucesses = 0
        str = '('
        for i in range(n):
            r = random.randint(1,6)
            if r == 5 or r == 6:
                sucesses += 1
            if i > 0:
                str += ', '
            str += '{}'.format(r)
        str += ')'
        await message.delete()
        await message.channel.send(message.author.mention +' :game_die:\n{} Sucesses {}'.format(sucesses,str))
        
client.run('NDgxNDMwMDk4NTc5NDIzMjQx.Xn4PVg.FqSLfTukqdsfTOjA1Dr81a7oL1Q')

#:game_die:
#message.author.mention