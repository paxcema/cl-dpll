__author__ = 'Patricio Cerda, Joaquin Moreno y Pedro Zepeda'

import os
from time import time

#Pseudocodigo y definiciones de lo que se debe hacer para optimizar el algoritmo base:
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

#En el problema 2, el recorrido despues de simplificar esta mal.


### DPLL BASICO ###

def DPLL(alpha, recorrido):
    print('\nExpresion actual', alpha)
    if alpha == '': print('Alpha es nada, por lo tanto True'); print('Para dar True, los valores a tomar para cada literal deben ser:', recorrido); return True
    elif alpha == []: print('Alpha es vacia, por lo tanto False'); return False
    elif (len(alpha[0]) == 1):
        print('Alpha es clausula unitaria, por lo tanto simplificamos.')
        literal_1 = alpha[0][0] # == True?
        print('Debiese asignarse True a ', literal_1)
        return DPLL(simplificacion(alpha, literal_1, recorrido), recorrido)
    i = 0; j = 0
    literal_2 =  alpha[i][j]
    while abs(literal_2) in recorrido:
        try: 
            literal_2 = alpha[i][j+1]
        except: 
            try: 
                j = 0
                literal_2 = alpha[i+1][j]
            except: break
    recorrido.append(literal_2)
    print('Asigno valor de verdad a', literal_2, 'y modifico el recorrido, que ahora es:', recorrido)
    if DPLL(simplificacion(alpha, literal_2, recorrido), recorrido) == True:
        return True
    else: 
        print('No resulto la asignacion, probamos con el valor de verdad contrario para el mismo literal.')
        return DPLL(simplificacion(alpha, -literal_2, recorrido),recorrido)

def simplificacion(alpha,literal, camino):
    """remueve clausulas en alpha donde el literal es afirmativo (positivo).
    Ademas, remover (no literal) de clausulas donde aparece.
    Finalmente, return new alpha"""
    flag_final = False
    i = 1
    largo = len(alpha)
    if len(alpha) == 1: largo = largo + 1
    while i in range(0,largo):
        if flag_final: break
        i -= 1
        clausula = alpha[i]
        print('Alpha a simplificar es', alpha)
        j = 0
        while j in range(0,2):
            flag = False
            atomo = clausula[j]
            print('En la clausula ', clausula, ' se tiene el atomo', atomo)
            if atomo == -literal:
                flag = True
                print('Este atomo es opuesto al literal asignado, asi que lo remuevo.')
                clausula.remove(atomo)
                j = 0
                if len(clausula) == 0: alpha.remove(clausula);break
                continue
            if atomo == literal:
                flag = True
                print('Este atomo es igual al literal asignado, asi que remuevo la clausula')
                alpha.remove(clausula)
                j = 1
                if len(alpha) >= 2: i += 1
                if len(alpha) == 0:
                    if abs(atomo) not in camino and atomo not in camino: camino.append(atomo)
                    return '' # No confundir, este no va indentado en el if del camino!!
                break
            elif not flag:
                if j == 1:
                    i += 2
                    if i == len(alpha)+1:
                        flag_final = True
                if j == 0 and len(clausula) == 1: break
            j += 1
    return alpha

def LeerArchivo(ruta):
    lista_clausulas = []
    archivo = open(ruta, 'r')
    linea   = archivo.readline()
    while linea != '' and linea != '\n':
        pos1   = linea.find(' ')
        valor1 = int(linea[:pos1])
        resto  = linea[pos1 + 1:len(linea)]
        pos2   = resto.find(' ')
        valor2 = int(resto[:pos2])
        valor3 = int(resto[pos2 +1:len(resto)])
        lista  = [valor1, valor2, valor3]
        lista_clausulas.append(lista)
        linea  = archivo.readline()
    archivo.close()
    return lista_clausulas

while True:
    opcion = str(input('Seleccione el archivo a probar: \n'))
    path = str(os.getcwd())

    if opcion == 'q' or opcion == 'Q':
        print("Gracias por usar nuestro SAT solver!")
        break

    try:
        r = '%s/instancia%s.txt' % (path,opcion)
        lista_clausulas = LeerArchivo(r)

    except:
        print("Archivo instancia%s.txt no encontrado. Intente de nuevo!" % opcion)
        continue

    casos_recorridos = []

    timer0 = time()
    evaluacion = DPLL(lista_clausulas, casos_recorridos)
    t_final = time() - timer0
    print(evaluacion)
    print("Tiempo", (t_final*1000)//1, 'ms')