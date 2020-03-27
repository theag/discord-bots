from discord.ext.commands import Bot
from discord import Game,utils
import re,dice,monster,asyncio,math

TOKEN = 'NDgxNDMwMDk4NTc5NDIzMjQx.Xn5JIw.0OkhoiuQf4LR1z5g6sE4xejcnIc'
BOT_PREFIX = ("?","!","=")

client = Bot(command_prefix=BOT_PREFIX)

in_session = None
sessions = {}

PATTERN_MENTION = re.compile(r'(?:\<@)(\d+)(?:\>)')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.channel in sessions:
        cntnt = message.content
        mat = PATTERN_MENTION.search(cntnt)
        while mat is not None:
            member = utils.get(message.server.members, id=mat.group(1))
            cntnt = cntnt[:mat.start()] +"@" +member.name +cntnt[mat.end():]
            mat = PATTERN_MENTION.search(cntnt)
            mat = None
        sessions[message.channel].append(message.author.name +": " +cntnt)
    if  message.author != client.user and message.content[0] in BOT_PREFIX:
        await client.process_commands(message)

@client.command(name='start_session',
                description='starts recording all messages in this channel',
                brief='starts a session',
                aliases=['ss'],
                pass_context=True)
async def start_session(ctx):
    if ctx.message.channel in sessions:
        await client.say(ctx.message.author.mention +" there is already a session started in this channel")
    else:
        sessions[ctx.message.channel] = []
        await client.say("Session started")
        
@client.command(name='end_session',
                description='stops the recording and saves everything',
                brief='ends a session',
                aliases=['es'],
                pass_context=True)
async def end_session(ctx,filename=None):
    if ctx.message.channel in sessions:
        if filename is None:
            await client.say("Session ended")
        else:
            f = open(filename,"w")
            for i,line in enumerate(sessions[ctx.message.channel][1:-1]):
                f.write(line)
                if i < len(sessions[ctx.message.channel])-3:
                    f.write("\n")
            f.close()
            await client.say("Session ended and saved")
        del sessions[ctx.message.channel]
    else:
        await client.say(ctx.message.author.mention +" there is no session running in this channel")
        

@client.command(name='roll',
                description="Call ""dice amount sides"" to roll amount d sides.",
                brief="Rolls some dice.",
                aliases=['r'],
                pass_context=True)
async def dice_roll(ctx,input_str="1d20"):
    [l1,l2] = dice.roll(input_str)
    #await client.delete_message(ctx.message)
    await client.say(ctx.message.author.mention +" :game_die:\n" +input_str +" " +l1 +"\n" +l2)
    
@client.command(name='multiroll',
                description='fill me out',
                brief='Rolls the same dice set multiple times',
                aliases=['rr'],
                pass_context=True)
async def multi_roll(ctx, count_str, dice_str):
    count = int(count_str)
    rolls = []
    total = 0
    for _ in range(count):
        roll = dice.roll(dice_str)
        rolls.append(" ".join(roll))
        total += int(roll[1])
    await client.say(ctx.message.author.mention +" :game_die:\n" +count_str +" " +dice_str +"\n" +("\n".join(rolls)) +"\n" +str(total))
    
@client.command(name='calc',
                description='acceptable operators are: +,-,* or x,/,^,(,)',
                brief='Is a calculator',
                aliases=['c'],
                pass_context=True)
async def calculator(ctx, input_str):
    eval_str = input_str.lower().replace("x","*")
    patt_dice = re.compile(r'\d\w+\d')
    mat = patt_dice.search(eval_str)
    rolls = []
    while mat is not None:
        rolls.append([mat.group()] +dice.roll(mat.group()))
        eval_str = eval_str[:mat.start()] +(rolls[-1][2]) +eval_str[mat.end():]
        mat = patt_dice.search(eval_str)
    patt_exp = re.compile(r'([0-9\.]+|\(.+?\))(?:\^)([0-9\.]+|\(.+?\))')
    mat = patt_exp.search(eval_str)
    if mat is not None:
        eval_str = eval_str[:mat.start()] +"math.pow(" +mat.group(1) +"," +mat.group(2) +")" +eval_str[mat.end():]
        mat = patt_exp.search(eval_str)
        while mat is not None:
            eval_str = eval_str[:mat.start()] +"math.pow(" +mat.group(1) +"," +mat.group(2) +")" +eval_str[mat.end():]
            mat = patt_exp.search(eval_str)
    result = eval(eval_str)
    if int(result) == result:
        result = int(result)
    if len(rolls) > 0:
        rolls = [" ".join(roll) for roll in rolls]
        await client.say(ctx.message.author.mention +" :game_die::1234:\n" +input_str +"\n" +("\n".join(rolls)) +"\n" +str(result))
    else:
        await client.say(ctx.message.author.mention +" :1234:\n" +input_str +"\n" +str(result))

@client.command(name="add_monster",
                description="Add a monster to the bestiary\n<name> <defense> <attack dice> <damage dice> <hp>\n<name> <defense> <attack dice> <damage dice> <hp> <damage_type>",
                brief="Add a monster to the bestiary",
                aliases=["am"],
                pass_context=True)
async def add_monster(ctx,*input_tuple):
    #print(input_tuple)
    monster.add_to_bestiary(input_tuple)
    await client.delete_message(ctx.message)
    await client.say("Sucessfully added " +str(input_tuple))
    
@client.command(name="save_bestiary",
                description="Saves the bestiary to file",
                brief="Saves the bestiary to file",
                aliases=["sb"],
                pass_context=True)
async def save_bestiary(ctx):
    await client.delete_message(ctx.message)
    if monster.bestiary_change:
        monster.write_bestiary()
        await client.say("Sucessfully saved bestiary")
    else:
        await client.say("Bestiary has no unsaved changes")
        
@client.command(name="clear",
                pass_context=True)
async def clear_messages(ctx,count=100):
    count = int(count)
    index = 0
    async for x in client.logs_from(ctx.message.channel,limit=count):
        index += 1
        await client.delete_message(x)
        print("clearing message " +str(index))
    print("done clearing")
    
@client.event
async def on_ready():
    monster.read_bestiary()
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " +client.user.name)
    
    
async def save_bestiary_task():
    await client.wait_until_ready()
    while not client.is_closed:
        await asyncio.sleep(60)
        if monster.bestiary_change:
            monster.write_bestiary()
        
client.loop.create_task(save_bestiary_task())

client.run(TOKEN)