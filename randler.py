# 10 names
# 5 people
# who gets what?
"""
Randomly generate names for secret santa.
"""
from __future__ import annotations
import random
from typing import List, Set, Tuple


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
    
