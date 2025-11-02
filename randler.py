# 10 names
# 5 people
# who gets what?
"""
Randomly generate names for secret santa.
"""
from __future__ import annotations
import copy
from math import perm
from os import remove
import random
from typing import Dict, List, Set, Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont


def draw_centered(draw: ImageDraw.ImageDraw, message: str, x: float, y: float, font: FreeTypeFont,
                  color: Tuple[int, int, int] = (255, 0, 0)):
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((x - (w / 2)), (y - (h / 2))), message, font=font, fill=color)


def generate_image(title, subtitle, note):
    img: Image.Image = Image.open('sscard.png')
    pen = ImageDraw.Draw(img)
    draw_centered(pen, title, img.width * .5, img.height * .4, ImageFont.truetype('MAIAN.TTF', 90), color=(0, 0, 0))
    draw_centered(pen, subtitle, img.width * .5, img.height * 0.6, ImageFont.truetype('MAIAN.TTF', 60), color=(0, 0, 0))

    draw_centered(pen, note, img.width * .5, img.height * 0.7, ImageFont.truetype('MAIAN.TTF', 30), color=(0, 0, 0))
    return img




# roll to get new names
def roll(roller_name: str, untaken: List[str]):
    c1 = list(filter(lambda it: it != roller_name, untaken))
    first_choice = random.choice(c1)
    c2 = list(filter(lambda it: it != first_choice, c1))
    second_choice = random.choice(c2)
    untaken.remove(first_choice)
    untaken.remove(second_choice)

    return first_choice, second_choice



def generate(names: List[str]):
    untaken = names + names
    values: Dict[str, Tuple[str, str]] = {}
    for i in names:
        values[i] = roll(i, untaken)

    return values


def generate_all_assignments(names_set: Set[str]) -> List[Tuple[str, Tuple[str,str]]]:
    """ Generate assignments for each name -- Two other and unique names will be chosen for each name, and each name will be chosen twice."""
    names = list(names_set)

    size = len(names_set)
    assignments = {0: (size-1,size-2)}
    for i in range(1, size-1):
        assignments[i] = (size-i, size-i-2)
    assignments[size-1] = (0,1)

    shuffled_values = list(names_set)
    random.shuffle(shuffled_values)
    values = []
    for i in range(len(shuffled_values)):
        values.append((shuffled_values[i], (shuffled_values[assignments[i][0]], shuffled_values[assignments[i][1]])))
    print(values)
    return values
    

    

    
    
    



#%%
def create_tree(universe, appearances: Dict[str, int], output):
    if len(universe) == 0:
        return {}
    permutations = []
    set_minus = list(appearances.keys())
    set_minus.remove(universe[0])
    set_minus = list(filter(lambda it: appearances[it] < 2, set_minus))
    for i in range(len(set_minus)):
        val = set_minus.pop(0)
        for o in set_minus:
            permutations.append((val+ o))
    children = {}
    #print(permutations)
    for i in permutations:
        new_appearances = copy.deepcopy(appearances)
        new_appearances[i[0]] +=1
        new_appearances[i[1]] += 1
        #print(universe[0], i, end=' ')
        children[universe[0] + i] = create_tree(universe[1:],new_appearances, output)
    #if len(universe) > 3:print(children)
    
    return children

def filter_tree(tree: Dict[str, dict]):
    out = {k:filter_tree(v) for k,v in tree.items() if len(v.values()) > 0 or k.startswith('d')}
    return out

def width(tree: dict):
    if len(tree) == 0:
        return 1
    
    return sum([width(i) for i in tree.values()])

def is_valid(key_group: List[str], tree:dict):
    subtree=tree
    for i in key_group:
        if i not in subtree.keys():
            return False
        subtree = subtree[i]
        if len(subtree) == 0:
            return False
    return True

import numpy as np
def make_matrix(key_group: List[str], universe:str):
    mat = np.zeros(shape=(len(key_group), len(key_group)))
    for i in key_group:
        this = universe.index(i[0])
        second = universe.index(i[1])
        third = universe.index(i[2])
        mat[this][second]=1
        mat[this][third]=1
    return mat

    

