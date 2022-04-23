# SGA - Algoritmo Simple Genetico.
Algoritmo tipo evolutivo y realiza un procedimiento de optimización inspirado en la teoría biológica de los genotipos o individuos, o soluciones potenciales más aptos que se utilizarán en la creación de los descendientes, con representación binaria y operadores simples basados ​​en recombinación genética y mutaciones genéticas.

Se usan procesos como lo son: **Cruza, Mutación, Clonación**. Así como también una **selección** de acuerdo con algún criterio a satisfacer (maximizar o minimizar), en función del cual se decide cuáles son los individuos más adaptados, y cuáles los menos aptos.

### Requerimientos
```
Python >= 3.8
Tkinter >= 8.6
Numpy >= 1.19.5
Matplotlib >= 3.3.4
```
De igual forma se anexo un txt con los plugins necesarios, puede instarlos con `pip install -r requerimientos.txt`.
Luego de esto, ejecuta `principal.py`.

### Función (criterio para medir la puntación de los individuos)
*z(x,y) = y &bull; cos(x) &bull; sin(y) + x &bull; cos(y) &bull; sin(x)*

### Criterio de aceptación
En esta problematica se presenta la opción de maximizar, lo que indica que nuestros mejores individuos serán los que tengan mejor puntaje evaluandolos en la función, a este puntaje se le denomina como **Fitness**.