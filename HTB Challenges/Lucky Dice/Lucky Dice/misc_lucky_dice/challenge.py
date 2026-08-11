#!/usr/bin/env python3
import random
import time
import sys
import os

rounds = 100
player_nr = random.randint(8, 13)
timeout = 0.3

def userinput(question, correct_answer):
    # Show question
    
    print(question)
    # Get user response
    given_answer = input("> ")
    # Check answer
    return (str(correct_answer) == given_answer.strip())

def loop(rnd):
    print("")

    dice_nr = rnd * 2 + 2
    dice_res = {}
    dice_sum = {}

    print('-----------   ' + 'Round ' + str(rnd+1) + '    -----------')
    for player in range(player_nr):
        dice_list = []
        rp = ('round_' + str(rnd+1), 'player_' + str(player+1))
        dice_sum[rp] = 0
        for dice in range(dice_nr):
            rpd = ('round_' + str(rnd+1), 'player_' + str(player+1), 'dice' + str(dice+1))
            dice_res[rpd] = int(random.randint(1, 6))
            dice_list.append(dice_res[rpd])
            dice_sum[rp] += dice_res[rpd]

        time.sleep(0.1)
        print('Player ' + str(player+1) + ': {dices}'.format(dices = ' '.join(map(str, dice_list))))

    result = sorted(dice_sum.items(), key=lambda x:x[1])[-1][0][1].split('_')[1]

    time.sleep(0.05)
    print('Who wins this round?')
    for player in range(player_nr):
        print(str(player+1) + '. Player' + str(player+1))

    start = time.time() 
    answer = input('> ')

    if time.time() - start > timeout:
        print("Mate... your are too slow! It seems your CPU is too old!")
        return False

    if answer != result:
        print('Hey! I think your scorring is off... Check your RAM... It may be corrupted!')
        return False

    print('Yes.. Correct!')
    return True


print("WELCOME TO THE DICE ARENA ...")
print("     ____             ")
print("    /\' .\\    _____   ")
print("   /: \\___\\  / .  /\\  ")
print("   \' / . / /____/..\\ ")
print("    \\/___/  \'  '\\  / ")
print("             \'__'\\/  ")
time.sleep(0.3)
print("Welcome my fellow bot!")
time.sleep(0.2)
print("I will need your help!")
time.sleep(0.1)
print("We are taksed to keep the score on this human game.")

time.sleep(0.5)
print("The game is simple!")
time.sleep(0.2)
print("Let's go over the rules...")
time.sleep(0.5)
print("1. On each round, each human player roles several dice.")
time.sleep(0.2)
print("2. The outcome of the dice is added to the player's score.")
time.sleep(0.5)
print("3. The round is won by the player with the highest overall score.")
time.sleep(0.5)
print("4. If there is a draw, the player who rolled the last dice wins the round.")
time.sleep(1) 
print("Simple as that!")
time.sleep(0.5)
print("Now... Clean your memory and prepare your registers ...")


print("The humans are about to start the game! Are you ready?")
print("1. Yes")
print("2. No")
if not input("> ").strip() == "1":
    print("Too bad... bye bye")
    sys.exit()

# Start game
print("")
time.sleep(0.5)
print("3 ...")
time.sleep(0.5)
print("2 ...")
time.sleep(0.5)
print("1 ...")
time.sleep(0.5)
print("Go!")

for i in range(rounds):
    if not loop(i):
        print("Check your system and come back later... bye bye")
        sys.exit()

time.sleep(0.2)
print()
print()
print("Nice job!")
time.sleep(0.2)

print("Here is your prize:")
flag_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag.txt")
with open(flag_path) as f:
    flag = f.read().strip()
print(flag)