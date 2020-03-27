import dice
import json

bestiary = {}
bestiary_change = False

def read_bestiary():
    global bestiary
    f = open("bestiary.json","r")
    bestiary = json.load(f)
    f.close()
    
def write_bestiary():
    global bestiary_change
    bestiary_change = False
    f = open("bestiary.json","w")
    json.dump(bestiary,f)
    f.close()
    
def add_to_bestiary(input_tuple):
    global bestiary_change
    arr = list(input_tuple)
    arr[1] = int(arr[1])
    arr[4] = int(arr[4])
    bestiary[arr[0].lower()] = arr
    bestiary_change = True

class Monster:
    def __init__(self,name,defense,attack,damage,hp,damage_type=None):
        self.name = name
        self.attack = attack
        self.damage = damage
        self.damage_type = damage_type
        self.defense = defense
        self.max_hp = hp
        self.current_hp = hp
    def attack(self,opponent,defense):
        attack = int(dice.roll(self.attack)[1])
        if attack > defense:
            damage = dice.roll(self.damage)[1]
            if self.damage_type is None:
                return [int(damage),self.name +" hits " +opponent +" for " +damage +" damage"]
            else:
                return [int(damage),self.name +" hits " +opponent +" for " +damage +" " +self.damage_type +" damage"]
        else:
            return [0,self.name +" misses " +opponent]
    def take_damage(self,damage):
        self.current_hp -= damage
        if self.current_hp > self.max_hp/2:
            return [True,self.name +" is wounded"]
        elif self.current_hp > 0:
            return [True,self.name +" is bloodied"]
        else:
            return [False,self.name +" is dead"]
    def heal(self, health):
        self.current_hp += health
        if self.current_hp >= self.max_hp:
            self.current_hp = self.max_hp
            return self.name +" seems to be unwounded"
        elif self.current_hp > self.max_hp/2:
            return self.name +" is still wounded"
        else:
            return self.name +" is still bloodied"

if __name__ == "__main__":
    read_bestiary()
    s = "Kobold 15 1d20+1 1d6-1 5"
    add_to_bestiary(tuple(s.split()))
    print(bestiary)
    write_bestiary()
        