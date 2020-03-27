import discord, re, random

client = discord.Client()
patt = re.compile('(\d+\+)?(\d+)[Dd](\d+)([HhLl]\d+)?(!\d+)?')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    m = patt.search(message.content)
    while m is not None:
        result = do_roll(m.groups())
        await message.channel.send(message.author.mention +' :game_die:\n' +result)
        m = patt.search(message.content,m.end())

def do_roll(dice_tpl):
    size = int(dice_tpl[2])
    original_rolls = []
    rolls = []
    explodes = []
    for _ in range(int(dice_tpl[1])):
        rolls.append(random.randint(1,size))
        original_rolls.append(rolls[-1])
        explodes.append([])
    #keeping some
    if dice_tpl[3] is not None:
        threshold = int(dice_tpl[3][1:])
        if threshold > len(rolls) or threshold <= 0:
            return "You can't keep 0 or less dice or more dice than you rolled."
        keeping = []
        if dice_tpl[3][0] == 'h' or dice_tpl[3][0] == 'H':
            while len(keeping) < threshold:
                curr = 0
                keeping.append(-1)
                for i in range(len(rolls)):
                    if i not in keeping and rolls[i] > curr:
                        curr = rolls[i]
                        keeping[-1] = i
        if dice_tpl[3][0] == 'l' or dice_tpl[3][0] == 'L':
            while len(keeping) < threshold:
                curr = size+1
                keeping.append(-1)
                for i in range(len(rolls)):
                    if i not in keeping and rolls[i] < curr:
                        curr = rolls[i]
                        keeping[-1] = i
        rolls = [rolls[i] for i in keeping]
        explodes = [explodes[i] for i in keeping]
    #exploding
    if dice_tpl[4] is not None:
        threshold = int(dice_tpl[4][1:])
        for i in range(len(rolls)):
            if rolls[i] >= threshold:
                explodes[i].append(random.randint(1,size))
                while explodes[i][-1] >= threshold:
                    explodes[i].append(random.randint(1,size))
    number_result = sum(rolls)
    if dice_tpl[0] is not None:
        number_result += int(dice_tpl[0][:-1])
    for e in explodes:
        number_result += sum(e)
        
    rv = "{}\n".format(number_result)
    if dice_tpl[0] is not None:
        rv += dice_tpl[0]
    rv += '('
    if len(original_rolls) > len(rolls):
        for i in range(len(original_rolls)):
            if i > 0:
                rv += ', '
            rv += "{}".format(original_rolls[i])
        rv += ') -> ('
    for i in range(len(rolls)):
        if i > 0:
            rv += ', '
        rv += "{}".format(rolls[i])
        if len(explodes[i]) > 0:
            rv += ' {}'.format(explodes[i])
    rv += ')'
    return rv
    
client.run('NDgxNDMwMDk4NTc5NDIzMjQx.Xn5JIw.0OkhoiuQf4LR1z5g6sE4xejcnIc')

#:game_die:
#message.author.mention