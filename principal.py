from Graficos import Grafico
from Modelado import Modelo
from Utils import Util
from tkinter import Tk, Button, LEFT, YES
from random import shuffle, randint

# Globales
DELTA_X = 0
DELTA_Y = 0
CONTEO_POBLACION = 0
HISTORIA_GENERACIONES = []

def poda(sobrepoblacion, poblacion_inicial, poblacion_final):
  """Funcion simulando la poda para una nueva generacion.
  1. Juntamos la poblacion inicial con la población cruzada y mutada en un arreglo.
  2. Ordenamos la poblacion final por aptitud de manera descendente (Util.sort_poblacion_by_aptitud:L85).
  3. Estimamos la sobrepoblacion y removemos de la poblacion a los menos aptos (peor aptitud) (L45).
  4. Actualizamos el conteo de población.

  Args:
    sobrepoblacion (int): Residuo entre la poblacion actual y la poblacion maxima.
    poblacion_inicial (list): Población inicial de generación
    poblacion_final (list): Población luego de cruzarse y mutar.

  Returns:
      list: Nueva población para siguiente generación
  """
  global CONTEO_POBLACION
  poblacion_total = []
  poblacion_total.extend(poblacion_inicial)
  poblacion_total.extend(poblacion_final)
  poblacion_total = Util.ordenar_poblacion_por_fitness(poblacion_total, True)
  print(f"Soprepoblacion: {sobrepoblacion}") 
  [ poblacion_total.pop() for i in range(sobrepoblacion) ]
  CONTEO_POBLACION = len(poblacion_total)
  Util.imprimir_lista('Poblacion podada', poblacion_total)
  return poblacion_total

def mutacion(modelado, poblacion):
  """Funcion simulando la mutación de bits en un individuo.
  1. Calculamos la probabilidad de mutación total.
  2. Realizamos la mutación (Util.realizar_mutacion:L32).
  3. Guardamos información nueva de los individuos.
  4. Actualizamos conteo de población

  Args:
    modelado (class): Clase con el modelado del programa
    poblacion (list): Población a mutar

  Returns:
    list:  Lista con la población después de mutar.
  """
  global DELTA_X
  global DELTA_Y
  global CONTEO_POBLACION
  poblacion_mutada = []
  prob_mutacion_total = Util.obtener_probabilidad_mutacion(modelado.get_mutacion_individuo(), modelado.get_mutacion_gen())
  for iterador in range(len(poblacion)):
    bit_cruzado = poblacion[iterador]['Genes']
    bit_mutado = Util.realizar_mutacion(bit_cruzado, prob_mutacion_total)
    print(f"Bits mutados: [{bit_cruzado}] -> [{bit_mutado}]")
    diccionario_mutacion = Util.inicializar_lista_mutacion(poblacion[iterador]['ID'], iterador+1, bit_mutado)
    poblacion_mutada.append(diccionario_mutacion)
    CONTEO_POBLACION += 1
  poblacion_mutada = Util.completar_informacion_poblacion(poblacion_mutada, modelado, DELTA_X, DELTA_Y)
  Util.imprimir_lista('Poblacion mutada', poblacion_mutada)
  return poblacion_mutada

def cruza(modelado, poblacion, total_bits):
  """Funcion simulando la cruza entre individuos.
  1. Clonamos la lista de población.
  2. Ordenamos aleatoriamente la lista (shuffle():L84).
  3. Realizamos cruza entre parejas (Util.realizar_cruza:L70).
  4. Guardamos información nueva de los individuos.

  Args:
    modelado (class): Clase con el modelado del programa
    poblacion (list): Población a cruzar
    total_bits (int): Bits a usar en el sistema

  Returns:
    list: Lista con la población después de cruzar entre parejas aleatoriamente
  """
  global DELTA_X
  global DELTA_Y
  clon_poblacion = poblacion[:]
  shuffle(clon_poblacion)
  poblacion_cruzada = []
  for i in range(0, len(clon_poblacion), 2):
    punto_cruza = randint(1, total_bits-1)
    bits_cruzados_uno, bits_cruzados_dos = Util.realizar_cruza(punto_cruza, clon_poblacion[i]['Genes'], clon_poblacion[i+1]['Genes'])
    print(f"Punto de cruza: {punto_cruza}\nA: [{clon_poblacion[i]['Genes']}] -> [{bits_cruzados_uno}]\nB: [{clon_poblacion[i+1]['Genes']}] -> [{bits_cruzados_dos}]")
    diccionario_mutacion_uno, diccionario_mutacion_dos = Util.inicializar_lista_cruza(clon_poblacion[i]['ID'], clon_poblacion[i+1]['ID'], bits_cruzados_uno, bits_cruzados_dos)
    poblacion_cruzada.append(diccionario_mutacion_uno)
    poblacion_cruzada.append(diccionario_mutacion_dos)
  poblacion_cruzada = Util.completar_informacion_poblacion(poblacion_cruzada, modelado, DELTA_X, DELTA_Y)
  Util.imprimir_lista('Poblacion cruzada', poblacion_cruzada)
  return poblacion_cruzada

def competencia(generacion, poblacion, modelado):
  """Funcion simulando la competencia entre individuos
  1. Completamos la información de los individuos.
  2. Recolectamos la información para la grafica.

  Args:
    generacion (int): Generacion en la que va el programa
    poblacion (list): Población por enviar a competencia
    modelado (class): Clase con el modelado del programa

  Returns:
    list: Lista con información completa de los individuos a competir
  """
  global DELTA_X
  global DELTA_Y
  global HISTORIA_GENERACIONES
  if poblacion[0]['Fitness'] == 0:
    poblacion = Util.completar_informacion_poblacion(poblacion, modelado, DELTA_X, DELTA_Y)
  Util.imprimir_lista(f"Poblacion Gen: {generacion}", poblacion)
  diccionario_generacion = Util.coleccionar_historial(generacion, poblacion)
  HISTORIA_GENERACIONES.append(diccionario_generacion)
  Util.imprimir_lista(f"Mejores Resultados", HISTORIA_GENERACIONES)
  return poblacion

def clonacion(poblacion):
  """Funcion simulando la clonacion del ultimo individuo si la población fuese impar

  Args:
    poblacion (list): Lista de población

  Returns:
    list: Población modificada con un clon
  """
  poblacion.append(poblacion[-1])
  return poblacion

def iniciar_algoritmo(modelado):
  """Funcion para preparar y inicializar el algoritmo

  Args:
    modelado (class): Clase que almacena el modelado del algoritmo

  Procesos:
    - Definir cuantos bits se usaran
    - Generar poblacion inicial
    - Iteracion por generaciones
    - Llamar a los procesos evolutivos (clonacion, competencia, cruza, mutacion, poda)
    - Llamar a funcion de graficar
  """
  global DELTA_X
  global DELTA_Y
  global CONTEO_POBLACION
  global HISTORIA_GENERACIONES
  print('==== Starting ====')
  bits_en_x, DELTA_X = Util.estimar_bits(modelado.get_abscisa_min(), modelado.get_abscisa_max(), modelado.get_error_perm(), DELTA_X)
  bits_en_y, DELTA_Y = Util.estimar_bits(modelado.get_ordenada_min(), modelado.get_ordenada_max(), modelado.get_error_perm(), DELTA_Y)
  print('bits X:', bits_en_x, ' Delta X: ', DELTA_X)
  print('bits Y:', bits_en_y, ' Delta Y: ', DELTA_Y)
  bits_a_usar = Util.comparar_bits(bits_en_x, bits_en_y)
  print('Los bits a usar seran:', bits_a_usar)
  poblacion, CONTEO_POBLACION = Util.inicializar(modelado.get_poblacion_inicial(), bits_a_usar)
  for generacion in range(modelado.get_generaciones()):
    if len(poblacion) % 2 != 0:
      poblacion = clonacion(poblacion)
    individuos_competencia = competencia(generacion, poblacion, modelado)
    individuos_cruzados = cruza(modelado, individuos_competencia, bits_a_usar)
    individuos_mutados = mutacion(modelado, individuos_cruzados)
    if CONTEO_POBLACION > modelado.get_poblacion_maxima():
      sobrepoblacion = CONTEO_POBLACION - modelado.get_poblacion_maxima()
      poblacion = poda(sobrepoblacion, individuos_competencia, individuos_mutados)
  generaciones, maxs, mins, avgs = Util.split_informacion_grafica(HISTORIA_GENERACIONES)
  Grafico.make_chart(generaciones, maxs, mins, avgs)

def cargar_configuracion(inputs):
  """Funcion encargada de guardar el modelado del algoritmo

  Args:
    inputs (list): Campos solicitados en el formulario inicial.
  """
  configuracion = {
    'pob_ini': int(inputs["Población inicial"].get()),
    'pob_max': int(inputs["Población máxima"].get()),
    'generaciones': int(inputs["Generaciones"].get()),
    'abscisa_min': float(inputs["Eje mínimo de X"].get()),
    'abscisa_max': float(inputs["Eje máximo de X"].get()),
    'ordenada_min': float(inputs["Eje mínimo de Y"].get()),
    'ordenada_max': float(inputs["Eje máximo de Y"].get()),
    'error_perm': float(inputs["Error permisible"].get()),
    'mutacion_gen': int(inputs["Probabilidad de mutación de bit"].get()),
    'mutacion_individuo': int(inputs["Probabilidad de mutación de individuo"].get())
  }
  modelado = Modelo(configuracion)
  iniciar_algoritmo(modelado)

if __name__ == '__main__':
  """Funcion main para crear la ventana inicial.
  """
  ventana = Tk()
  ventana.title("SGA - IA")
  ventana.resizable(0,0)
  entries = Grafico.crear_formulario(ventana)
  btn1 = Button(ventana, text = 'Iniciar',
    command=(lambda e=entries: cargar_configuracion(e)), bg="green",fg='white')
  btn1.pack(side = LEFT, pady = 5, expand = YES)
  btn2 = Button(ventana, text = 'Quitar', command = ventana.quit, bg="red",fg='white')
  btn2.pack(side = LEFT, pady = 5, expand = YES)
  ventana.mainloop()