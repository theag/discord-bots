import re
import random

DICE_PATTERN = re.compile("^(\d+)(?:d)(\d+)(\w+)?([\+\-]\d+)?$")
COMMAND_PATTERN = re.compile("([a-z]+)(\d+)")

def roll(input_str):
    mat = DICE_PATTERN.search(input_str)
    rolls = [random.randint(1,int(mat.group(2))) for _ in range(int(mat.group(1)))]
    strs = [str(roll) for roll in rolls]
    roll_str_map = [i for i in range(len(rolls))]
    #extras
    if mat.group(3) is not None:
        for cmd in COMMAND_PATTERN.findall(mat.group(3)):
            #print(cmd)
            value = int(cmd[1])
            if cmd[0] == "kh":
                for i in range(1,7):
                    while len(rolls) > value:
                        try:
                            ind = rolls.index(i)
                            del rolls[ind]
                            strs[roll_str_map[ind]] = "~~" +strs[roll_str_map[ind]] +"~~"
                            roll_str_map = roll_str_map[:ind] +roll_str_map[ind+1:]
                        except ValueError:
                            break
                    if len(rolls) == value:
                        break
            elif cmd[0] == "kl":
                for i in range(6,0,-1):
                    while len(rolls) > value:
                        try:
                            ind = rolls.index(i)
                            del rolls[ind]
                            strs[roll_str_map[ind]] = "~~" +strs[roll_str_map[ind]] +"~~"
                            roll_str_map = roll_str_map[:ind] +roll_str_map[ind+1:]
                        except ValueError:
                            break
                    if len(rolls) == value:
                        break
            elif cmd[0] == "ro":
                i = 0
                tot = len(rolls)
                while i < tot:
                    if rolls[i] == value:
                        del rolls[i]
                        strs[roll_str_map[i]] = "~~" +strs[roll_str_map[i]] +"~~"
                        roll_str_map = roll_str_map[:i] +roll_str_map[i+1:]
                        rolls.append(random.randint(1,int(mat.group(2))))
                        roll_str_map.append(len(strs))
                        strs.append(str(rolls[-1]))
                        tot -= 1
                    else:
                        i += 1
            elif cmd[0] == "rr":
                while value in rolls:
                    i = rolls.index(value)
                    del rolls[i]
                    strs[roll_str_map[i]] = "~~" +strs[roll_str_map[i]] +"~~"
                    roll_str_map = roll_str_map[:i] +roll_str_map[i+1:]
                    rolls.append(random.randint(1,int(mat.group(2))))
                    roll_str_map.append(len(strs))
                    strs.append(str(rolls[-1]))
            elif cmd[0] == "min" or cmd[0] == "mi":
                for i,roll in enumerate(rolls):
                    if roll < value:
                        rolls[i] = value
                        strs[roll_str_map[i]] = strs[roll_str_map[i]] +" -> " +str(value)
            elif cmd[0] == "max" or cmd[0] == "ma":
                for i,roll in enumerate(rolls):
                    if roll > value:
                        rolls[i] = value
                        strs[roll_str_map[i]] = strs[roll_str_map[i]] +" -> " +str(value)
    
    #final printing
    rv = ["("+",".join(strs)+")"]
    if mat.group(4) is None:
        rv.append(str(sum(rolls)))
    else:
        rv.append(str(sum(rolls)+int(mat.group(4))))
    return rv


if __name__ == "__main__":
    tests = ['4d6','4d6+2','3d6-2','4d6kh3','4d6kl3','4d6ro3','4d6ro3kh3']
    for test in tests:
        print(" "+test)
        print("".join(["-" for _ in range(len(test)+2)]))
        [l1, l2] = roll(test)
        print(l1+"\n"+l2 +"\n")
        