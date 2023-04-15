import string
from collections import deque


class TopDownParsing:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.first = {}
        self.follow = {}

    def nT(self):
        pila = list(self.gramatica.keys())
        while pila:
            llave = pila.pop()
            for valor in self.gramatica.get(llave):
                for cadena in valor:
                    if cadena != "ε" and (cadena.islower() | cadena.isnumeric() | (cadena in string.punctuation)):
                        if cadena not in self.first:
                            self.first[cadena] = set()
                        self.first[cadena].add(cadena)
                        if cadena not in self.follow:
                            self.follow[cadena] = set()
                        self.follow[cadena].add("NA")

    def calculateFirst(self):
        dictAux = self.gramatica
        pila = list(dictAux.keys())
        dependiente = []
        faltantes = []
        while True:
            while pila:
                llave = pila.pop()
                for valor in dictAux.get(llave):
                    if (valor[0].islower() | valor[0].isnumeric() | (valor[0] in string.punctuation)):
                        if llave not in self.first:
                            self.first[llave] = set()
                        self.first[llave].add(valor[0])
                    elif valor[0].isupper():
                        if(valor[0] in self.first):
                            if llave not in self.first:
                                self.first[llave] = set()
                            self.first[llave].update(self.first.get(valor[0]))
                        else:
                            dependiente.insert(0, llave)
                    if "ε" in valor:
                        faltantes.append(llave)

            while(dependiente):
                llave2 = dependiente.pop()
                for valor in dictAux.get(llave2):
                    if(valor[0] in self.first):
                        if llave not in self.first:
                            self.first[llave2] = set()
                        self.first[llave2].update(self.first.get(valor[0]))
            while(faltantes):
                llave = faltantes.pop()
                for key in dictAux.keys():
                    for cadena in dictAux.get(key):
                        if cadena[0] == llave:
                            posicion = dictAux.get(key).index(cadena)
                            dictAux[key][posicion] = dictAux.get(key)[
                                posicion][1:]
                            pila.append(key)
            if not pila:
                break
        return self.first

    def calculateFollow(self):
        cola = deque(self.gramatica.keys())
        indice = 0
        visitar = []
        while cola:
            llave = cola.popleft()
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
                        if llave == list(self.gramatica.keys())[0] and (siguiente.islower() | siguiente.isnumeric() | (siguiente in string.punctuation)):
                            if llave not in self.follow:
                                self.follow[llave] = set()
                            self.follow[llave].add("$")
                            continue
                        if siguiente != '' and 'ε' not in self.first[siguiente]:
                                if llave not in self.follow:
                                    self.follow[llave] = set()
                                self.follow[llave].update(
                                    self.first.get(siguiente))
                                continue
                        
                        if siguiente != '' and 'ε' in self.first[siguiente]:
                            if key not in self.follow.keys():
                                cola.append(key)
                                cola.append(llave)
                                print("aaaaa")
                            if llave not in self.follow:
                                self.follow[llave] = set()
                            self.follow[llave].update(self.first[siguiente] | self.follow[key])
                            continue
                    
                        
                        if siguiente == '':
                            if llave not in self.follow:
                                self.follow[llave] = set()
                            self.follow[llave].update(self.follow[key])
                            continue
                    except ValueError:
                        pass
        print(cola)
        # return indice

    def calculateTabla(self):
        pass

    def calculateCondiciones(self):
        pass


a = TopDownParsing({"E": ["TA"], "A": ["+TA", "ε"],"T": ["FB"], "B": ["*FB", "ε"], "F": ["(E)", "i"]})
#a = TopDownParsing({"A": ["BCD"], "B": ["b", "ε"],"C": ["c", "ε"], "D": ["d", "Ce"]})
#a = TopDownParsing({"S": ["ABC","i","ε"], "A": ["BC", "a"],"B": ["b", "ε"], "C": ["c"]})
a.calculateFirst()
# print(a.nT())
# print(a.first)
print(a.calculateFollow())
print(a.follow)
