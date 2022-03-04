import discord, re, random, json

client = discord.Client()
patt = re.compile('(\d+\+)?(\d+)[Dd](\d+)([HhLl]\d+)?(!\d+)?')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith("weather"):
        result = weather(message.content.lower()[8:].strip())
        await message.channel.send("{} {}\n{}".format(message.author.mention ,result[0],result[1]))
        return
    m = patt.search(message.content)
    print('starting roll for {}'.format(message.author.name))
    while m is not None:
        result = do_roll(m.groups())
        print('rolling: {} -> {}'.format(m.groups(),result))
        await message.channel.send(message.author.mention +' :game_die:\n' +result)
        m = patt.search(message.content,m.end())
    print('done')

def weather(input):
    r = random.randint(1,100)
    if input == 'sunny':
        if r <= 80:
            return (':sunny:','sunny')
        else:
            return random_weather(False)
    elif input == 'rainy':
        if r <= 50:
            return (':sunny:','sunny')
        else:
            return random_weather(False)
    elif input == 'weird':
        return random_weather(True)
    elif input == '':
        return random_weather(False)
    else:
        return (':warning:','Possible input are rainy, sunny or nothing')

def random_weather(strange_again):
    r = random.randint(1,100)
    if r <= 95 and not strange_again:
        r = random.randint(1,8)
        if r >= 1 and r <= 3:
            return (':partly_sunny:','still\overcast')
        elif r >= 4 and r <= 6:
            return (':sunny:','breezy\light')
        elif r == 7:
            return (':wind_blowing_face:','gusty\heavy')
        elif r == 8:
            return (':thunder_cloud_rain:','windy\thunderstorm')
    else:
        r = random.randint(1,23)
        if r == 1:
            return(':cloud_tornado:','Acid Rain\nAcid Rain corrodes metal, wears down stone, ruins cloth, kills fish, and does 1d6 damage per minute if you are caught in it.  More damage afterwards, too, if you don’t get that stuff off your clothing and skin.')
        elif r == 2:
            r = random.randint(1,6)
            c = ''
            if r == 1:
                c = 'red'
            elif r == 2:
                c = 'orange'
            elif r == 3:
                c = 'yellow'
            elif r == 4:
                c = 'green'
            elif r == 5:
                c = 'blue'
            elif c == 6:
                c = 'purple'
            return(':cloud_tornado:','Painted Rain\nPainted Rain comes down in different colors.  {}.  Mostly harmless, but the green one causes mercury poisoning and the blue one causes hallucinations.  Surfaces (and people) will stain that color until it is washed off.'.format(c))
        elif r == 3:
            return(':cloud_tornado:','Noxious Rain\nNoxious Rain causes vomiting and mutation if you get more than a few drops on you.  Save negates.  It looks like thin, golden brown fluid that smells like a pile of goats that died of dysentery last week.  Use your favorite mutation table.  Afterwards, brown mushrooms grow out of everything that isn\'t metal.')
        elif r == 4:
            return(':cloud_tornado:','Reverse Rain\nReverse Rain pulls water from the surface up into the clouds.  If a creature isn’t indoors or underwater or something, they take 1 damage per minute as they desiccate painfully.  Pink clouds form over crowds of people who are losing a lot of blood.  Green clouds form over forests.  Most clouds formed this way are yellowish brown.')
        elif r == 5:
            return(':cloud_tornado:','Hallucinatory Sky\nHallucinatory Skies are completely harmless, but they are freaky.  Deformed, inhuman faces appear in the clouds and rain down silent indictments, blasphemies, and profanities for those who can read lips.')
        elif r == 6:
            l1 = ''
            l2 = ''
            r = random.randint(1,100)
            if r <= 20:
                l1 = ' it rains fire.'
            r = random.randint(1,100)
            if r <= 20:
                l1 = ' it rolls along the ground like asshole fog.'
            return(':cloud_tornado:','Burning Clouds\nThe clouds turn red, roiling masses of angry cinders.{}{}'.format(l1,l2))
        elif r == 7:
            return(':cloud_tornado:','Rain of Rage\nBlood rains from the sky!  Anyone who gets it in their eyes or mouth flips out in a murderous rage!  They kill their loved ones first!  After the rain stops, affected people dive into a deep depression.')
        elif r == 8:
            return(':cloud_tornado:','Rain of Soot\nHot ashes and soot rain from the sky!  {} feet of it!  1 damage per round if you are caught out there.  Afterwards, snowplows and choking hazards.'.format(random.randint(1,6)))
        elif r == 9:
            return(':cloud_tornado:','Rain of Gasoline\nA very bad time to have a cigarette craving.  This is why we don’t have wooden buildings anymore.  Inevitably, a fire starts by the end of it.  Air quality = shit.  Sewers, waterways, rivers, lakes, ocean runoffs will all become infernos.  Afterwards, oil stains and ashy smudges.')
        elif r == 10:
            return(':cloud_tornado:','Thick Air\nThe air has the consistency of water.  Breathing is exhausting.  Old people die.  Guns and engines don\'t work.  Fish swim out of the ocean and through the air.  When the weather ends, all the fish swimming over dry land drop and die, gasping faces mouthing the word “Why??????”  The fish all die looking betrayed.')
        elif r == 11:
            return(':cloud_tornado:','Antigravity\nAntigravity pillars roam over the land like searchlights from mars (which they might be).  Things caught in the beams fall upwards for {} seconds before falling back down.  Cars are dropped on buildings.  Schoolchildren pepper their playground like a dozen dropped eggs.  Smart folks hang out in their basement and tie themselves to the floor.'.format(random.randint(1,20)+random.randint(1,20)+random.randint(1,20)))
        elif  r == 12:
            return(':cloud_tornado:','Low Gravity\nLike, 1/10 of normal!  It’s like being on the moon!  You can jump really far!  Waves look really cool!  You suck at throwing things because they don’t arc the way they should!  Running is difficult without traction!  Lasts for {} minutes, and then whops back to normal.'.format(random.randint(1,20)*10))
        elif r == 13:
            r = random.randint(1,6)
            c = ''
            if r == 1:
                c = 'frogs'
            elif r == 2:
                c = 'locusts'
            elif r == 3:
                c = 'lice'
            elif r == 4:
                c = 'snakes'
            elif r == 5:
                c = 'minnows'
            elif c == 6:
                c = 'lizards'
            r = random.randint(1,2)
            l = ''
            if r == 1:
                l = 'the vermin are a new species.'
            else:
                l = 'they all share a specific deformity (no eyes, no mouth, no head, two heads, no limbs, spider limbs, etc).'
            return(':cloud_tornado:','Rain of Vermin\n{}. {}'.format(c,l))
        elif r == 14:
            return(':cloud_tornado:','Hungry Fog\nThe fog comes in on little cat feet, a hungry stomach, and sucking tendrils like giant hungry elephant trunks.  Hide and seek as the fog breaks down doors and windows, trying to suck you into its central stomach, where you will be held above the ground, paralyzed, slowly whirled around, and digested in layers.  Lasts {} hours, and usually leaves piles of bones, shoeleather, and keychains in the town square.'.format(random.randint(1,6)))
        elif r == 15:
            return(':cloud_tornado:','Drunk Fog\nThis fog is way more fun than the hungry fog!  Everyone it touches gets wicked drunk!  Chance for alcohol poisoning is low, but don’t drive a car.  The police try to pull people over but they drive into ditches.  Sometimes bad stuff attacks, ‘cuz it knows that everyone sucks at fighting back.')
        elif r == 16:
            return(':cloud_tornado:','Stone Rain\n Stay indoors.  Mostly pebbles, but sometimes fist-sized stones and 1d4 boulders!')
        elif r == 17:
            return(':cloud_tornado:','Reverse Stone Rain\nPieces of rock break off of everything and fly into space.  Buildings look like bites are being taken out of them by invisible rats.  Your exposed skin with also break off in fingernail-sized servings and fly away.  1d6 damage per round after your clothing is gone (shouldn\'t take more than a couple of rounds).')
        elif r == 18:
            r = random.randint(1,6)
            c = ''
            if r == 1:
                c = 'skulls'
            elif r == 2:
                c = 'skeletons'
            elif r == 3:
                c = 'heads'
            elif r == 4:
                c = 'headless corpses'
            elif r == 5:
                c = 'garbage'
            elif c == 6:
                c = 'ectoplasmic ghost guys that crawl around moaning piteously before dying'
            l = ''
            r = random.randint(1,100)
            if r <= 20:
                l = ' this stuff comes to life and attacks everyone.'
            return(':cloud_tornado:','Rain of Horror\n{}.{}'.format(c,l))
        elif r == 19:
            return(':cloud_tornado:','Rain of Worms\nMost of these are just 3" long carnivorous worms, but roll a the largest ones are {} ft.  These are stormworms, with mouths like rotary electric razors and skin in big leathery flaps.  They take minimal damage from falling.  They mostly devote their energy to eating each other, and afterwards people make hunting parties.  Like a lot of these weird weather effects, looting and burglary are rampant.'.format(random.randint(1,4)*random.randint(1,4)))
        elif r == 20:
            return(':cloud_tornado:','Rain of Slimes\nGlobs of carnivorous slime.  Tough to kill, but sunlight, fire, cold, and salt destroy it.  Normally immobile, but if it eats enough (falls on an unlucky herd of cattle), then giant blobs rampage through town eating people.')
        elif r == 21:
            return(':cloud_tornado:','Rain of Meat\nMost of these are bitesize, the biggest chunk of meat is {} lb.  20% of the meat is recognizable, 20% of the meat is poisonous, 20% of the meat looks pre-chewed.  A lot of carnivores slouch in from the hills.  Slorgs go into gluttony mode.  Afterwards, everyone makes bonfires.  Alternatively, fly swarms next week like Moses hates you.'.format(random.randint(1,20)*100))
        elif r == 22:
            r = random.randint(1,4)
            c = ''
            if r == 1:
                c = 'icicles'
            elif r == 2:
                c = 'ninja star snowflakes'
            elif r == 3:
                c = 'no physical knives but things just start getting cut'
            elif r == 4:
                c = 'totally metal knives, I lied about the ice'
            return(':cloud_tornado:','Rain of Knives\nActually just pieces of really sharp ice. {}.'.format(c))
        elif r == 23:
            r1 = random_weather(True)
            r2 = random_weather(True)
            return (':cloud_tornado:',r1[1]+'\n'+r2[1])
        

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

f = open('bot-token.json', 'r')
client.run(json.load(f))
f.close()

#:game_die:
#message.author.mention