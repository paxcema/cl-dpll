__author__ = 'Patricio Cerda, Joaquin Moreno y Pedro Zepeda'

import os
from time import time

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

def DPLL(alpha, recorrido):
    print('Expresion actual', alpha)
    if alpha == '': print('alpha es nada, por lo tanto True'); return True
    elif alpha == []: print('alpha es vacia, por lo tanto False'); return False
    elif (len(alpha[0]) == 1) and (alpha[0].isalpha()):
        print('alpha es clausula unitaria, por lo tanto simplificamos.') 
        literal_1 == alpha[2] # == True?
        print('Debiese asignarse True a ', literal_1)
        return DPLL(simplificacion(alpha, literal_1))
    i = 0; j = 0
    literal_2 =  alpha[i][j]
    while literal_2 in recorrido:
        try: 
            literal_2 = alpha[i][j+1]
        except: 
            try: 
                j = 0
                literal_2 = alpha[i+1][j]
            except: break
    recorrido.append(literal_2)
    print('Asigno valor de verdad a ', literal_2, 'y modifico el recorrido, que ahora es: ', recorrido)
    if DPLL(simplificacion(alpha, literal_2), recorrido) == True: 
        return True
    else: 
        print('No resulto la asignacion, probamos con el valor de verdad contrario para el mismo literal.')
        return DPLL(simplificacion(alpha, -literal_2),recorrido)

def simplificacion(alpha,literal):
    """remover clausulas in alpha donde literal es afirmativo/positivo
    remover (no literal) de clausulas donde aparece
    return new alpha"""
    i = 1
    largo = len(alpha)
    if len(alpha) == 1: largo = largo + 1
    while i in range(0,largo):
        i -= 1
        clausula = alpha[i]
        print('Alpha que entra es ', alpha)
        j = 0
        while j in range(0,2):
            atomo = clausula[j]
            print('En la clausula ', clausula, ' se tiene el atomo ', atomo)
            if atomo == -literal:
                print('Atomo opuesto, remuevo el atomo.')
                clausula.remove(atomo)
                j = 0
                continue
            if atomo == literal:
                print('Atomo igual, remuevo clausula')
                alpha.remove(clausula)
                j = 1
                if len(alpha) >= 2: i += 1
                if len(alpha) == 0: return ''
                break
            j += 1
    return alpha

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
        lista  = [valor1, valor2, valor3]
        lista_clausulas.append(lista)
        linea  = archivo.readline()
    archivo.close()
    return lista_clausulas

while True:
    opcion = input('Seleccione el archivo a probar: \n')
    path = str(os.getcwd())

    if opcion == 'q' or opcion == 'Q':
        print("Gracias por usar nuestro SAT solver!")
        break

    try:
        r = '%s/instancia%s.txt' % path,opcion
        print('r', r)
        lista_clausulas = LeerArchivo(r)

        print(lista_clausulas)

    except:
        print("Archivo instancia%s.txt no encontrado. Intente de nuevo!" % opcion)
        continue

    casos_recorridos = []

    timer0 = time()
    evaluacion = DPLL(lista_clausulas, casos_recorridos)
    t_final = time() - timer0
    print(evaluacion)
    print("Tiempo", (t_final*1000)//1, 'ms')