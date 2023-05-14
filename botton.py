import SupportFunctions as sf

class BottonUpParsing:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.terminales = {}
        self.noterminales = {}
        self.first = {}
        self.follow = {}


Diccionario = {"S":["L=R","R"],"L":["*R","i"],"R":["L"]}

No_Terminales = list(Diccionario.keys())
Simbolo_incial = No_Terminales[0]+"'"

Diccionario[Simbolo_incial] = list(No_Terminales[0])

No_Terminales.insert(0, Simbolo_incial)


def closure(noterminal, gramatica):
    listaSimbolo  = gramatica[noterminal]
    DicApoyo = { }
    lista = []
    
    for elemento in listaSimbolo:
        elemento2 = elemento
        elemento = '·' + elemento
        lista.append(elemento)
        DicApoyo[noterminal] = lista 
        
        if elemento2[0] in No_Terminales:
            DicApoyo.update(closure(elemento2[0], gramatica))
    return DicApoyo





def GoTo(estado, simbolo, gramatica):
    lista = []
    noterminales = estado.keys()
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
            if cadena[pos+1] in noterminales:
                nuevoEstado.update(closure(cadena[pos+1], gramatica))
    
    
    noterminales = nuevoEstado.keys()

    for elemento in keyys:
        if elemento in noterminales:
            nuevoEstado[elemento].append(lista[i])
        else:
            nuevoEstado[elemento] = [lista[i]]
        i += 1
    
    return nuevoEstado, dicKernel
    


def LR0 (gramaticaIncial, simboloInicial):
    i = 0
    j = 0
    lista = []
    diccionarioEstados = {}
    diccionarioKernels = {}
    diccionarioTrans = {}
    
    diccionarioEstados[i] = closure(simboloInicial, gramaticaIncial)
    lista.append(closure(simboloInicial, gramaticaIncial))
    
    
    for diccionario in lista:
        diccionarioTrans[j] = []   
        for k, v in diccionario.items():
            
            for elemento in v:
                pos = elemento.find('·')
                if pos + 1 >= len(elemento):
                    break
                else:
                    simbolo = elemento[pos+1]
                
                posibleEstado, posibleKernel = GoTo(diccionario, simbolo, gramaticaIncial)
                
                if not posibleKernel in diccionarioKernels.values():
                    i += 1
                    diccionarioEstados[i] = posibleEstado
                    diccionarioKernels[i] = posibleKernel
                    diccionarioTrans[j].append([simbolo, i])
                    lista.append(posibleEstado)
                
                else:
                    for key, value in diccionarioTrans.items():
                        if value == posibleKernel:
                            diccionarioTrans[j].append([simbolo, key])
        j += 1
    
    return diccionarioEstados, diccionarioKernels, diccionarioTrans

d1, d2, d3 = LR0(Diccionario, "S'")

print(f'd1 : {d1}, d2 : {d2}, d3 : {d3}')