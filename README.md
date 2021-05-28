# SGA
Algoritmo Simple Genetico.
___
Se usan procesos que simulan a los de la evolución de las especies (**Cruza, Mutación**). Así como también una **selección** de acuerdo con algún criterio a satisfacer (maximizar o minimizar), en función del cual se decide cuáles son los individuos más adaptados, y cuáles los menos aptos. Estos individuos hacen referencia a un conjunto de soluciones a cualquier problema.

### Requerimientos
```
Python >= 3.6
Tkinter >= 8.6
Numpy >= 1.19.5
Matplotlib >= 3.3.4
```

### Función
*z(x,y) = y &bull; cos(x) &bull; sin(y) + x &bull; cos(y) &bull; sin(x)*

### Criterio de aceptación
En esta problematica se presenta la opción de maximizar, lo que indica que nuestros mejores individuos serán los que tengan mejor puntaje
en el **Fitness** (evaluar la función).

### Modelación
- Selección: Ruleta
  - A cada individuo se le asigna una prioridad con base al fitness.
  - Enseguida generar números aleatorios, tantos como se desee.
  - Evaluar en qué rango cae el número aleatorio generado.
  - Contar cuántos números entraron a los rangos de cada individuo.
  - Ese conteo servirá para saber el número de veces que ese individuo pasará al siguiente método.

- Cruza: Punto de cruza
  - Generando un valor aleatorio entre 1 y m-1
  	- m: número de bits por individuo
  - Seleccionar parejas de individuos
  - Intercambiar sus valores desde el punto de cruza hasta m.

- Mutación: Mutación en una etapa
  - Definiendo una probabilidad de mutación.
  - Solicitamos al usuario la Probabilidad de mutación de un individuo.
  - Solicitamos al usuario la Probabilidad de mutación de un bit.
  - Calculamos la probabilidad de mutación.
  	- *Pm = Pmi &bull; Pmb*
  	  - Pmi: Probabilidad de mutación por individuo.
  	  - Pmb: Probabilidad de mutación por bit.
  - Generar números aleatorios para cada individuo.
  - Evaluar si el número aleatorio es menor que Pm.
  - Alteración aleatoria del genotipo de un individuo (si vale 1, cambia a 0).

- Poda: Estrategia 1
  - Pasar los 2 mejores individuos a la siguiente generación
  - Eliminar las peores soluciones (individuos con peor fitness), comparando con los demás individuos.



### Inicialización
Para iniciar el algoritmo, debemos de recibir los siguientes parámetros:
- Población inicial: tipo de dato entero
- Población máxima: tipo de dato entero
- Número de generaciones: tipo de dato entero
- Rango mínimo de X: tipo de dato entero
- Rango máximo de X: tipo de dato entero
- Rango mínimo de Y: tipo de dato entero
- Rango máximo de Y: tipo de dato entero
- Error permisible: tipo de dato float (decimal)
- Probabilidad de mutación de bits: tipo de dato entero
