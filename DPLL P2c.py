__author__ = 'Patricio Cerda, Joaquin Moreno y Pedro Zepeda'

import os
import copy
import random
from time import time

# Para el basebase mostrar el DPLL 1 sin la funcion de simplificacion (y sin el caso base de clausula unitaria, parece).
# Eso es fuerza bruta. Luego el DPLL1, luego el DPLL2.


### DPLL MEJORADO ###

def tautologia(alpha):
    # Aplica la ley de la tautologia. Esto es, elimina clausulas que posean dentro de ellas literales complementarios.
    # Aplicada solo una vez, y al comienzo.
    global eleccion, counter

    i = 0
    while i in range(0, len(alpha)):
        clausula = alpha[i]
        lista = []
        for atomo in clausula:
            if -atomo in lista:
                alpha.remove(clausula)
                counter += 1
                if abs(atomo) not in eleccion: eleccion.append(abs(atomo))
                i -= 1
                break
            if atomo not in lista: lista.append(atomo)
        i += 1
    return alpha

def unit(alpha):
    # Contador de clausulas unitarias en alpha.
    if alpha == '' or alpha == []: return 0
    c = 0
    for clausula in alpha:
        if len(clausula) == 1: c += 1
    return c

def puros(alpha):
    # Contador de literales puros en alpha. Se le dice puro al literal que aparece solo con un signo a lo largo de tod alpha.
    lista_puros = []; lista_impuros = []
    if alpha == '' or alpha == []: return []
    for clausula in alpha:
        for atomo in clausula:
            if abs(atomo) in lista_impuros: continue
            if -atomo in lista_puros:
                lista_puros.remove(-atomo)
                lista_impuros.append(abs(atomo))
                continue
            if atomo not in lista_puros: lista_puros.append(atomo)
    return lista_puros

def purelit(alpha, camino):
    # Regla del literal puro

    global counter, show

    if alpha == [] or alpha == [[]]: return alpha, camino

    while len(puros(alpha)) >= 1:
        puro = puros(alpha)[0]; i = 0
        if puro not in camino: camino.append(puro)
        while i in range(0, len(alpha)):
            if puro in alpha[i]:
                alpha.remove(alpha[i])
                counter += 1
            else: i += 1
    if show:
        print("Por regla del literal puro, la expresion queda:")
        print(alpha)
    if alpha == []: alpha = ''
    if alpha == [[]]: alpha = []

    return alpha, camino


def DPLL(alpha,recorrido):
    global eleccion, show, counter

    # Nueva tecnica

    try: alpha, recorrido = purelit(alpha, recorrido)
    except: pass

    # Casos Base

    if alpha == '':
        recorrido.sort()
        if show: print('La expresion es nula, y por lo tanto True. Los literales restantes (no especificados) pueden tomar cualquier valor de verdad.')
        if show: print('Entonces, para que toda la expresion sea True, los siguientes atomos deben ser verdaderos:', recorrido)
        eleccion.append(recorrido)
        return True

    elif alpha == []:
        if show: print('La clausula es vacia, por lo tanto la expresion es False con el recorrido:', recorrido)
        return False

    # Regla de la bifurcacion

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
    if show: print('Asignamos valor de verdad a', literal_2, 'y se modifica el recorrido, que ahora es:', recorrido)
    if DPLL(simplificacionv2(alpha, literal_2, recorrido), recorrido):
        eleccion = recorrido
        return True

    else:
        if show: print('No resulto la asignacion, probamos con el valor de verdad contrario para el mismo literal.')
        if literal_2 in recorrido:
            indice = recorrido.index(literal_2)
            recorrido = recorrido[:indice]
        recorrido.append(-literal_2)
        return DPLL(simplificacionv2(alpha, -literal_2, recorrido),recorrido)


def simplificacionv2(beta, literal, camino):

    global counter
    alpha = copy.deepcopy(beta)
    largo = len(alpha); i = 0
    if largo == 1: largo += 1

    # Simplificacion original

    while i in range(0,largo):

        j = 0
        try: clausula = alpha[i]
        except: i %= largo

        if clausula == 0: break
        if clausula == []: return []
        if alpha == [0]: break

        while j in range(0,len(clausula)):

            if clausula == []: return []
            if not clausula in alpha: break
            try: atomo = clausula[j]
            except: break

            if atomo == -literal:
                clausula.remove(atomo)
                counter += 1
                if j == 3: i += 1
                if clausula == 0 or clausula == []: i += 1; break
                continue

            elif atomo == literal:
                alpha[i] = 0
                i += 1
                counter += 1
                if largo == 0:
                    if (abs(atomo) not in camino) and (atomo not in camino): camino.append(atomo)
                    return ''
                break

            else:
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

    if show: print('La expresion simplificada es', alpha)
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

    global eleccion, show
    casos_recorridos = []
    timer0 = time()
    #if show:
    print('\nExpresion a evaluar desde el archivo dado es:', lista)
    evaluacion = DPLL(tautologia(lista), casos_recorridos)
    t_final = time() - timer0
    #if show:
    print('\n\nEl DPLL retorna:', evaluacion)
    if evaluacion:# and show:
        print("El camino a tomar sera:", eleccion)
    # if show:
    print("Tiempo:", (t_final*1000)//1, 'ms')
    if not show:
        return [(t_final*1000)//1, evaluacion]
    return

while True:

    print("\nBienvenido al triple-SAT solver mejorado!")
    imprimir = input("\nIngrese 2 para probar variacion de parametros, 1 si desea obtener una descripcion del proceso de evaluacion, o un 0 si prefiere omitirlo. Esto ultimo es recomendable en caso de evaluar instancias muy complejas!\n")
    if imprimir == '2':
        show = False
        while True:
            choice = input("\n(Se asume que no existen literales repetidos dentro de cada clausula).\n1 para variar numero de clausulas, 2 para variar numero de literales:\n")

            if choice == '1':
                fijo = int(input("Numero fijo de literales:\n"))
                index1 = int(input("Cantidad inicial de clausulas:\n"))
                index2 = int(input("Cantidad final de clausulas:\n"))

            if choice == '2':
                fijo = int(input("Numero fijo de clausulas:\n"))
                index1 = int(input("Cantidad inicial de literales:\n"))
                index2 = int(input("Cantidad final de literales:\n"))

            repeticiones = int(input("Repeticiones por cada estado:\n"))
            salto = int(input("Salto de la variable por cada iteracion:\n"))
            lista_final = []

            for i in range(index1,index2+1,salto):

                lista_resultadosTrue = []
                lista_resultadosFalse = []

                for j in range(0,repeticiones):

                    counter = 0; eleccion = []; instancia = []
                    if choice == '1': lista_clausulas = instanciacion(instancia, i, fijo, True)
                    if choice == '2': lista_clausulas = instanciacion(instancia, fijo, i, True)
                    tiempo, valor = exec(lista_clausulas)
                    tupla = (tiempo, valor, counter, eleccion)
                    if tupla[1]: lista_resultadosTrue.append([tupla, lista_clausulas])
                    else: lista_resultadosFalse.append([tupla, lista_clausulas])

                suma_t = 0; suma_operaciones = 0; suma_v = 0; aux1 = []; aux2 = []
                for lista in [lista_resultadosTrue, lista_resultadosFalse]:

                    for resultado in lista:
                        suma_t += resultado[0][0]
                        if resultado[0][1]: suma_v += 1
                        suma_operaciones += resultado[0][2]

                    t_promedio = suma_t//repeticiones
                    op_promedio = suma_operaciones//repeticiones
                    if choice == '1': tupla2 = (t_promedio, op_promedio, suma_v, i, fijo)
                    else:             tupla2 = (t_promedio, op_promedio, suma_v, fijo, i)
                    if lista == lista_resultadosTrue: aux1.append(tupla2)
                    else: aux2.append(tupla2)

                for i in range(0,len(aux1)):
                    tupla = [aux1[i], aux2[i]]
                    lista_final.append(tupla)
            print()
            for resultado in lista_final:
                print("####\nPara", resultado[0][3], "clausulas de", resultado[0][4], "literales, se ejecuto el programa", repeticiones, "veces, con", resultado[0][2], "instancias satisfacibles, obteniendo:")

                if resultado[0][2] > 0:
                    print("Para las instancias satisfacibles:")
                    print("Tiempo de ejecucion promedio:", resultado[0][0], "ms , y numero de operaciones promedio:", resultado[0][1], "\n####\n ")

                if repeticiones - resultado[0][2] > 0:
                    print("Para las instancias no satisfacibles:")
                    print("Tiempo de ejecucion promedio:", resultado[1][0], "ms , y numero de operaciones promedio:", resultado[1][1], "\n####\n ")

    else:
        opcion1 = str(input("\nIngrese 1 para un generador automatico de instancias, o 2 para evaluar \nalguna en particular dentro de la carpeta contenedora del programa:\n"))
        if imprimir == '1': show = True
        if imprimir == '0': show = False

        if opcion1 == "1":

            while True:
                counter = 0; eleccion = []
                print('\n(Para volver al menu principal, presione q.)')
                n_clausulas = input("Ingrese el numero de clausulas de la instancia a generar\n")
                if n_clausulas == 'q' or n_clausulas == 'Q': break
                n_literales = input("Ingrese el numero de literales de la instancia a generar\n")
                if n_literales == 'q' or n_literales == 'Q': break
                pureza = input("Ingrese 1 para una instancia sin clausulas que tengan literales repetidos. Ingrese 0 para omitir esta restriccion:\n")
                if pureza == '1': puro = True
                if pureza == '0': puro = False
                if pureza == 'q' or pureza == 'Q': break

                instancia = []

                lista_clausulas = instanciacion(instancia, int(n_clausulas), int(n_literales), puro)
                exec(lista_clausulas)
                print("Numero de operaciones:", counter)

        if opcion1 == "2":

            while True:
                counter = 0; eleccion = []
                print("\n(Para volver al menu principal, ingrese 'q' en cualquier momento.)")
                opcion2 = str(input("Seleccione el archivo a probar: \n"))
                if opcion2 == 'q' or opcion2 == 'Q': break
                path = str(os.getcwd())

                try:
                    r = '%s/instancia%s.txt' % (path,opcion2)
                    lista_clausulas = LeerArchivo(r)
                    exec(lista_clausulas)
                    print("Numero de operaciones:", counter)

                except:
                    print("Archivo instancia%s.txt no encontrado. Intente de nuevo!" % opcion2)
                    continue

        if opcion1 == 'q' or opcion1 == 'Q':
            print("Gracias por usar nuestro triple-SAT solver!")
            break