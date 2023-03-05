import json

food_list = []
fails = []
with open('generic-food.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        data = [item.strip() for item in line.split(',')]
        if (len(data) > 4):
            fails.append(data)
            continue
        food_list.append(data)
        

print(fails)

""" from models import db, Ingredient
from app import app
def retrieve_ingredients():
    ingredients = Ingredient.query.all()
    lidt = [ingredient.name for ingredient in ingredients]
    with open('food_import.txt', 'w') as f:
        f.write(str(lidt))
        f.close()
retrieve_ingredients() """