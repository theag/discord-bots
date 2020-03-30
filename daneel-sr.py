import discord, re, random, json

client = discord.Client()
patt = re.compile('^[rR]\d+$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    m = patt.match(message.content)
    if m is not None:
        n = int(m.group(0)[1:])
        sucesses = 0
        ones = 0
        str = '('
        for i in range(n):
            r = random.randint(1,6)
            if r == 5 or r == 6:
                sucesses += 1
            elif r == 1:
                ones += 1
            if i > 0:
                str += ', '
            str += '{}'.format(r)
        str += ')'
        await message.delete()
        await message.channel.send(message.author.mention
            +' :game_die:\n{} Sucesses {}'.format(sucesses,str))
        
f = open('bot-token.json', 'r')
client.run(json.load(f)[0])

#:game_die:
#message.author.mention