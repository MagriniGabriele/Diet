import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as numpy


def proteinCalculus(a, s):
    if a < 1:
        pMin = 1.11
        pMax = pId = 1.32
    elif 1 <= a <= 3:
        pMin = 0.82
        pMax = pId = 1.32
    elif 4 <= a <= 6:
        pMin = 0.76
        pMax = pId = 0.94
    elif 7 <= a <= 10:
        pMin = 0.81
        pMax = pId = 0.99
    elif 11 <= a <= 14:
        if s == 'm' or s == 'M':
            pMin = 0.79
            pMax = pId = 0.97
        else:
            pMin = 0.77
            pMax = pId = 0.95
    elif 15 <= a <= 17:
        if s == 'm' or s == 'M':
            pMin = 0.79
            pMax = pId = 0.93
        else:
            pMin = 0.72
            pMax = pId = 0.90
    elif a > 17:
        pMin = 0.71
        pMax = pId = 0.90
    return pMin, pMax, pId


def mbCalculus(a, s, w):
    if s == 'm' or s == 'M':
        if a < 3:
            MB = 59.512 * w - 30.4
        elif 3 <= a < 10:
            MB = 22.706 * w + 504.3
        elif 10 <= a < 18:
            MB = 17.686 * w + 658.2
        elif 18 <= a < 30:
            MB = 15.057 * w + 692.2
        elif 30 <= a < 60:
            MB = 11.472 * w + 873.1
        elif a >= 60:
            MB = 11.711 * w + 587.7
    else:
        if a < 3:
            MB = 58.317 * w - 31.1
        elif 3 <= a < 10:
            MB = 20.315 * w + 485.9
        elif 10 <= a < 18:
            MB = 13.384 * w + 692.6
        elif 18 <= a < 30:
            MB = 14.818 * w + 486.6
        elif 30 <= a < 60:
            MB = 8.126 * w + 845.6
        elif a >= 60:
            MB = 9.082 * w + 658.5
    return MB


# Caricamento tabella cibi

food = pd.read_csv("data/Food-Tab-Ult.csv", delimiter=";")
# foods = set(food['Descrizione'])
# foods = sorted(foods)
# print(foods)

# Input sesso, età, peso e attività fisica

print('Enter your sex:')
sex = input()

print('Enter your age:')
age = int(input())

print('Enter your weight:')
weight = int(input())

print('Choose your level of activity: \n')
print('1)Sedentary\n2)Moderate active\n3)Active\n4)Strongly active\n')
choice = int(input())

# Calcolo Livello di Attività Fisica

if choice == 1:
    LAF = 1.45
elif choice == 2:
    LAF = 1.60
elif choice == 3:
    LAF = 1.75
elif choice == 4:
    LAF = 2.10
elif choice == 0:
    LAF = 1

# Calcolo bounds calorici

minCalories = mbCalculus(age, sex, weight)
idCalories = (minCalories * LAF)
maxCalories = idCalories + (20 % idCalories)

print("Calories Objective: ", idCalories)

# Caricamento tabella bounds

if sex == 'm' or sex == 'M':
    data = pd.read_csv("data/nutrientBoundMale.csv", delimiter=";")
else:
    data = pd.read_csv("data/nutrientBoundFemale.csv", delimiter=";")

# Calcolo bounds proteine


protMin, protMax, protId = proteinCalculus(age, sex)

print(data)

print(food)

# Creazione bounds nutrizionali

categories, minNutrition, maxNutrition, idealNutrition = gp.multidict({
    'Calories': [minCalories, maxCalories, idCalories],
    #'Protein': [protMin, protMax, protId],
    # 'Fat': [0, 65, 102],
    'Iron': [data['minIron'][age], data['maxIron'][age], data['idIron'][age]],
    'Calcium': [data['minCalcium'][age], data['maxCalcium'][age], data['idCalcium'][age]],
    'Sodium': [data['minSodium'][age], data['maxSodium'][age], data['idSodium'][age]],
    'Potassium': [data['minPotassium'][age], data['maxPotassium'][age], data['idPotassium'][age]],
    'Phosphorus': [data['minPhosphorus'][age], data['maxPhosphorus'][age], data['idPhosphorus'][age]],
    'Zinc': [data['minZinc'][age], data['maxZinc'][age], data['idZinc'][age]],
    'Thiamine': [data['minThiamine'][age], data['maxThiamine'][age], data['idThiamine'][age]],
    'Riboflavin': [data['minRiboflavin'][age], data['maxRiboflavin'][age], data['idRiboflavin'][age]],
    'Niacine': [data['minNiacine'][age], data['maxNiacine'][age], data['idNiacine'][age]],
    'VitC': [data['minVitC'][age], data['maxVitC'][age], data['idVitC'][age]],
    'VitB6': [data['minVitB6'][age], data['maxVitB6'][age], data['idVitB6'][age]],
    'VitB9': [data['minVitB9'][age], data['maxVitB9'][age], data['idVitB9'][age]],
    'VitA': [data['minVitA'][age], data['maxVitA'][age], data['idVitA'][age]],
    'VitE': [data['minVitE'][age], data['maxVitE'][age], data['idVitE'][age]],
    'VitD': [data['minVitD'][age], data['maxVitD'][age], data['idVitD'][age]]
})

nutritionValues = {}

for x in range(food['Descrizione'].size):
    b = {
        (food['Descrizione'][x], 'Calories'): food['Calories'][x],
        (food['Descrizione'][x], 'Tipo'): food['Tipo'][x],
        #(food['Descrizione'][x], 'Protein'): food['Proteins'][x],
        # (food['Descrizione'][x], 'Fat'): food['Fat'][x],
        (food['Descrizione'][x], 'Iron'): food['Iron'][x],
        (food['Descrizione'][x], 'Calcium'): food['Calcium'][x],
        (food['Descrizione'][x], 'Sodium'): food['Sodium'][x],
        (food['Descrizione'][x], 'Potassium'): food['Potassium'][x],
        (food['Descrizione'][x], 'Phosphorus'): food['Phosphorus'][x],
        (food['Descrizione'][x], 'Zinc'): food['Zinc'][x],
        (food['Descrizione'][x], 'Thiamine'): food['Thiamine'][x],
        (food['Descrizione'][x], 'Riboflavin'): food['Riboflavin'][x],
        (food['Descrizione'][x], 'Niacine'): food['Niacine'][x],
        (food['Descrizione'][x], 'VitC'): food['VitC'][x],
        (food['Descrizione'][x], 'VitB6'): food['VitB6'][x],
        (food['Descrizione'][x], 'VitB9'): food['VitB9'][x],
        (food['Descrizione'][x], 'VitA'): food['VitA'][x],
        (food['Descrizione'][x], 'VitE'): food['VitE'][x],
        (food['Descrizione'][x], 'VitD'): food['VitD'][x]
    }
    nutritionValues.update(b)

# Model
m = gp.Model("diet")

# Variabile di decisione acquisto del cibo
buy = m.addVars(food['Descrizione'], name="buy")
preferences = m.addVars(food['Descrizione'], name="preferences")

for i in preferences:
    preferences[i] = 0

preferences["BOVINO  MIDOLLO OSSEO      "] += 1
preferences["PASTA DI SEMOLA      "] -= 1

print(preferences)

s = m.addVars(categories, name="s")

for c in categories:
    for f in food['Descrizione']:
        nutritionValues[f, c] = str(nutritionValues[f, c]).replace(',', '.')
    idealNutrition[c] = str(idealNutrition[c]).replace(',', '.')
    minNutrition[c] = str(minNutrition[c]).replace(',', '.')
    maxNutrition[c] = str(maxNutrition[c]).replace(',', '.')
    minNutrition[c] = str(minNutrition[c]).replace('ND(0)', '0')
    minNutrition[c] = str(minNutrition[c]).replace('ND(inf)', '1000000')
    maxNutrition[c] = str(maxNutrition[c]).replace('ND(0)', '0')
    maxNutrition[c] = str(maxNutrition[c]).replace('ND(inf)',
                                                   str(float(minNutrition[c]) + 100 % float(minNutrition[c])))

# trasformazione della funzione obiettivo: soluzine temporanea in atesa di capire a pienno come usare Gurobi per
# portare la funzione obiettivo nella forma PL come pianificato nel paper.
m.update()
print(buy)

# for c in categories:
#    x = (sum(float(nutritionValues[f, c]) * (buy[f]) for f in food['Descrizione']) - float(idealNutrition[c]))
#    s.append(abs(x))

m.addConstrs(
    s[c] >= (gp.quicksum(float(nutritionValues[f, c]) * (buy[f]) for f in food['Descrizione']) - float(
        idealNutrition[c])) for c in
    categories)
m.addConstrs(
    s[c] >= -(gp.quicksum(float(nutritionValues[f, c]) * (buy[f]) for f in food['Descrizione']) - float(
        idealNutrition[c])) for c in
    categories)

# Limito le porzioni
m.addConstrs(buy[f] <= 2.5 for f in food['Descrizione'])

# Limito alimenti dannosi
m.addConstrs(buy[f] == 0 for t, f in enumerate(food['Descrizione']) if (food['Tipo'][t] == 'D'))
m.addConstr(buy['BURRO        '] <= 0.3, 'Burro')

# Forzo degli alimenti
# m.addConstr(sum(buy[f] for t, f in enumerate(food['Descrizione']) if (food['Tipo'][t] == 'CR' or food['Tipo'][t] == 'PS')) >= 0.8,
#            'Primo')

# Aggiunta bound nutrizionali

# for c in categories:
#    m.addRange(sum(nutritionValues[f, c] * buy[f] for f in food['Descrizione']),
#               float(minNutrition[c]), float(maxNutrition[c]), c)

for c in categories:
    m.addConstr(sum(nutritionValues[f, c] * buy[f] for f in food['Descrizione']) >=
                float(minNutrition[c]), c)
    m.addConstr(sum(nutritionValues[f, c] * buy[f] for f in food['Descrizione']) <=
                float(maxNutrition[c]), c)

# Funzione obiettivo
# m.setObjective(gp.quicksum(s[j] for j in s), GRB.MINIMIZE)
m.setObjective(gp.quicksum(s[j] for j in s)+gp.quicksum(buy[i]*preferences[i] for i in food['Descrizione']), GRB.MINIMIZE)



def printSolution():
    sum = {
        'Calories': 0,
        # 'Protein': 0,
        # 'Fat': 0,
        'Iron': 0,
        'Calcium': 0,
        'Sodium': 0,
        'Potassium': 0,
        'Phosphorus': 0,
        'Zinc': 0,
        'Thiamine': 0,
        'Riboflavin': 0,
        'Niacine': 0,
        'VitC': 0,
        'VitB6': 0,
        'VitB9': 0,
        'VitA': 0,
        'VitE': 0,
        'VitD': 0
    }
    if m.status == GRB.OPTIMAL:
        print('\nCost: %g' % m.objVal)
        print('\nBuy:')
        for f in food['Descrizione']:
            if buy[f].x > 0.0001:
                for c in categories:
                    sum[c] += float(nutritionValues[f, c]) * buy[f].x
                print('%s %g gr.' % (f, buy[f].x * 100))
        print('Categories: %s' % sum)

    else:
        print('No solution')


# Risoluzione
m.optimize()
printSolution()

# Rilasso vincoli se infeasible
m.feasRelaxS(0, False, False, True)
m.optimize()
printSolution()
print(s)