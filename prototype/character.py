import random
from action import Action 

class Character:
    # actions movement die in speed tokens out

    def __init__(self):
        self.action_dice = ["d6","d6","d6","d6"]
        self.action_pool = []
        self.tokens = {}
        self.actions = [Movement()]
    
    def add_tokens(self, tokenType: str, tokenAmount:int):
        if tokenType in self.tokens:
            self.tokens[tokenType] += tokenAmount 
        else:
            self.tokens[tokenType] = tokenAmount

    def roll_die(self, die) -> int:
        if type(die) == int:
            return die 
        elif type(die) == str: #die represented as d4, d6, d8, or d10 this drops the d and gets the number
            size = int(die.split("d").pop())
            result = random.randint(1,size)
            return result

    def start_turn(self):
        # anything else at start of turn
        self.action_pool = []
        for die in self.action_dice:
            self.action_pool.append(self.roll_die(die))

# Basic actions
class Movement(Action):
    def __init__(self):
        super(Movement, self).__init__()
    
    def available(self, pool=[], tokens={}) -> bool:
        if len(pool) > 0:
            return True 
        else:
            return False 
    
    def act(self, actor: Character, die:int):
        actor.add_tokens("speed", die)
        actor.action_pool.remove(die)
    
    def __repr__(self):
        return "X: Movement"

if __name__ == "__main__":
    oc = Character()
    oc.start_turn()
    while True:
        print("action pool:",oc.action_pool)
        print("tokens:", oc.tokens)
        for index in range(len(oc.actions)):
            print(index, oc.actions[index])
        print("which action will you take?")
        result = input(">")
        if result.isdigit() and int(result) < len(oc.actions):
            chosen_action = oc.actions[int(result)]
            print("Which die do you want to use?", oc.action_pool)
            result = input(">")
            if int(result) in oc.action_pool:
                chosen_action.act(oc, int(result))
            else:
                print("You don't have a die for that amount!")
        else:
            print("invalid action, goodbye!")
            break

    print("character.py ran")