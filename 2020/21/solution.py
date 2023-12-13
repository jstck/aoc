#!/usr/bin/env python3

import sys
import re
from typing import Set, List, Tuple
from collections import defaultdict

def deduce_allergens(foods: List[Tuple[Set[str],Set[str]]], ingredients: Set[str], allergens: Set[str]) -> Tuple[int, list[str]]:
    ingredient_allergens = defaultdict(lambda: allergens)
    allergen_ingredients = defaultdict(lambda: ingredients)
    
    for ii, aa in foods:
        for i in ii:
            ingredient_allergens[i] = set.intersection(ingredient_allergens[i], aa)
        for a in aa:
            allergen_ingredients[a] = set.intersection(allergen_ingredients[a], ii)


    #for i, aa in ingredient_allergens.items():
    #    print(i,aa)
    #print("***")


    can_have_allergen = set()
    for a, ii in allergen_ingredients.items():
        print(a, ii)
        can_have_allergen.update(ii)
    
    no_allergen = ingredients - can_have_allergen

    #print("***")
    #print("N ingredients:", len(ingredients))
    #print("N allergens:  ", len(allergens))
    print("No possible allergen:", no_allergen)

    #Count all occurences of those "safe" ingredients
    total_safe = 0
    for (ing, _) in foods:
        total_safe += len(ing.intersection(no_allergen))
    

    known_allergens = {}
    known_ingredients = {}


    allergen_to_ingredient = dict(allergen_ingredients)
    
    while len(allergen_to_ingredient) > 0:
        for a, ii in allergen_to_ingredient.items():
            print(a, ii)
        print()
    

        #Find allergens with exactly one possible ingredient
        for a, ii in allergen_to_ingredient.items():
            if len(ii) == 1:
                #Lock it in as a result. Pop also removes it from here
                i = ii.pop()
                known_allergens[i] = a
                known_ingredients[a] = i

                #Remove it from any other groups
                for a2, i2 in allergen_to_ingredient.items():
                    if i in i2:
                        i2.remove(i)

        #Filter out all ingredients with empty sets
        allergen_to_ingredient = {a: i for a, i in allergen_to_ingredient.items() if len(i)>0}

    print(known_allergens)
    print(known_ingredients)

    #Sort the ingredient->allergen by key (ingredient), return the allergens
    allergenlist = [known_ingredients[i] for i in sorted(known_ingredients)]

    return total_safe, allergenlist


if __name__ == "__main__":
    lines = sys.stdin.readlines()

    all_ingredients = set()
    all_allergens = set()
    all_foods = []

    for line in lines:
        line = line.strip()
        if len(line) == 0: continue


        matches = re.match("^([a-z ]+) \\(contains ([a-z, ]+)\\)$", line)

        if matches is None:
            print(f"COULD NOT PARSE: {line}")
            sys.exit(1)

        ingredients = {x.strip() for x in str(matches.groups(1)[0]).split()}
        allergens   = {x.strip() for x in str(matches.groups(1)[1]).split(",")}

        food = (ingredients, allergens)

        all_ingredients |= ingredients
        all_allergens |= allergens
        all_foods.append(food)

    (part1, part2) = deduce_allergens(all_foods, all_ingredients, all_allergens)

    print("Part 1:", part1)
    print("Part 2:")
    print(",".join(part2))



