__author__ = 'Patricio Cerda, Joaquin Moreno y Pedro Zepeda'

#Recordar definicion basica de un algoritmo con backtracking:
#
#def backtracking (s):
#    if es_objetivo(s): return True
#    for h in s.sucesores:
#        if no_ha_sido_explorado(h):
#            if backtracking(h): return True
#    return False

#Pseudocodigo de lo que se debe hacer para optimizar el algoritmo base:
#
#Unit propagation
#If a clause is a unit clause, i.e. it contains only a single unassigned literal,
#this clause can only be satisfied by assigning the necessary value to make this
#literal true. Thus, no choice is necessary. In practice, this often leads to
#deterministic cascades of units, thus avoiding a large part of the naive search space.
#
#Pure literal elimination
#If a propositional variable occurs with only one polarity in the formula, it is called
#pure. Pure literals can always be assigned in a way that makes all clauses containing
#them true. Thus, these clauses do not constrain the search anymore and can be deleted.
#
#def DPLL(lista):
#   if lista (es un set de literales consistente):
#       return true
#   if lista (contiene una clausula vacia):
#       return false
#   for (cada clausula unitaria 'l') in lista:
#***   lista = unit-propagate(l, lista)
#   for (cada literal 'l' que ocurre 'puro') in lista:
#***   lista = pure-literal-assign(l, lista)
#   l = choose-literal(lista)
#   lista1 = lista.append(l)
#   lista2 = lista.append(-l)
#   return DPLL(lista1) or DPLL(lista2)
#
#Con *** indicando los pasos a implementar para mejorar la rapidez. De wikipedia:
#
#unit-propagate(l, lista) and pure-literal-assign(l, lista) are functions that return the result of applying unit
#propagation and the pure literal rule, respectively, to the literal l and the formula ?. In other words, they
#replace every occurrence of l with "true" and every occurrence of not l with "false" in the formula ?, and
#simplify the resulting formula.

#En progreso...
#def DPLL(lista):
#    if literalidad(lista) == True: return True
#    if existeVacio(lista) == True: return False
#    for unitaria in clausulasUnitarias(lista):


def LeerArchivo(ruta):
    lista_clausulas = []
    archivo = open(ruta, 'r')
    linea   = archivo.readline()
    while linea != '':
        pos1   = linea.find(' ')
        valor1 = int(linea[:pos1])
        resto  = linea[pos1 + 1:len(linea) - 1]
        pos2   = resto.find(' ')
        valor2 = int(resto[:pos2])
        valor3 = int(resto[pos2 +1:len(resto)])
        tupla  = (valor1, valor2, valor3)
        lista_clausulas.append(tupla)
        linea  = archivo.readline()
    archivo.close()
    return lista_clausulas

while True:
    opcion = input('Seleccione el archivo a probar: \n')

    try:
        r = './instancia%s.txt' % opcion
        lista_clausulas = LeerArchivo(r)

        print(lista_clausulas)

    except:
        print("Archivo instancia%s.txt no encontrado. Intente de nuevo!" % opcion)
        continue

    #evaluacion = DPLL(lista_clausulas)