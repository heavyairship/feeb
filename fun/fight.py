import salamandrew
import ragebot3000
import dnd

import pdb
import random

class Player(object):
    def __init__(self, name, hp, ac, attack_fun):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attack_fun = attack_fun

    def attack(self, other, verbose=True):
        if verbose:
            print(f"{self.name} ATTACKS!!!")
        dmg = self.attack_fun()
        other.hp -= dmg

def run_trial():
    verbose = False
    players = [
        Player("salamandrew", 102, 17, lambda: salamandrew.salamandrew_attack(3, 9, 18, verbose=verbose, hex=True)),
        Player("ragebot3000", 112, 18, lambda: ragebot3000.ragebot3000_attack(2, 9, 17, advantage=False, verbose=verbose))
    ]
    random.shuffle(players)
    while True:
        players[0].attack(players[1], verbose=verbose)
        if players[1].hp <= 0:
            return players[0]
        players[1].attack(players[0], verbose=verbose)
        if players[0].hp <= 0:
            return players[1]

def run_simulation():  
    wins = {}
    num_trials = 10000

    for _ in range(num_trials):
        winner = run_trial()
        wins[winner.name] = wins.get(winner.name, 0) + 1
    print(wins)

if __name__ == "__main__":
    run_simulation()
