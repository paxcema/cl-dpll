__author__ = 'Patricio Cerda, Joaquin Moreno y Pedro Zepeda'

def backtracking (s):
    if es_objetivo(s): return True
    for h in s.sucesores:
        if no_ha_sido_explorado(h):
            if backtracking(h): return True
    return False

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
    opcion = input('Seleccione el archivo a probar. Hay 20 archivos. \n')

    r = './instancia%s.txt' % opcion
    lista_clausulas = LeerArchivo(r)

    print(lista_clausulas)