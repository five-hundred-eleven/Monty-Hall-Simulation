#!/usr/bin/env python3

import random
from random import randint

NUMBER_OF_DOORS = 10
ITERATIONS = 100000

# Base class player 
class BasePlayer:
    def __init__(self):
        self.correct = 0    # keeps track of successful rounds
        self.total = 0      # keeps track of total rounds
    
    # results() returns the fraction of successes/total
    def results(self):
        return float(self.correct)/(self.total)
   
    # initializes a round of the game.
    # Doors is a list of the door numbers.
    def start_round(self, doors):
        self.guess = None
        self.door_choices = doors
        self.total += 1

    # receive_hint() is called when the host reveals one door, after the player
    # makes the first guess. The door number is removed from the list of
    # possible choices.
    def receive_hint(self, door_num):
        self.door_choices.remove(door_num)
    
    # The door number of the prize door is revealed. If guess is correct, the
    # count of successful rounds is incremented.
    def receive_prize(self, prize_num):
        if prize_num == self.guess:
            self.correct += 1
    
    # Not implemented in the base class
    def guess_door(self):
        pass
    
# Persistant Guess Player: Never changes his guess when the hint is given
class PersistantGuessPlayer(BasePlayer):
    def __init__(self):
        super().__init__()

    # If the initial guess has not been made, chooses a random door number.
    # Otherwise, does nothing.
    def guess_door(self):
        if not self.guess:
            self.guess = random.choice(self.door_choices)
        return self.guess

# Change door player: Always changes his guess when the hint is given
class ChangeGuessPlayer(BasePlayer):
    def __init__(self):
        super().__init__()

    # If the initial guess has not been made, chooses a random door number.
    # Otherwise, removes the previous guess from the list of door choices and
    # picks another random number.
    def guess_door(self):
        if not self.guess:
            self.guess = random.choice(self.door_choices)
        else:
            self.door_choices.remove(self.guess)
            self.guess = random.choice(self.door_choices)
        return self.guess


# Wrapper functions, seems more intuitive because the player is not performing
# these actions.
def reveal_door(player, door_num):
    player.receive_hint(door_num)
def reveal_prize(player, prize_num):
    player.receive_prize(prize_num)

# Performs an iteration of the game with the player.
def commence_round(player, num_doors):
    prize_door = randint(0, num_doors-1)    # the prize door

    player.start_round([i for i in range(0, num_doors)]) 
    g = player.guess_door()                 # the player's guess
    # next section: give player a hint
    doors = [i for i in range(0, num_doors)] # create set of doors
    if prize_door != g:     # if prize door isn't player's guess, eliminate both prize door and guess
        doors.remove(prize_door)    
        doors.remove(g)
    else:                   # else if guess and prize door are the same
        doors.remove(prize_door)
    reveal_door(player, random.choice(doors))   # give the player hint
    player.guess_door()     # allow player to guess again   
    reveal_prize(player, prize_door)    # tell player prize number

if __name__ == '__main__':

    print("Running game with {ndoors} doors and {its} iterations.".format(ndoors=NUMBER_OF_DOORS, its=ITERATIONS))
    p1 = PersistantGuessPlayer()
    p2 = ChangeGuessPlayer()

    for i in range(ITERATIONS):
        commence_round(p1, NUMBER_OF_DOORS)
        commence_round(p2, NUMBER_OF_DOORS)

    print("Persistant choice player:", p1.results())
    print("Change choice player:", p2.results())
