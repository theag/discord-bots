import discord, re, random, json

intents = discord.Intents.default()
print(intents)
intents.message_content = True

client = discord.Client(intents=intents)

results = ['Failure','Success, But...', 'Success', 'Success, And...', 'Super Success!']

patt = re.compile('^\\!r(\\d+)dc(\\d+)$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    roll_str = message.content
    mat = patt.search(roll_str)
    
    if mat is not None:
        count = int(mat.group(1))
        dc = int(mat.group(2))
        rolls = []
        successes = 0
        for _ in range(count):
            rolls.append(random.randint(1,6))
            if rolls[-1] >= dc and successes < 4:
                successes += 1
        await message.delete()
        await message.channel.send('{} rolled {} on difficulty {}\nresulting in {}'.format(message.author.mention,','.join(map(str,rolls)),dc,results[successes]))
        

f = open('chester-token.json', 'r')
client.run(json.load(f))
f.close()
#https://discord.com/oauth2/authorize?client_id=1211759427074531378&permissions=11264&scope=bot