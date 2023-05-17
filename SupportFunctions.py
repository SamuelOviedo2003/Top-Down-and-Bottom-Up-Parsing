#gramatica  = {"S": ["aaSb", "cSb", "b"]}
#Diccionario = {"S":["L=R","R"],"L":["*R","i"],"R":["L"]}

def dot(cadena):
    pos = cadena.find('·')
    
    lista = list(cadena)
    char = lista[pos + 1] 
    lista[pos], lista[pos + 1] = lista[pos + 1], lista[pos] 
    cadena_nueva = "".join(lista) 
    
    lista = [cadena_nueva, char]
    return lista

def cadenaFinal(cadena):
    pos = cadena.find('·')
    if pos == len(cadena) - 1:
        return True
    else:
        return False

def reglasDeDerivacion(gramatica):
    reglas = []
    for key, value in gramatica.items():
        reglas = reglas + value
    return reglas


def terminales(cadena):
    terminales = []
    
    for c in cadena:
        if not c.isupper():
            terminales.append(c)
    
    return terminales


def casoEspecialKernel(lista):
    for i in range(0, len(lista)):
        cadena = lista[i]
        pos = cadena.find('·')
        if pos == len(cadena) - 1:
            del lista[i]
            lista.insert(0, cadena)
    return lista

def listaToString(lista):
    cadena = ''.join(str(elem) for elem in lista)
    return cadena

