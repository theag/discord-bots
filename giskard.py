import discord, re, random, json

client = discord.Client()

dice = ['4\uFE0F\u20E3','6\uFE0F\u20E3','8\uFE0F\u20E3','\U0001F51F']
values = ['d4','d6','d8','d10']

guild_dice = {'Bot Test':['<:twelve:936291406803271782>','<:twenty:936291506766086164>','<:hundred:936291552823762984>']}
guild_values = ['d12','d20','d100']

patt = re.compile('(\d*)d(\d+)(\+\d+)?')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print("received {} from {}".format(message.content,message.author.name))
    #print([hex(ord(a)) for a in message.content])
    roll_str = message.content
    found = False
    for i,d in enumerate(dice):
        if d in message.content:
            roll_str = roll_str.replace(d,values[i])
            found = True
    
    if message.guild.name in guild_dice:
        for i,d in enumerate(guild_dice[message.guild.name]):
            if d in message.content:
                roll_str = roll_str.replace(d,guild_values[i])
                found = True
    
    if found:
        roll_str = roll_str.replace(' ','')
        mat = patt.search(roll_str)
        if mat is not None:
            a = 1
            if mat.groups()[0]:
                a = int(mat.groups()[0])
            s = int(mat.groups()[1])
            m = 0
            if mat.groups()[2] is not None:
                m = int(mat.groups()[2][1:])
            results = []
            for _ in range(a):
                results.append(random.randint(1,s))
            await message.delete()
            if a == 1:
                await message.channel.send('{} rolled {}\n{}'.format(message.author.mention,message.content,sum(results)+m))
            else:
                await message.channel.send('{} rolled {}\n{} ({})'.format(message.author.mention,message.content,sum(results)+m," ".join(map(str,results))))

f = open('bot-token.json', 'r')
client.run(json.load(f))
f.close()

#https://discord.com/api/oauth2/authorize?client_id=936247071671980042&permissions=1073752064&scope=bot