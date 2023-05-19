import string
from collections import deque
import pandas as pd
from typing import List


class TopDownParsing:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.terminales = {}
        self.first = {}
        self.follow = {}
        self.tabla = pd.DataFrame()
        self.LL1 = True

    def nT(self):
        pila = list(self.gramatica.keys())
        while pila:
            llave = pila.pop()
            for valor in self.gramatica.get(llave):
                for cadena in valor:
                    if cadena != "ε" and (cadena.islower() | cadena.isnumeric() | (cadena in string.punctuation)):
                        if cadena not in self.first:
                            self.first[cadena] = set()
                            self.terminales[cadena] = set()
                        self.first[cadena] = cadena
                        self.terminales[cadena] = cadena
                        if cadena not in self.follow:
                            self.follow[cadena] = set()
                        self.follow[cadena].add("NA")

    def calculateFirst(self):
        dictAux = {k: v[:] for k, v in self.gramatica.items()}
        pila = list(dictAux.keys())
        dependiente = []
        faltantes = []
        while True:
            while pila:
                llave = pila.pop()
                for valor in dictAux.get(llave):
                    if valor != "":
                        if (valor[0].islower() | valor[0].isnumeric() | (valor[0] in string.punctuation)):
                            if llave not in self.first:
                                self.first[llave] = set()
                            self.first[llave].add(valor[0])
                        elif valor[0].isupper():
                            if(valor[0] in self.first):
                                if llave not in self.first:
                                    self.first[llave] = set()
                                self.first[llave].update(
                                    list(filter(lambda v: v != 'ε', self.first.get(valor[0]))))
                            else:
                                dependiente.insert(0, llave)
                        if "ε" in valor:
                            faltantes.append(llave)
                    else:
                        self.first[llave].update("ε")

            while(dependiente):
                llave2 = dependiente.pop()
                for valor in dictAux.get(llave2):
                    if valor:
                        if(valor[0] in self.first):
                            if llave2 not in self.first:
                                self.first[llave2] = set()
                            self.first[llave2].update(
                                list(filter(lambda v: v != 'ε', self.first.get(valor[0]))))
            aux = False
            while(faltantes):
                llave = faltantes.pop()
                for key in dictAux.keys():
                    for cadena in dictAux.get(key):
                        if len(cadena) > 0 and cadena[0] == llave:
                            posicion = dictAux.get(key).index(cadena)
                            dictAux[key][posicion] = dictAux.get(key)[
                                posicion][1:]
                            pila.append(key)
                            aux = True
                        if cadena:
                            if cadena[0] in dictAux.get(key):
                                dependiente.append(key)
                if aux:
                    break
            if not pila:
                break
        return self.first

    def calculateFollow(self):
        cola = deque(self.gramatica.keys())
        indice = 0
        primero = True
        while cola:
            llave = cola.popleft()
            if primero == True:
                if llave not in self.follow:
                    self.follow[llave] = set()
                self.follow[llave].add("$")
                primero = False
            for key in self.gramatica.keys():
                for cadena in self.gramatica.get(key):
                    try:
                        longitud = len(cadena)
                        indice = cadena.index(llave)
                        siguiente = ''
                        if(indice == longitud - 1):
                            siguiente = ''
                        else:
                            siguiente = cadena[indice+1]
                        if siguiente != '':
                            if llave not in self.follow:
                                self.follow[llave] = set()
                            recorrido = deque(cadena[indice+1:])
                            while(recorrido):
                                primero1 = recorrido.popleft()
                                if 'ε' in self.first.get(primero1):
                                    self.follow[llave].update(
                                        list(filter(lambda v: v != 'ε', self.first.get(primero1))))
                                if 'ε' not in self.first.get(primero1):
                                    self.follow[llave].update(
                                        list(filter(lambda v: v != 'ε', self.first.get(primero1))))
                                    break

                        if siguiente != '' and 'ε' in self.first[siguiente]:
                            validacion = False
                            recorrido1 = deque(cadena[indice+1:])
                            while(recorrido1):
                                primero2 = recorrido1.pop()
                                if 'ε' in self.first[primero2]:
                                    validacion = True
                                if 'ε' not in self.first[primero2]:
                                    validacion = False
                                    break
                            if key not in self.follow.keys():
                                self.follow[key] = set()
                                cola.append(key)
                                cola.append(llave)
                            if llave not in self.follow:
                                self.follow[llave] = set()
                            if validacion:
                                self.follow[llave].update(self.follow[key])
                        if siguiente == '':
                            if llave not in self.follow:
                                self.follow[llave] = set()
                            if key not in self.follow.keys():
                                cola.append(key)
                                cola.append(llave)
                            if key in self.follow.keys():
                                self.follow[llave].update(self.follow[key])

                    except ValueError:
                        pass
        # return indice

    def recursionTabla(self, llave, buscado, produccion: List[str], diccionario):
        producciones = produccion
        for valor in diccionario.get(llave):
            producciones.append(valor)
            if(valor[0] != buscado):
                if valor[0].isupper() and 'ε' in self.first[valor[0]] :
                    return "1"
                if valor[0].isupper() and 'ε' not in self.first[valor[0]] :
                    return self.recursionTabla(valor[0], buscado, producciones, diccionario)
                else:
                    producciones.pop()
            if(valor[0] == buscado):
                return producciones[0]

    def calculateTabla(self):
            self.tabla = pd.DataFrame(index=list(self.gramatica.keys()), columns=list(self.terminales.keys()))
            for noTerminal in self.tabla.index:
                for terminal in self.tabla.columns:
                    auxDict = self.gramatica.copy()
                    if(terminal in self.first[noTerminal]):
                        agregado = self.recursionTabla(
                            noTerminal, terminal, [], auxDict)
                        self.tabla.at[noTerminal, terminal] = agregado
                    if('ε' in self.first[noTerminal]):
                        for valor in self.follow[noTerminal]:
                            self.tabla.at[noTerminal, valor] = 'ε'

    def firstCadena(self, cadena):
        firstC = set()
        for i in cadena:
            try:
                if i == 'ε':
                    continue
                if 'ε' not in self.first[i]:
                    firstC.update(self.first[i])
                    break
                if 'ε' in self.first[i]:
                    firstC.update(self.first[i])
            except KeyError as e:
                print(
                    "El siguiente valor puede causar errores en la ejecucion debido a que no esta definido en la gramtica: ", end="")
                print(e)
        return firstC

    def analizarCadena(self, cadena):
        proceso = pd.DataFrame(columns=['PILA', 'INPUT'])
        input = list(cadena)
        input.append("$")
        pila = list(next(iter(self.gramatica)))
        pila.append("$")
        try:
            while(pila):
                proceso.loc[len(proceso)] = [' '.join(pila), ' '.join(input)]
                if (pila[0] == input[0]):
                    pila.pop(0)
                    input.pop(0)
                    continue
                if self.tabla.loc[pila[0], input[0]] != 'ε':
                    direccion = self.tabla.loc[pila[0], input[0]]
                    direccion = direccion[::-1]
                    pila.pop(0)
                    for caracter in direccion:
                        pila.insert(0, caracter)
                    continue
                if self.tabla.loc[pila[0], input[0]] == 'ε':
                    pila.pop(0)
                    continue
            return proceso
        except KeyError:
            return "La cadena ingresada no pertenece a la gramatica "

        

    def calculateCondiciones(self):
        dictAux = {k: v[:] for k, v in self.gramatica.items()}
        pass


#a = TopDownParsing({"E": ["TA"], "A": ["+TA", "ε"],"T": ["FB"], "B": ["*FB", "ε"], "F": ["(E)", "i"]})
#a= TopDownParsing({"S":["L=R","R"],"R":["L"],"L":["*R","i"]})
#a= TopDownParsing({"S":["aaSb","cSb","b"]})
#a= TopDownParsing({"S":["aSc","B","ε"],"B":["bBc","ε"]})
#a = TopDownParsing({"A": ["BCD","Aa"], "B": ["b", "ε"],"C": ["c", "ε"], "D": ["d", "Ce"]})
# a = TopDownParsing({"S": ["ABC","i","ε"], "A": ["BC", "a"],"B": ["b", "ε"], "C": ["c"]})#first
#a= TopDownParsing({"S" :["aSb", "c"]})
#a = TopDownParsing({"R": ["EA"], "A": ["EA", "ε"],"E": ["CB"], "B": ["CB", "ε"],"C":["L","(R)"],"L":["a","b","c"]})
# a = TopDownParsing({"E": ["E+T","E-T","T"], "T": ["T*F", "T/F","F"],"F": ["(E)","n"]})# problema tabla
#a = TopDownParsing({"S": ["ABC"], "A": ["a", "ε"],"B": ["b","ε"], "C": ["c", "D"],"D":["d"]})
a = TopDownParsing({"E" : ["E+T", "T"], "T" : ["T*F", "F"], "F" : ["(E)", "i"]})

'''

a.nT()
a.calculateFirst()

print("First:")
for clave, valores in a.first.items():
    print(f"{clave} : {valores}")
    print("")
a.calculateFollow()

print("Follow:")
for clave, valores in a.follow.items():
    print(f"{clave} : {valores}")
    print("")

a.calculateTabla()
# print(a.first)
# print(a.terminales)
print(a.tabla)
print(a.firstCadena("BPε"))
print(a.analizarCadena("a"))
# print(a.gramatica)'''



