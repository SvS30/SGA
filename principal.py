from tkinter import *
from tkinter import messagebox
import sys
import random 
import math
import numpy as np
import matplotlib.pyplot as plot

# globals
root = Tk()
bits = []
lSelection = []
lCrossover = []
lMutation = []
lTop = []
lGenerations = []
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
    a = y * math.cos(x) * math.sin(y)
    b = x * math.cos(y) * math.sin(x)
    return abs(a + b)

def findX(a, decimal):
    global Dx
    return a + (decimal * Dx)

def findY(a, decimal):
    global Dy
    return a + (decimal * Dy)

def poda(pob):
    global lSelection
    global lGenerations
    global contPob
    for i in range(pob):
        if lGenerations[i]['fitnessH'] > lGenerations[i]['fitnessP']:
            dictSel = {'ID': i+1, 'bits': lGenerations[i]['bitsH'], 'decimal': int(lGenerations[i]['bitsH'], 2), 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Conteo': 0}
        else:
            dictSel = {'ID': i+1, 'bits': lGenerations[i]['bitsP'], 'decimal': int(lGenerations[i]['bitsP'], 2), 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Conteo': 0}
        lSelection.append(dictSel)
        contPob += 1
    print('------------------ Poda #', contGen+1, ' ------------------')
    printList(lGenerations)
    lGenerations.clear()

def cleanLists():
    global lSelection
    global lCrossover
    global lMutation
    global contPob
    lSelection.clear()
    lCrossover.clear()
    lMutation.clear()
    contPob = 0

def mutation(inp):
    global lMutation
    global lGenerations
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
            # print('if ', randomGen, ' < ', Pm, '?')
            if randomGen < Pm:
                if bit == '1':
                    newBit += '0'
                else:
                    newBit += '1'
            else:
                newBit += bit
        # print('bitCurrently: ', bitCurrently, ' Muto a -> ', newBit)
        lMutation[i]['mutaR'] = newBit
    for i in range(len(lMutation)):
        bitInd = str(lMutation[i]['mutaR'])
        lMutation[i]['decimal'] = int(bitInd, 2)
        lMutation[i]['X'] = findX(int(inp['Rango mínimo de X'].get()), lMutation[i]['decimal'])
        lMutation[i]['Y'] = findY(int(inp['Rango mínimo de Y'].get()), lMutation[i]['decimal'])
        lMutation[i]['Fitness'] = findFitness(lMutation[i]['X'], lMutation[i]['Y'])
        lGenerations[i]['bitsH'] = lMutation[i]['mutaR']
        lGenerations[i]['fitnessH'] = lMutation[i]['Fitness']
        if lGenerations[i]['fitnessH'] > lGenerations[i]['fitnessP']:
            lGenerations[i]['fitnessM'] = lGenerations[i]['fitnessH']
            lGenerations[i]['bitsM'] = lGenerations[i]['bitsH']
        else:
            lGenerations[i]['fitnessM'] = lGenerations[i]['fitnessP']
            lGenerations[i]['bitsM'] = lGenerations[i]['bitsP']
    printList(lMutation)
    cleanLists()
    poda(int(inp['Población inicial'].get()))

def crossover(inp):
    global lCrossover
    global lMutation
    global contBits
    bit1 = ''
    bit2 = ''
    auxBit1 = ''
    auxBit2 = ''
    position = 0
    for i in range(0, len(lCrossover), 2):
        pointCrossover = random.randint(1, contBits-1)
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
        lCrossover[i]['X'] = findX(int(inp['Rango mínimo de X'].get()), lCrossover[i]['decimal'])
        lCrossover[i]['Y'] = findY(int(inp['Rango mínimo de Y'].get()), lCrossover[i]['decimal'])
        lCrossover[i]['Fitness'] = findFitness(lCrossover[i]['X'], lCrossover[i]['Y'])
        dictMut = {'ID': position+1, 'cruzaR': lCrossover[i]['cruzaR'], 'mutaR':  0, 'decimal': 0, 'X': 0, 'Y': 0, 'Fitness': 0}
        lMutation.append(dictMut)
        position += 1
    printList(lCrossover)

def selection():
    global lSelection
    global lCrossover
    global lGenerations
    position = 0
    for i in range(len(lSelection)):
        if lSelection[i]['Conteo'] != 0:
            for j in range(lSelection[i]['Conteo']):
                dictCross = {'ID':position+1, 'bitsP': lSelection[i]['bits'], 'puntoC': 0, 'cruzaR': 0, 'decimal': 0, 'X': 0, 'Y': 0, 'Fitness': 0}
                lCrossover.append(dictCross)
                dictGeneration = {'ID': position+1, 'bitsP': lSelection[i]['bits'], 'fitnessP': lSelection[i]['Fitness'], 'bitsH': 0, 'fitnessH': 0, 'fitnessM': 0, 'bitsM': 0}
                lGenerations.append(dictGeneration)
                position += 1

def getFitnessMaxSelec():
    global lSelection
    maximo = 0
    position = 0
    for i in range(len(lSelection)):
        if i == 0:
            maximo = lSelection[i]['Fitness']
        else:
            if maximo < lSelection[i]['Fitness']:
                maximo = lSelection[i]['Fitness']
                position = i
    return position

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
    contadorPob = 0
    for i in range(len(lSelection)):
        lSelection[i]['X'] = findX(int(inp['Rango mínimo de X'].get()), int(lSelection[i]['bits'], 2))
        lSelection[i]['Y'] = findY(int(inp['Rango mínimo de Y'].get()), int(lSelection[i]['bits'], 2))
        lSelection[i]['Fitness'] = findFitness(lSelection[i]['X'], lSelection[i]['Y'])
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
            if randNumbers[i] >= aux[0] and randNumbers[i] <= aux[1] and contadorPob <= int(inp['Población inicial'].get()):
                if contadorPob < (int(inp['Población inicial'].get())-1):
                    # print('Se encontro',randNumbers[i], ' en aux:',aux,'\nPoblación act: ',contPob)
                    lSelection[j]['Conteo'] += 1
                    contPob += 1
                    contadorPob += 1
                    break
                else:
                    pos = getFitnessMaxSelec()
                    lSelection[pos]['Conteo'] += 1
                    contPob += 1
                    contadorPob += 1
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
    dictTop = {'# Generation' : contGen+1, 'Máximo': maxFitness, 'Mínimo' : minFitness, 'Promedio' : (totFitness/len(lSelection))}
    lTop.append(dictTop)
    print('Sum fitness: ',totFitness)
    print('Prom fitness: ',(totFitness/len(lSelection)))
    print('Generation: ', contGen+1,' X: ', xMax,' Y:', yMax, ' maxFitness: ', maxFitness, ' minFitness: ', minFitness)
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
    print('Y usara ', bits, ' bits\nDy: ', Dy)
    return bits

def calculateX(a, b, e):
    global Dx
    rango = b - a
    delta = 2 * e
    saltos = int(rango / delta)
    aux = format(saltos, "b")
    bits = len(aux)
    Dx = rango / math.pow(2, bits)
    print('X usara ', bits, ' bits\nDx: ', Dx)
    return bits

def getBits(a, b, c, d, e):
    bitsX = calculateX(a, b, e)
    bitsY = calculateY(c, d, e)
    if bitsX > bitsY:
        print('Se usaran ', bitsX, ' bits')
        return bitsX
    else:
        print('Se usaran ', bitsY, ' bits')
        return bitsY

def inicializacion(inp):
    global bits
    global lSelection
    global contPob
    global contBits
    contBits = getBits(int(inp['Rango mínimo de X'].get()), int(inp['Rango máximo de X'].get()), int(inp['Rango mínimo de Y'].get()), int(inp['Rango máximo de Y'].get()), float(inp['Error permisible'].get()))
    bits = createIndividuals(int(inp['Población inicial'].get()), contBits)
    for i in range(int(inp['Población inicial'].get())):
        dictPob = {'ID':i+1, 'bits': bits[i], 'decimal': int(bits[i], 2), 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Conteo': 0}
        lSelection.append(dictPob)
        contPob += 1

def getFitnessMax():
    global lTop
    maximo = 0
    for i in range(len(lTop)):
        if i == 0:
            maximo = lTop[i]['Máximo']
        else:
            if maximo < lTop[i]['Máximo']:
                maximo = lTop[i]['Máximo']
    return maximo

def grafica1(inp):
    global lTop
    maxs = []
    mins = []
    proms = []
    generations = []
    
    for i in range(int(inp['Número de generaciones'].get())):
        maxs.append(lTop[i]['Máximo'])
        mins.append(lTop[i]['Mínimo'])
        proms.append(lTop[i]['Promedio'])
        generations.append(i+1)
    plot.plot(generations, maxs, 'b-x', linewidth=2, label="Máximos")
    plot.plot(generations, mins, 'r-o', linewidth=2, label="Mínimos")
    plot.plot(generations, proms, 'g-s', linewidth=2, label="Promedio")
    plot.legend(loc='lower right')
    plot.xlabel('Generaciones')
    plot.ylabel('Fitness')
    plot.title("Evolución del Fitness")
    plot.grid()
    plot.show()


def start(entries):
    global lTop
    global contGen
    inicializacion(entries)
    # iterar por generaciones
    for i in range(int(entries['Número de generaciones'].get())):
        print('------------------ Selection #', i+1, ' ------------------')
        evaluation(entries)
        print('------------------ Crossover #', i+1, ' ------------------')
        crossover(entries)
        print('------------------ Mutation #', i+1, ' ------------------')
        mutation(entries)
        contGen += 1
    print('------------------ Mejores Resultados ------------------')
    printList(lTop)
    grafica1(entries)
    fitnessMax = getFitnessMax()
    messagebox.showinfo('Mejor fitness de todas las generaciones', fitnessMax)

def validModelation(input):
    try:
        float(input)
        return True
    except:
        return False
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