# 10 names
# 5 people
# who gets what?
import os
import sys
from pathlib import Path
from random import randint
import os.path as ospath
# initialize names
names = ['T', 'K', 'S', 'G', 'D']
taken = {'T': 0, 'K': 0, 'S': 0, 'G': 0, 'D': 0}
values = {'T': [], 'K': [], 'S': [], 'G': [], 'D': []}


def check_taken(roller_name: str):
    taken_count = 0
    for e in taken.values():
        if e == 2:
            taken_count += 1
    return taken_count


# roll to get new names
def roll(roller_name: str):
    while True:
        first_name = names[randint(0, len(names) - 1)]
        second_name = names[randint(0, len(names) - 1)]
        # if names are equal or any of the names are the same as the roller's name, continue
        taken_count = check_taken(roller_name)
        if first_name == second_name or first_name == roller_name or second_name == roller_name and taken_count == len(
                names) - 3:
            return None
        if first_name != second_name and first_name != roller_name and second_name != roller_name:
            # if the names are already taken continue
            if taken[second_name] == 2 or taken[first_name] == 2:
                continue
            # if the names aren't taken, and none of the three names are equal, increment taken
            taken[second_name] += 1
            taken[first_name] += 1
            # return the checked first and second name
            return [first_name, second_name]


while True:
    for i in names:
        rolled = roll(i)
        if rolled is None:
            for o in taken.keys():
                taken[o] = 0
            for a in values.keys():
                values[a] = 0
            break

        first_name, second_name = rolled
        values[i] = [first_name, second_name]
        if i == names[-1]:
            for p in values.keys():
                first, second = values[p]
                path = f'./values/{p}.txt'
                if not ospath.isdir('./values'):
                    os.mkdir('./values')
                if os.path.isfile(path):
                    with open(path, 'w+') as file:
                        file.write(f'Your people are: {first} and {second}')
                else:
                    with open(path, 'x+') as file:
                        file.write(f'Your people are: {first} and {second}')

            sys.exit()
