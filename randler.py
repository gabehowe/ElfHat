# 10 names
# 5 people
# who gets what?
"""
Randomly generate names for secret santa.
"""
from __future__ import annotations
import copy
import random
from typing import List, Set, Tuple

def generate_derangement(group: list): 
    tmp = copy.deepcopy(group)
    random.shuffle(tmp)
    while any([tmp[i] == group[i] for i in range(len(group))]):
        random.shuffle(tmp)
    return tmp

def generate_double_derangement(group: list):
    initial = generate_derangement(group)
    second = generate_derangement(initial)
    while any([second[i] == group[i] for i in range(len(group))]):
        second = generate_derangement(initial)
    return initial, second


def generate_all_assignments(names_set: Set[str]) -> List[Tuple[str, Tuple[str,str]]]:
    """ Generate assignments for each name -- Two other and unique names will be chosen for each name, and each name will be chosen twice."""
    names = list(names_set)
    
    first, second = generate_double_derangement(names)
    assignments = zip(first,second)
    values = list(zip(names, assignments))
    return values
    
