import SupportFunctions as sf
import tdParsing as td
from tabulate import tabulate

class BottonUpParsing:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.terminales = []
        self.noterminales = []
        self.prima = ""
        self.first = {}
        self.follow = {}


    def noterminalprima(self):
        noterminales = list(self.gramatica.keys())
        Simbolo_incial = noterminales[0]+"'"
        self.prima = Simbolo_incial
        self.gramatica[Simbolo_incial] = list(noterminales[0])
        noterminales.insert(0, Simbolo_incial)
        return self.gramatica


    def funcionTerminales (self):
        self.terminales = list(self.gramatica.values())
        cojunto = []
        
        for lista in self.terminales:
            for objeto in lista:
                cojunto = cojunto + sf.terminales(objeto)
        
        cojunto = list(dict.fromkeys(cojunto))
        
        self.terminales = cojunto
        
        return self.terminales




    def closure(self,noterminal):
        self.noterminales = list(self.gramatica.keys())
        listaSimbolo  = self.gramatica[noterminal]
        diccionario = { }
        lista = []
        
        for elemento in listaSimbolo:
            elemento2 = elemento
            elemento = '·' + elemento
            lista.append(elemento)
            diccionario[noterminal] = lista 
            
            if elemento2[0] != noterminal:
                if elemento2[0] in self.noterminales :
                    diccionario.update(self.closure(elemento2[0]))
        return diccionario



    def GoTo(self, estado, simbolo):
        lista = []
        #noterminales = estado.keys()
        nuevoEstado = {}
        dicKernel = {}
        keyys = []
        i = 0
        
        for x, y in estado.items():
            for elemento in y:
                pos = elemento.find('·')
                if pos + 1 >= len(elemento):
                    break
                else: 
                    if elemento[pos+1] == simbolo:
                        sl = sf.dot(elemento)
                        lista.append(sl[0])
                        keyys.append(x)
        
        dicKernel['Kernel']  = lista
        
        for cadena in lista:
            pos = cadena.find('·')
            if pos + 1 >= len(cadena):
                break
            else:
                if cadena[pos+1] in self.noterminales:
                    nuevoEstado.update(self.closure(cadena[pos+1]))
        

        noterminales = nuevoEstado.keys()
        
        for elemento in keyys:
            if elemento in noterminales:
                nuevoEstado[elemento].append(lista[i])
            else:
                nuevoEstado[elemento] = [lista[i]]
            i += 1
        
        return nuevoEstado, dicKernel


    def LR0 (self):
        i = 0
        j = 0
        lista = []
        diccionarioEstados = {}
        diccionarioKernels = {}
        diccionarioTrans = {}
        
        bu.noterminalprima()
        
        diccionarioEstados[i] = self.closure(self.prima)
        lista.append(self.closure(self.prima))
        
        diccionarioKernels[0] = {'Kernel' : diccionarioEstados[0][self.prima]}
        
        for diccionario in lista:
            diccionarioTrans[j] = []
            for k, v in diccionario.items():
                
                for elemento in v:
                    pos = elemento.find('·')
                    if pos + 1 >= len(elemento):
                        break
                    else:
                        simbolo = elemento[pos+1]
                    
                    posibleEstado, posibleKernel = self.GoTo(diccionario, simbolo)
                    
                    if not posibleKernel in diccionarioKernels.values():
                        i += 1
                        diccionarioEstados[i] = posibleEstado
                        diccionarioKernels[i] = posibleKernel
                        diccionarioTrans[j].append([simbolo, i])
                        lista.append(posibleEstado)
                    
                    else:
                        
                        for key, value in diccionarioKernels.items():
                            if (value['Kernel'] == posibleKernel['Kernel']) and not([simbolo, key] in diccionarioTrans[j]):
                                diccionarioTrans[j].append([simbolo, key])
            j += 1
        
        diccionarioTrans[1].append(['$', 'acc'])
        
        return diccionarioEstados, diccionarioKernels, diccionarioTrans


    def action(self, estado, caracter):
        acc = None
        reduce = None
        shift = None
        error = False
        accion = ''
        
        
        d1, d2, d3 = bu.LR0()
        
        
        self.noterminales = self.gramatica.keys()
        
        
        matriz  = d3[estado]
        
        #Reduce
        if caracter in self.terminales or caracter == '$':
            
            
            lista = d2[estado]['Kernel']
            
            if len(lista) >= 2:
                lista = sf.casoEspecialKernel(lista)
            
            cadena = lista[0]
            
            pos  = cadena.find('·')
            
            if pos == len(cadena) - 1:
                
                
                key = [llave for llave, valor in d1[estado].items() if valor == [cadena]]
                key = str(key[0])
                
                cadena = cadena[:len(cadena) - 1]
                gramaticaSinPrima = self.gramatica
                del gramaticaSinPrima[self.prima]
                reglas  = sf.reglasDeDerivacion(gramaticaSinPrima)
                
                for i in range(0, len(reglas)):
                    if reglas[i] == cadena:
                        posRegla = i + 1
                
                
                
                #Accept
                if ("'" in key):
                    if (caracter == "$"):
                        acc = 'acc'
                    else:
                        acc = None
                
                else:
                    
                    tdp = td.TopDownParsing(gramaticaSinPrima)
                    tdp.nT()
                    tdp.calculateFirst()
                    tdp.calculateFollow()
                    
                    follow = list(tdp.follow[key])
                    
                    if caracter in follow:
                        reduce  = 'r' + str(posRegla)
        
        
        
        #Shift
        if caracter in self.terminales:
            for lista in matriz:
                if lista[0] == caracter:
                    shift = 's' + str(lista[1])
        
        elif caracter in self.noterminales:
            for lista in matriz:
                if lista[0] == caracter:
                    shift = str(lista[1])
        
        
        if (shift != None) and (reduce != None):
            error = True
            accion = error
        
        elif acc!= None:
            accion  = acc
        
        elif reduce != None:
            accion  = reduce
        
        elif shift != None:
            accion  = shift
        
        
        return accion


    def SLR (self):
        data = []
        lista = []
        mensaje  = ''
        
        
        d1, d2, d3 = bu.LR0()
        
        estados  = list(d1.keys())
        
        self.terminales.append("$")
        
        
        self.noterminales = list(self.noterminales)
        self.noterminales.remove(self.prima)
        
        head = self.terminales + self.noterminales
        
        for i in range(len(head)):
            lista.append('')
        
        
        for estado in estados:
            lista_copia = list(lista)            
            for elemento in head:
                indice  = head.index(elemento)
                
                accion = self.action(estado, elemento)
                if accion == True:
                    lista_copia[indice] = 'Error'
                    mensaje  = 'Esta gramatica no es LR1, la tabla presenta conflictos'
                else:
                    lista_copia[indice] = accion
                
            lista_copia.insert(0, estado)
            
            data.append(lista_copia)
        
        head.insert(0, '#')
        print(tabulate(data, headers= head, tablefmt="psql"))
        
        return mensaje


    def parsing(self, cadena):
        data = []
        head = ['Line', 'Stack', 'Symbols', 'Input', 'Action']
        line = 2 
        
        gramaticaSinPrima = self.gramatica
        del gramaticaSinPrima[self.prima]
        reglas  = sf.reglasDeDerivacion(gramaticaSinPrima)
        
        
        
        action  = ''
        stack  = [0]
        symbols  = ['$']
        input  = list(cadena)
        input.append('$')
        
        st = stack.copy()
        sy = symbols.copy()
        inp = input.copy()
        
        
        
        lista = [1, sf.listaToString(st), sf.listaToString(sy), sf.listaToString(inp), '']
        
        data.append(lista)
        
        while action != 'acc':
            lista_copia = list()
            action = ''
            
            
            estado  = stack[-1]
            caracter = input[0]
            
            
            accion = self.action(estado, caracter)
            
            
            if accion == True or accion == '':
                return 'Esta no es una cadena valida'
            
            elif accion[0] == 's':
                
                estadoShift  = int(accion[1])
                action = 'Shift to ' + str(estadoShift)
                stack.append(estadoShift)
                symbols.append(input[0])
                del input[0]
                
                
                st = stack.copy()
                sy = symbols.copy()
                inp = input.copy()
                
                lista_copia.append(line)
                
                lista_copia.append(sf.listaToString(st))
                lista_copia.append(sf.listaToString(sy))
                lista_copia.append(sf.listaToString(inp))
                lista_copia.append('')
                
                
                data.append(lista_copia)
                
            elif accion[0] == 'r':
                numeroregla = int(accion[1:])
                derivacion  = reglas[numeroregla-1]
                
                for llave, valor in self.gramatica.items():
                    for element in valor:
                        if derivacion == element:
                            key = llave
                
                
                symbols = symbols[:-len(derivacion)]
                
                symbols.append(key)
                
                action = 'Reduce by ' + key + ' --> ' + derivacion
                
                simbolosEliminar = len(derivacion)
                
                stack  = stack[:-simbolosEliminar]
                
                
                accionreduce = self.action(stack[-1], symbols[-1])
                            
                if accionreduce.find('r') == -1:
                    stack.append(int(accionreduce))
                else:
                    stack.append(int(accionreduce[1:]))
                
                
                st = stack.copy()
                sy = symbols.copy()
                inp = input.copy()
                
                lista_copia.append(line)
                
                lista_copia.append(sf.listaToString(st))
                lista_copia.append(sf.listaToString(sy))
                lista_copia.append(sf.listaToString(inp))
                lista_copia.append('')
                
                #data[-1].append(action)
                
                data.append(lista_copia)
            
            elif accion == 'acc':
                action = 'acc'
                
                st = stack.copy()
                sy = symbols.copy()
                inp = input.copy()
                
                lista_copia.append(line)
                
                lista_copia.append(sf.listaToString(st))
                lista_copia.append(sf.listaToString(sy))
                lista_copia.append(sf.listaToString(inp))
                lista_copia.append('')
                
                
                data.append(lista_copia)
                
            
            
            data[-2][-1] = action
            
            line += 1
        
        del data[-1]
        
        #print(f'data: {data}')
        print(tabulate(data, headers= head, tablefmt="github"))
        
        
        
        
        return None



'''
print(SLRPT(d1,d3, No_Terminales, Terminales, follow, gramatica))


Diccionario = {"S":["L=R","R"],"L":["*R","i"],"R":["L"]}
gramatica  = {"S": ["aaSb", "cSb", "b"]}



d1, d2, d3 = LR0(gramatica, "S'")
#print(f'd1: {d1}, d2: {d2}, d3: {d3}')

follow = {'a' : ['NA'], 'b' : ['NA'], 'c' : ['NA'], 'S': ['$', 'b']}

'''



gramatica  = {"S": ["aaSb", "cSb", "b"]}
#gramatica = {"S":["L=R","R"],"L":["*R","i"],"R":["L", "i"]}

#gramatica = {"A": ["BCD","Aa"], "B": ["b", "ε"],"C": ["c", "ε"], "D": ["d", "Ce"]}

#gramatica = {"E" : ["E+T", "T"], "T" : ["T*F", "F"], "F" : ["(E)", "i"]}

#a= td.TopDownParsing({"S":["L=R","R"],"R":["L"],"L":["*R","i"]})



bu  = BottonUpParsing(gramatica)
bu.funcionTerminales()
bu.noterminalprima()

#print(bu.gramatica)

#estado0 = bu.closure("E'")
#print(estado0)

#print(bu.GoTo(estado0, 'T'))

d1, d2, d3 = bu.LR0()
#print(f'd1: {d1}, d2: {d2}, d3: {d3}')

#accion =  bu.action(0, "F")

#print (f'accion: {accion}')


#print(bu.SLR())

print(bu.parsing('aacbbb'))
