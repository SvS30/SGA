from tkinter import *
from tkinter import messagebox
import random 
import math
import numpy as np

# globals
root = Tk()
bits = []
individuals = []
selection = []
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

def findFitness(x, y):
    return x**2 + y**3 # z = f(x) = x² + y³

def findX(a, Dx, decimal):
    return a + (decimal * Dx)

def findY(a, Dy, decimal):
    return a + (decimal * Dy)

def printList(list):
    for i in range(len(list)):
        print(list[i])

def createIndividuals(pob, bits):
    cadena = ''
    aux = []
    for i in range(pob):
        cadena = ''
        for j in range(bits):
            cadena += str(random.randint(0,1))
        aux.append(cadena)
    return aux

def evaluation():
    global individuals
    global selection
    totFitness = 0
    promFitness = 0
    for i in range(len(individuals)):
        totFitness += individuals[i]['Fitness']
    for i in range(len(individuals)):
        individuals[i]['Prob'] = individuals[i]['Fitness'] / totFitness
    
    printList(individuals)
    print('Sum fitness: ',totFitness)
    print('Prom fitness: ',(totFitness/len(individuals)))

def inicializacion(inp):
    global bits
    global individuals
    global contPob
    rangoX = abs(int(inp['Rango máximo de X'].get()) - int(inp['Rango mínimo de X'].get()))
    Dx = (rangoX / int(inp['Tamaño de cadena de bits'].get()))
    rangoY = abs(int(inp['Rango máximo de Y'].get()) - int(inp['Rango mínimo de Y'].get()))
    Dy = (rangoY / int(inp['Tamaño de cadena de bits'].get()))
    info = 'X mínimo: ', inp['Rango mínimo de X'].get(), ', X máximo: ', inp['Rango máximo de X'].get(), ', Dx: ', Dx, ', Dy: ', Dy
    print(info)
    bits = createIndividuals(int(inp['Población inicial'].get()), int(inp['Tamaño de cadena de bits'].get()))
    for i in range(int(inp['Población inicial'].get())):
        auxX = findX(int(inp['Rango mínimo de X'].get()), Dx, int(bits[i],2))
        auxY = findY(int(inp['Rango mínimo de Y'].get()), Dy, int(bits[i],2))
        auxFitness = findFitness(auxX, auxY)
        dictPob = {'ID':i+1, 'bits': bits[i], 'decimal': int(bits[i], 2), 'X': auxX, 'Y': auxY, 'Fitness': auxFitness, 'Prob': 0, 'Conteo': 0}
        individuals.append(dictPob)
        contPob += 1

def start(entries):
    inicializacion(entries)
    evaluation()

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