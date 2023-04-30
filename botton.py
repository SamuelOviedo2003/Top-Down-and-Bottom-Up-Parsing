class BottonUpParsing:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.terminales = {}
        self.noterminales = {}
        self.first = {}
        self.follow = {}
        #self.tabla = pd.DataFrame()


Diccionario = {"S":["L=R","R"],"L":["*R","i"],"R":["L"]}

No_Terminales = list(Diccionario.keys())
Simbolo_incial = No_Terminales[0]+"'"

Diccionario[Simbolo_incial] = list(No_Terminales[0])

No_Terminales.insert(0, Simbolo_incial)

print(Diccionario)

#·
lista_estados = []

# def clousure():
#     estado  = []
    
#     Item = Diccionario[Simbolo_incial]
#     ItemInicial  = '·' + Item[0]
    
#     estado.insert(0, {Simbolo_incial : ItemInicial})
    
#     for diccionario in estado:
        
#         simbolo = diccionario[Simbolo_incial]
#         pos = simbolo.find('·')
#         simbolo = simbolo[pos+1]

def closure(noterminal):
    listaSimbolo  = Diccionario[noterminal]
    DicApoyo = { }
    lista = []
    
    for elemento in listaSimbolo:
        elemento2 = elemento
        elemento = '·' + elemento
        lista.append(elemento)
        DicApoyo[noterminal] = lista 
        
        if elemento2[0] in No_Terminales:
            DicApoyo.update(closure(elemento2[0]))
    return DicApoyo

print(closure('S'))