__author__ = 'Patricio Cerda, Joaquin Moreno y Pedro Zepeda'

import os
import copy
import random
from time import time


# Mejoras: introduccion de generador de instancias, creacion rudimentaria de menus por comandos, major overhaul de simplificacion(): ahora reemplaza por ceros, y luego elimina.
#TAL VEZ DEBO IR COPIANDO LOS CONTENIDOS DE LISTA1 SIMPLIFICADOS EN LISTA2????

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

    if alpha == '':
        recorrido.sort()
        print('La expresion es nula, y por lo tanto True. Los literales restantes (si es que sobran) pueden tomar cualquier valor de verdad.')
        print('Entonces, para que toda la expresion sea True, los siguientes atomos deben ser verdaderos:', recorrido)
        return True

    elif alpha == []:
        print('La clausula es vacia, por lo tanto la expresion es False con el recorrido:', recorrido)
        return False

    elif (len(alpha[0]) == 1) and (len(alpha) == 1):
        print('La expresion es una clausula unitaria. Hacemos que su literal sea verdadero.')
        literal_1 = alpha[0][0]
        recorrido.append(literal_1)
        return DPLL(simplificacionv2(alpha, literal_1, recorrido), recorrido)

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
    print('Asignamos valor de verdad a', literal_2, 'y se modifica el recorrido, que ahora es:', recorrido)
    if DPLL(simplificacionv2(alpha, literal_2, recorrido), recorrido):
        return True

    else:
        print('No resulto la asignacion, probamos con el valor de verdad contrario para el mismo literal.')
        #recorrido.pop()
        if literal_2 in recorrido:
            indice = recorrido.index(literal_2)
            recorrido = recorrido[:indice]
        recorrido.append(-literal_2)
        return DPLL(simplificacionv2(alpha, -literal_2, recorrido),recorrido)

def simplificacionv2(beta, literal, camino):
    alpha = copy.deepcopy(beta); largo = len(alpha)
    flag_final = False; i = 0
    if largo == 1: largo = largo + 1

    while i in range(0,largo):

        if flag_final: break
        j = 0
        try: clausula = alpha[i]
        except: i %= largo # Cambie a %=

        if clausula == 0: break
        if clausula == []: return []
        if alpha == [0]: break

        while j in range(0,len(clausula)):

            if clausula == []: return []
            if not clausula in alpha: break
            flag = False
            try: atomo = clausula[j]
            except: break

            if atomo == -literal:
                flag = True
                clausula.remove(atomo)
                if j == 3: i += 1
                if clausula == 0 or clausula == []: i += 1; break
                continue

            elif atomo == literal:
                flag = True
                alpha[i] = 0
                i += 1
                if largo == 0:
                    if abs(atomo) not in camino and atomo not in camino: camino.append(atomo)
                    return ''
                break

            elif not flag:
                if len(clausula) == 1 or j+1 == len(clausula):
                    if (i+1) <= largo: i += 1
                    else: break
            j += 1

    while True:
        c = 0
        for clausula in alpha:
            if clausula == 0:
                alpha.remove(clausula)
                c += 1
        if c == 0: break

    if alpha == []: return ''
    if alpha == [[]]: return []
    for clausula in alpha:
        if clausula == []: return []

    print('La expresion simplificada es', alpha)
    return alpha



def simplificacion(beta,literal, camino):

    alpha = copy.deepcopy(beta); largo = len(alpha)
    flag_final = False; i = 1
    if len(alpha) == 1: largo = largo + 1

    while i in range(0,largo):

        if flag_final: break
        i -= 1; j = 0
        try: clausula = alpha[i]
        except: i = i%len(alpha)

        while j in range(0,3):

            if not clausula in alpha: break
            flag = False
            try: atomo = clausula[j]
            except: break

            if atomo == -literal:
                flag = True
                clausula.remove(atomo)
                j = 0
                continue

            elif atomo == literal:
                flag = True
                alpha.remove(clausula)
                j = 1
                if len(alpha) >= 2: i += 1
                if len(alpha) == 0:
                    if abs(atomo) not in camino and atomo not in camino: camino.append(atomo)
                    return ''
                break

            elif not flag:
                if j == 1:
                    i += 2
                    if i == len(alpha)+1:
                        flag_final = True
                if j == 0 and len(clausula) == 1: break
            j += 1

    if alpha == [[]]: return []
    print('La expresion simplificada es', alpha)
    return alpha

def instanciacion(alpha, nclausulas, nliterales, pure):

    for i in range(nclausulas):
        clausula = []
        for j in range(3):
            if pure:
                try:
                    while literal in clausula or -literal in clausula:
                        literal = random.randint(1, nliterales)
                    signo = random.choice([-1,1])
                    if signo == -1: literal = -literal
                    clausula.append(literal)
                    continue
                except:
                    literal = random.randint(1, nliterales)
                    signo = random.choice([-1,1])
                    if signo == -1: literal = -literal
                    clausula.append(literal)
            else:
                literal = random.randint(1, nliterales)
                signo = random.choice([-1,1])
                if signo == -1: literal = -literal
                clausula.append(literal)
        alpha.append(clausula)

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

def exec(lista):

    casos_recorridos = []
    timer0 = time()
    print('\nExpresion a evaluar desde el archivo dado es:', lista_clausulas)
    evaluacion = DPLL(lista_clausulas, casos_recorridos)
    t_final = time() - timer0
    print('\n\nFinalmente, el DPLL retorna:', evaluacion)
    print("Tiempo", (t_final*1000)//1, 'ms')
    return

while True:

    opcion1 = str(input("\nIngrese 1 para un generador automatico de instancias, o 2 para evaluar \nalguna en particular dentro de la carpeta contenedora del programa:\n"))

    if opcion1 == "1":

        while True:
            print('\n(Para volver al menu principal, presione q.)')
            n_clausulas = input("Ingrese el numero de clausulas de la instancia a generar\n")
            if n_clausulas == 'q' or n_clausulas == 'Q': break
            n_literales = input("Ingrese el numero de literales de la instancia a generar\n")
            if n_literales == 'q' or n_literales == 'Q': break
            pureza      = input("Ingrese 1 para una instancia sin clausulas que tengan literales repetidos. Ingrese 0 para omitir esta restriccion:")
            if pureza == 'q' or pureza == 'Q': break
            if pureza == '1': puro = True
            if pureza == '0': puro = False
            instancia = []

            lista_clausulas = instanciacion(instancia, int(n_clausulas), int(n_literales), puro)
            exec(lista_clausulas)

    if opcion1 == "2":

        while True:

            print("\n(Para volver al menu principal, ingrese 'q' en cualquier momento.)")
            opcion2  = str(input("Seleccione el archivo a probar: \n"))
            if opcion2 == 'q' or opcion2 == 'Q': break
            path     = str(os.getcwd())

            try:
                r = '%s/instancia%s.txt' % (path,opcion2)
                lista_clausulas = LeerArchivo(r)
                exec(lista_clausulas)

            except:
                print("Archivo instancia%s.txt no encontrado. Intente de nuevo!" % opcion2)
                continue

    if opcion1 == 'q' or opcion1 == 'Q':
        print("Gracias por usar nuestro triple-SAT solver!")
        break