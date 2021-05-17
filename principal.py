from tkinter import *
from tkinter import messagebox
import random 
import math
import numpy as np

# globals
root = Tk()
bits = []
lSelection = []
lCrossover = []
contPob = 0

fields = (
    'Población inicial', # int
    'Población máxima', # int 
    'Tamaño de cadena de bits', # int 
    'Número de generaciones', # int
    'Rango mínimo de X', # float 
    'Rango máximo de X', # float
    'Rango mínimo de Y', # float 
    'Rango máximo de Y', # float
    'Prob de mutación de bits', # float
    'Prob de mutación de individuo' # float
)

def printList(list):
    for i in range(len(list)):
        print(list[i])

def findFitness(x, y):
    return x**2 + y**3 # z = f(x) = x² + y³

def findX(a, Dx, decimal):
    return a + (decimal * Dx)

def findY(a, Dy, decimal):
    return a + (decimal * Dy)

def crossover(inp):
    global lCrossover
    bit1 = ''
    bit2 = ''
    auxBit1 = ''
    auxBit2 = ''
    for i in range(0, len(lCrossover), 2):
        pointCrossover = random.randint(0, int(inp['Tamaño de cadena de bits'].get()))
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
    print('Sum fitness: ',totFitness)
    print('Prom fitness: ',(totFitness/len(lSelection)))
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

def inicializacion(inp):
    global bits
    global lSelection
    global contPob
    rangoX = abs(int(inp['Rango máximo de X'].get()) - int(inp['Rango mínimo de X'].get()))
    Dx = (rangoX / int(inp['Tamaño de cadena de bits'].get()))
    rangoY = abs(int(inp['Rango máximo de Y'].get()) - int(inp['Rango mínimo de Y'].get()))
    Dy = (rangoY / int(inp['Tamaño de cadena de bits'].get()))
    infoX = 'X mínimo: ', inp['Rango mínimo de X'].get(), ', X máximo: ', inp['Rango máximo de X'].get(), ', Dx: ', Dx
    infoY = 'Y mínimo: ', inp['Rango mínimo de Y'].get(), ', Y máximo: ', inp['Rango máximo de Y'].get(), ', Dy: ', Dy
    print(infoX)
    print(infoY)
    bits = createIndividuals(int(inp['Población inicial'].get()), int(inp['Tamaño de cadena de bits'].get()))
    for i in range(int(inp['Población inicial'].get())):
        auxX = findX(int(inp['Rango mínimo de X'].get()), Dx, int(bits[i],2))
        auxY = findY(int(inp['Rango mínimo de Y'].get()), Dy, int(bits[i],2))
        auxFitness = findFitness(auxX, auxY)
        dictPob = {'ID':i+1, 'bits': bits[i], 'decimal': int(bits[i], 2), 'X': auxX, 'Y': auxY, 'Fitness': auxFitness, 'Prob': 0, 'Conteo': 0}
        lSelection.append(dictPob)
        contPob += 1

def start(entries):
    inicializacion(entries)
    # iterar por generaciones
    print('------------------Selection------------------')
    evaluation(entries)
    print('------------------Crossover------------------')
    crossover(entries)

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