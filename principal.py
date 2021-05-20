from tkinter import *
from tkinter import messagebox
import sys
import random 
import math
import numpy as np

# globals
root = Tk()
bits = []
lSelection = []
lCrossover = []
lMutation = []
lTop = []
contGen = 0
contPob = 0
contBits = 0
Dx = 0
Dy = 0

fields = (
    'Población inicial',
    'Población máxima',
    'Número de generaciones',
    'Rango mínimo de X', 
    'Rango máximo de X',
    'Rango mínimo de Y', 
    'Rango máximo de Y',
    'Error permisible',
    'Prob de mutación de bits',
    'Prob de mutación de individuo'
)

def printList(list):
    for i in range(len(list)):
        print(list[i])

def findFitness(x, y):
    return x**2 + y**3 # z = f(x) = x² + y³

def findX(a, decimal):
    global Dx
    return a + (decimal * Dx)

def findY(a, decimal):
    global Dy
    return a + (decimal * Dy)

def mutation(inp):
    global lMutation
    global contBits
    Pmi = float(inp['Prob de mutación de individuo'].get())
    Pmb = float(inp['Prob de mutación de bits'].get())
    Pm = (Pmi/100) * (Pmb/100)
    for i in range(len(lMutation)):
        bitCurrently = ''
        newBit = ''
        bitCurrently = lMutation[i]['cruzaR']
        for bit in bitCurrently:
            randomGen = (random.randint(1,100)/100)
            print('if ', randomGen, ' < ', Pm, '?')
            if randomGen < Pm:
                if bit == '1':
                    newBit += '0'
                else:
                    newBit += '1'
            else:
                newBit += bit
        print('bitCurrently: ', bitCurrently, ' Muto a -> ', newBit)
        lMutation[i]['mutaR'] = newBit
    for i in range(len(lMutation)):
        bitInd = str(lMutation[i]['mutaR'])
        lMutation[i]['decimal'] = int(bitInd, 2)
        lMutation[i]['X'] = findX(int(inp['Rango mínimo de X'].get()), int(inp['Rango máximo de X'].get()), contBits, lMutation[i]['decimal'], float(inp['Error permisible'].get()))
        lMutation[i]['Y'] = findY(int(inp['Rango mínimo de Y'].get()), int(inp['Rango máximo de Y'].get()), contBits, lMutation[i]['decimal'], float(inp['Error permisible'].get()))
        lMutation[i]['Fitness'] = findFitness(lMutation[i]['X'], lMutation[i]['Y'])
    printList(lMutation)

def crossover(inp):
    global lCrossover
    global lMutation
    global contBits
    bit1 = ''
    bit2 = ''
    auxBit1 = ''
    auxBit2 = ''
    for i in range(0, len(lCrossover), 2):
        pointCrossover = random.randint(0, contBits)
        bit1 = lCrossover[i]['bitsP'][0:pointCrossover]
        bit2 = lCrossover[i+1]['bitsP'][0:pointCrossover]
        auxBit1 = lCrossover[i]['bitsP'][pointCrossover:len(lCrossover)]
        auxBit2 = lCrossover[i+1]['bitsP'][pointCrossover:len(lCrossover)]
        bit1 = bit1 + auxBit2
        bit2 = bit2 + auxBit1
        lCrossover[i]['puntoC'] = pointCrossover
        lCrossover[i+1]['puntoC'] = pointCrossover
        lCrossover[i]['cruzaR'] = bit1
        lCrossover[i+1]['cruzaR'] = bit2
        lCrossover[i]['decimal'] = int(bit1, 2)
        lCrossover[i+1]['decimal'] = int(bit2, 2)

    for i in range(len(lCrossover)):
        position = 0
        lCrossover[i]['X'] = findX(int(inp['Rango mínimo de X'].get()), int(inp['Rango máximo de X'].get()), contBits, lCrossover[i]['decimal'], float(inp['Error permisible'].get()))
        lCrossover[i]['Y'] = findY(int(inp['Rango mínimo de Y'].get()), int(inp['Rango máximo de Y'].get()), contBits, lCrossover[i]['decimal'], float(inp['Error permisible'].get()))
        lCrossover[i]['Fitness'] = findFitness(lCrossover[i]['X'], lCrossover[i]['Y'])
        dictMut = {'ID': position+1, 'cruzaR': lCrossover[i]['cruzaR'], 'mutaR':  0, 'decimal': 0, 'X': 0, 'Y': 0, 'Fitness': 0}
        lMutation.append(dictMut)
        position += 1
    printList(lCrossover)

def selection():
    global lSelection
    global lCrossover
    position = 0
    for i in range(len(lSelection)):
        if lSelection[i]['Conteo'] != 0:
            for j in range(lSelection[i]['Conteo']):
                dictCross = {'ID':position+1, 'bitsP': lSelection[i]['bits'], 'puntoC': 0, 'cruzaR': 0, 'decimal': 0, 'X': 0, 'Y': 0, 'Fitness': 0}
                lCrossover.append(dictCross)
                position += 1

def getProbAcu(limit):
    global lSelection
    a = 0
    for i in range(0, limit, 1):
        a += lSelection[i]['Prob']
    return a

def evaluation(inp):
    global lSelection
    global contPob
    global contGen
    totFitness = 0
    promFitness = 0
    for i in range(len(lSelection)):
        totFitness += lSelection[i]['Fitness']
    for i in range(len(lSelection)):
        lSelection[i]['Prob'] = lSelection[i]['Fitness'] / totFitness
    auxPob = int(inp['Población máxima'].get()) - int(inp['Población inicial'].get())
    randNumbers = np.random.rand(auxPob)
    for i in range(len(randNumbers)):
        aux = []
        for j in range(len(lSelection)):
            if j == 0:
                aux = [0, float(lSelection[j]['Prob'])]
            else:
                prob = getProbAcu(j)
                aux = [float(prob), float((prob + lSelection[j]['Prob']))]
            if randNumbers[i] >= aux[0] and randNumbers[i] <= aux[1] and contPob <= int(inp['Población máxima'].get()):
                lSelection[j]['Conteo'] += 1
                contPob += 1
                print('Se encontro',randNumbers[i], ' en aux:',aux,'\nPoblación act: ',contPob)
                break
    printList(lSelection)
    for i in range(len(lSelection)):
        if i == 0:
            maxFitness = lSelection[0]['Fitness']
            xMax = lSelection[0]['X']
            yMax = lSelection[0]['Y']
            minFitness = lSelection[0]['Fitness']
        else:
            if maxFitness < lSelection[i]['Fitness']:
                maxFitness = lSelection[i]['Fitness']
                xMax = lSelection[i]['X']
                yMax = lSelection[i]['Y']
            if minFitness > lSelection[i]['Fitness']:
                minFitness = lSelection[i]['Fitness']
    dictTop = {'# Generation' : contGen, 'Máximo': maxFitness, 'Mínimo' : minFitness, 'Promedio' : (totFitness/len(lSelection))},
    lTop.append(dictTop)
    print('Sum fitness: ',totFitness)
    print('Prom fitness: ',(totFitness/len(lSelection)))
    print('Generation: ', contGen,' X: ', xMax,' Y:', yMax, ' maxFitness: ', maxFitness, ' minFitness: ', minFitness)
    selection()

def createIndividuals(pob, bits):
    cadena = ''
    aux = []
    for i in range(pob):
        cadena = ''
        for j in range(bits):
            cadena += str(random.randint(0,1))
        aux.append(cadena)
    return aux

def calculateY(a, b, e):
    global Dy
    rango = b - a
    delta = 2 * e
    saltos = int(rango / delta)
    aux = format(saltos, "b")
    bits = len(aux)
    Dy = rango / math.pow(2, bits)
    return bits

def calculateX(a, b, e):
    global Dx
    rango = b - a
    delta = 2 * e
    saltos = int(rango / delta)
    aux = format(saltos, "b")
    bits = len(aux)
    Dx = rango / math.pow(2, bits)
    return bits

def getBits(a, b, c, d, e):
    bitsX = calculateX(a, b, e)
    bitsY = calculateY(c, d, e)
    if bitsX > bitsY:
        return bitsX
    else:
        return bitsY

def inicializacion(inp):
    global bits
    global lSelection
    global contPob
    global contBits
    contBits = getBits(int(inp['Rango mínimo de X'].get()), int(inp['Rango máximo de X'].get()), int(inp['Rango mínimo de Y'].get()), int(inp['Rango máximo de Y'].get()), float(inp['Error permisible'].get()))
    bits = createIndividuals(int(inp['Población inicial'].get()), contBits)
    for i in range(int(inp['Población inicial'].get())):
        auxX = findX(int(inp['Rango mínimo de X'].get()), int(bits[i], 2))
        auxY = findY(int(inp['Rango mínimo de Y'].get()), int(bits[i], 2))
        dictPob = {'ID':i+1, 'bits': bits[i], 'decimal': int(bits[i], 2), 'X': auxX, 'Y': auxY, 'Fitness': findFitness(auxX, auxY), 'Prob': 0, 'Conteo': 0}
        lSelection.append(dictPob)
        contPob += 1

def start(entries):
    inicializacion(entries)
    # iterar por generaciones
    print('------------------Selection------------------')
    evaluation(entries)
    print('------------------Crossover------------------')
    crossover(entries)
    print('------------------Mutation------------------')
    mutation(entries)

def validModelation(input):
    if input.isdigit():
        return True
    else:
        messagebox.showerror('Error en modelación', 'Se esperaba un tipo de dato: Integer')
        return False

def makeform(root, fields):
    title = Label(root, text="Inicialización", width=20, font=("bold",20))
    title.pack()
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=30, text=field+": ", anchor='w')
        ent = Entry(row, validate="key", validatecommand=(row.register(validModelation), '%P'))
        row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
        lab.pack(side = LEFT)
        ent.pack(side = RIGHT, expand = YES, fill = X)
        entries[field] = ent
    return entries


if __name__ == '__main__':
    root.title("SGA - UPCH IA")
    root.geometry("300x450")
    root.resizable(0,0)
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e = ents: fetch(e)))
    b1 = Button(root, text = 'Iniciar',
       command=(lambda e = ents: start(e)), bg="green",fg='white')
    b1.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    b3 = Button(root, text = 'Quit', command = root.quit, bg="red",fg='white')
    b3.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    root.mainloop()