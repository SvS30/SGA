from tkinter import *
from tkinter import messagebox
import random 
import math

# globals
root = Tk()
individues = []
selection = []

fields = (
    'Población inicial', # int
    'Población máxima', # int 
    'Tamaño de cadena de bits', # int 
    'Número de generaciones', # int
    'Rango mínimo de X', # float 
    'Rango máximo de X', # float
    'Prob de mutación de bits', # float
    'Prob de mutación de individuo' # float
)

def findX(a, Dx, decimal):
    return a + (decimal * Dx)

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

def inicializacion(inp):
    global individues
    global selection
    rango = abs(int(inp['Rango máximo de X'].get()) - int(inp['Rango mínimo de X'].get()))
    Dx = (rango / len(inp['Tamaño de cadena de bits']).get())
    info = 'X mínimo: ', inp['Rango mínimo de X'].get(), ', X máximo: ', inp['Rango máximo de X'].get(), ', Dx: ', Dx
    print(info)
    individues = createIndividuals(int(inp['Población inicial'].get()), int(inp['Tamaño de cadena de bits'].get()))
    for i in range(int(inp['Población inicial'].get())):
        auxX = findX(int(inp['Rango mínimo de X'].get()), Dx, int(individues[i],2))
        dictPob = {'ID':i+1, 'bits': individues[i], 'decimal': int(individues[i], 2), 'X': auxX, 'Fitness': 0}
        selection.append(dictPob)
    printList(selection)

def start(entries):
    inicializacion(entries)

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
    root.geometry("300x400")
    root.resizable(0,0)
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e = ents: fetch(e)))
    b1 = Button(root, text = 'Iniciar',
       command=(lambda e = ents: start(e)), bg="green",fg='white')
    b1.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    b3 = Button(root, text = 'Quit', command = root.quit, bg="red",fg='white')
    b3.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    root.mainloop()