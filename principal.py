from tkinter import *
from tkinter import messagebox

fields = (
	'Población inicial',
	'Tamaño de cadena de bits',
	'Número de generaciones',
	'Prob de mutación de población',
	'Prob de mutación de individuo'
)

def validModelation(input):
    if input.isdigit():
        return True
    else:
        messagebox.showerror('Error en modelación', 'Se esperaba un tipo de dato: Integer')
        return False


def start(entries):
	print('Start Algorithm')

def makeform(root, fields):
    title = Label(root, text="Modelado", width=20, font=("bold",20))
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
   root = Tk()
   root.title("SGA - UPCH IA")
   root.geometry("300x300")
   root.resizable(0,0)
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e = ents: fetch(e)))
   b1 = Button(root, text = 'Iniciar',
      command=(lambda e = ents: start(e)), bg="green",fg='white')
   b1.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
   b3 = Button(root, text = 'Quit', command = root.quit, bg="red",fg='white')
   b3.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
   root.mainloop()