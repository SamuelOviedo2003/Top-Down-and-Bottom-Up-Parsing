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

