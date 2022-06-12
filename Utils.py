from math import cos, sin, pow
from random import randint

class Util:

  @staticmethod
  def split_informacion_grafica(data_grafica):
    """Funcion para preparar la información a graficar.

    Args:
      data_grafica (list): Lista con la información de HISTORIA_GENERACIONES.

    Returns:
      generaciones, maxs, mins, avgs (list): Listas con la información separada por generaciones, aptitudes maximas, aptitudes minimas y promedio de aptitudes.
    """
    generaciones = []
    maxs = []
    mins = []
    avgs = []
    for i in range(len(data_grafica)):
      generaciones.append(i+1)
      maxs.append(data_grafica[i]['Fitness-Max'])
      mins.append(data_grafica[i]['Fitness-Min'])
      avgs.append(data_grafica[i]['Fitness-Prom'])
    return generaciones, maxs, mins, avgs

  @staticmethod
  def inicializar_lista_mutacion(id_padre, id, bits):
    """Funcion para recolectar la información de individuos en mutación.

    Args:
      id_padre (int): ID del individuo padre.
      id (int): ID del individuo.
      bits (str): Bits del individuo.

    Returns:
      diccionario_mutacion (dict): Diccionario con información del individuo mutado.
    """
    diccionario_mutacion = {
      'ID': f"{id_padre}-{id}",
      'Genes': bits,
      'Decimal': int(bits, 2),
      'Fenotipo X': 0,
      'Fenotipo Y': 0,
      'Fitness': 0,
    }
    return diccionario_mutacion

  @staticmethod
  def realizar_mutacion(bit_a_mutar, probabilidad_mutar):
    """Funcion encargada de realizar la mutación.
    1. Generamos un número aleatorio.
    2. Evaluamos si el número aleatorio es menor que la probabilidad total.
    3. Tomamos el bit de cada individuo y cambiamos el bit a su valor opuesto.

    Args:
      bit_a_mutar (str): Bits de un individuo.
      probabilidad_mutar (float): Probabilidad de mutación total.

    Returns:
      bit_mutado (str): Cadena de bits mutado.
    """
    bit_mutado = ''
    for bit in bit_a_mutar:
      numero_random = (randint(1,100)/1000)
      if numero_random < probabilidad_mutar:
        if bit == '1':
          bit_mutado += '0'
        else:
          bit_mutado += '1'
      else:
        bit_mutado += bit
    return bit_mutado

  @staticmethod
  def obtener_probabilidad_mutacion(prob_mutacion_individuo, prob_mutacion_gen):
    """Funcion para obtener la probabilidad total.

    Args:
      prob_mutacion_individuo (float): Probabilidad de mutación del individuo (Parametro en formulario).
      prob_mutacion_gen (float): Probabilidad de mutación del gen (Parametro en formulario).

    Returns:
      probabilidad_total (float): Resultado del producto entre la probabilidad de mutación.
    """
    return prob_mutacion_individuo * prob_mutacion_gen

  @staticmethod
  def inicializar_lista_cruza(id_padre_uno, id_padre_dos, bits_cruzados_uno, bits_cruzados_dos):
    """Funcion para recolectar la información de individuos en cruza.

    Args:
      id_padre_uno (int): ID del individuo padre 1.
      id_padre_dos (int): ID del individuo padre 2.
      bits_cruzados_uno (str): Bits del individuo padre 1.
      bits_cruzados_dos (str): Bits del individuo padre 2.

    Returns:
      (dict): Diccionarios de los individuos en cruza.
    """
    diccionario_cruza_uno = {
      'ID': id_padre_uno,
      'Genes': bits_cruzados_uno,
      'Decimal': int(bits_cruzados_uno, 2),
      'Fenotipo X': 0,
      'Fenotipo Y': 0,
      'Fitness': 0,
    }
    diccionario_cruza_dos = {
      'ID': id_padre_dos,
      'Genes': bits_cruzados_dos,
      'Decimal': int(bits_cruzados_dos, 2),
      'Fenotipo X': 0,
      'Fenotipo Y': 0,
      'Fitness': 0,
    }
    return diccionario_cruza_uno, diccionario_cruza_dos

  @staticmethod
  def realizar_cruza(punto_cruza, bits_uno, bits_dos):
    """Funcion encargada de realizar la cruza.
    1. Tomamos los bits y separamos la longitud hasta el punto de cruza.
    2. Añadimos el resto de bits con los bits cruzados.

    Args:
      punto_cruza (int): Punto de cruza entre bits.
      bits_uno (str): Bits del padre uno.
      bits_dos (str): Bits del padre dos.

    Returns:
      bits_cruzados_uno (str): bits resultanes de la cruza entre padre 1 y resto de padre 2.
      bits_cruzados_dos (str): bits resultanes de la cruza entre padre 2 y resto de padre 1.
    """
    bits_cruzados_uno = ''
    bits_cruzados_dos = ''
    split_bits_uno = bits_uno[0:punto_cruza]
    split_bits_dos = bits_dos[0:punto_cruza]
    resto_bits_uno = bits_uno[punto_cruza:]
    resto_bits_dos = bits_dos[punto_cruza:]
    bits_cruzados_uno = split_bits_uno + resto_bits_dos
    bits_cruzados_dos = split_bits_dos + resto_bits_uno
    return bits_cruzados_uno, bits_cruzados_dos

  def key_to_sort(lista):
    """Funcion usada para la key de ordenación.

    Args:
      lista (list): Población actual.

    Returns:
      lista['Fitness']: Key para ordenación de población.
    """
    return lista['Fitness']

  @staticmethod
  def ordenar_poblacion_por_fitness(poblacion, orden):
    """Funcion para ordenar la población por fitness y recuperar la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      poblacion (list): Población ordenada por fitness.
    """
    poblacion.sort(key=Util.key_to_sort, reverse=orden)
    return poblacion

  def obtener_fitness_minimo(poblacion):
    """Funcion para ordenar la población por fitness ascendente y recuperar la minima de la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      poblacion[0]['Fitness'] (float): Fitness minima de la población.
    """
    poblacion.sort(key=Util.key_to_sort)
    return poblacion[0]['Fitness']

  def obtener_fitness_maximo(poblacion):
    """Funcion para ordenar la población por fitness de manera descendente y recuperar la maxima de la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      poblacion[0]['Fitness'] (float): Fitness máximo de la población.
    """
    poblacion.sort(key=Util.key_to_sort, reverse=True)
    return poblacion[0]['Fitness']

  @staticmethod
  def obtener_registro_fitness(poblacion):
    """Funcion principal para obtener la fitness minima y máxima de la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      fitness_min (float): Fitness minima de la población.
      fitness_max (float): Fitness máxima de la población.
    """
    clon_poblacion = poblacion[:]
    fitness_min = Util.obtener_fitness_minimo(clon_poblacion)
    fitness_max = Util.obtener_fitness_maximo(clon_poblacion)
    return fitness_min, fitness_max

  @staticmethod
  def calcular_fitness(x, y):
    """Funcion para calcular la aptitud de cada individuo.

    Args:
      x (float): Fenotipo X del individuo.
      y (float): Fenotipo Y del individuo.

    Returns:
      (double): Aptitud del individuo, ingresando los fenotipos en la función dada.
    """
    # y * cos(x) * sin(y) + x * cos(y) * sin(x)
    return abs(y * cos(x) * sin(y) + x * cos(y) * sin(x))

  @staticmethod
  def calcular_fenotipo(limite_inf, decimal, delta):
    """Funcion para calcular el fenotipo de cada individuo

    Args:
      limite_inf (float): Valor minimo del eje a evaluar (X,Y).
      decimal (int): Valor decimal del bit de un individuo.
      delta (float): Saltos en el eje a evaluar.

    Returns:
      (float): fenotipo del individuo.
    """
    return limite_inf + ( decimal * delta )

  @staticmethod
  def coleccionar_historial(generacion, poblacion):
    """Funcion encargada de recolectar la información para la grafica final.
    1. Obtenemos el fitness minimo y máximo de la generación.
    2. Obtenemos la suma de los fitness y obtenemos el promedio.

    Args:
      generacion (int): Generación actual.
      poblacion (list): Lista con la población actual.

    Returns:
      (dict): Diccionario que almacena los datos para graficar.
    """
    fitness_min, fitness_max = Util.obtener_registro_fitness(poblacion)
    suma_fitness = sum([ poblacion[i]['Fitness'] for i in range(len(poblacion)) ])
    prom_fitness = suma_fitness / len(poblacion)
    return {
      'Gen': generacion,
      'Fitness-Max': fitness_max,
      'Fitness-Min': fitness_min,
      'Fitness-Prom': prom_fitness
    }

  @staticmethod
  def completar_informacion_poblacion(poblacion, modelado, DELTA_X, DELTA_Y):
    """Funcion encargada de completar la información de cada individuo de la población 0.
    1. Calculamos el fenotipo X.
    2. Calculamos el fenotipo Y.
    3. Calculamos fitness.

    Args:
      poblacion (list): Lista con la población 0.
      modelado (class): Clase que almacena el modelado del algoritmo.
      DELTA_X (float): Saltos en X
      DELTA_Y (float): Saltos en Y

    Returns:
      poblacion (list): Lista de la población 0 con la información completa.
    """
    for iterador in range(len(poblacion)):
      poblacion[iterador]['Fenotipo X'] = Util.calcular_fenotipo(modelado.get_abscisa_min(), poblacion[iterador]['Decimal'], DELTA_X)
      poblacion[iterador]['Fenotipo Y'] = Util.calcular_fenotipo(modelado.get_ordenada_min(), poblacion[iterador]['Decimal'], DELTA_Y)
      poblacion[iterador]['Fitness'] = Util.calcular_fitness(poblacion[iterador]['Fenotipo X'], poblacion[iterador]['Fenotipo Y'])
    return poblacion

  @staticmethod
  def imprimir_lista( name, lista ):
    """Funcion para imprimir por consola alguna lista

    Args:
      name (string): Nombre de la lista a imprimir
      list (lista): Lista que se imprimira
    """
    print(f"==== Lista: {name}  ====")
    for i in range(len(lista)):
      print(lista[i])
    print('==== End Lista ====')

  @staticmethod
  def generar_bits_para_individuos(poblacion_inicial, numero_bits):
    """Funcion para generar los bits de la población 0.
    1. Primer ciclo para generar el numero de individuos deseados (población inicial).
    2. Segundo ciclo para generar bit por bit de manera aleatoria.

    Args:
      poblacion_inicial (int): Parametro en formulario.
      numero_bits (int): Bits a usar en la configuración del sistema.

    Returns:
      bits_individuos (list): Lista con los bits de cada individuo.
    """
    bits_individuos = []
    for i in range(poblacion_inicial):
      bits = ''
      for j in range(numero_bits):
        bits += str(randint(0,1))
      bits_individuos.append(bits)
    return bits_individuos

  @staticmethod
  def inicializar(poblacion_inicial, numero_bits):
    """Funcion para generar la población 0 del sistema.
    1. Generar bits de manera aleatoria.
    2. Generar un diccionario con la información relevante de los individuos y guardar en una lista.
    3. Actualizar conteo de población.

    Args:
      poblacion_inicial (int): Parametro en formulario.
      numero_bits (int): Bits a usar en la configuración del sistema.

    Returns:
      individuos (list): Lista de la población 0.
      conteo_poblacion (int): Conteo de la población.
    """
    conteo_poblacion = 0
    individuos = []
    bits_individuos = Util.generar_bits_para_individuos(poblacion_inicial, numero_bits)
    for iterator in range(poblacion_inicial):
      diccionario_poblacion = {
        'ID': iterator +1,
        'Genes': bits_individuos[iterator],
        'Decimal': int(bits_individuos[iterator], 2),
        'Fenotipo X': 0,
        'Fenotipo Y': 0,
        'Fitness': 0,
      }
      individuos.append(diccionario_poblacion)
      conteo_poblacion += 1
    return individuos, conteo_poblacion

  @staticmethod
  def comparar_bits( bits_x, bits_y ):
    """Funcion para comparar y decidir cuantos bits se usaran como configuración
    1. Configuración con mayor bits es más adecuada.

    Args:
      bits_x (int): Bits calculados para uso en X.
      bits_y (int): Bits calculados para uso en Y.

    Returns:
      bits_x | bits_y (int): Bits a usar en el sistema.
    """
    return (bits_x if bits_x > bits_y else bits_y)

  @staticmethod
  def estimar_bits(a_min, b_max, error_perm, delta):
    """Funcion para calcular los bits que seran los mejores para la configuración
    1. Obtenemos el rango de acción
    2. Calculamos los bits requeridos para cada configuración (X, Y)
    3. Calculamos Delta

    Args:
      a_min (float): Valor minimo del eje a evaluar (X,Y).
      b_max (float): Valor maximo del eje a evaluar (X,Y).
      error_perm (float): Error permisible.
      delta (float): Delta (X,Y)

    Returns:
      bits (int): Bits a usar con la configuración de ejes enviada.
      delta (float): Delta a usar con la configuración de ejes enviada.
    """
    rango = b_max - a_min
    delta = 2 * error_perm
    saltos = int(rango / delta)
    aux = format(saltos, "b")
    bits = len(aux)
    delta = rango / pow(2, bits)
    return bits, delta