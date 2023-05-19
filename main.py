from tdParsing import TopDownParsing
from buParsing import BottonUpParsing

if __name__ == '__main__':
    print("| Desea analizar un:   |")
    print("| 1) Top-Down Parsing  |")
    print("| 2) Bottom-Up Parsing |")
    opcion = int(input(""))

    if opcion == 1:
        gramatica = {}
        numNoTerminales = int(input("Cuantos no-terminales hay? "))
        for i in range(numNoTerminales):
            noTerminal = input("no-terminal "+str(i+1)+": ")
            gramatica[noTerminal] = []
            print(
                "Ingresa las derivaciones empezando con el noTerminal inicial , cuando termine con cada una digite '$' para seguir con la siguiente")
            derivacion = input("")
            while(derivacion != "$"):
                gramatica[noTerminal].append(derivacion)
                derivacion = input("")
        L = TopDownParsing(gramatica)
        L.nT()
        L.calculateFirst()
        L.calculateFollow()
        print(L.calculateCondiciones())
        if L.calculateCondiciones()==True:
            print("First: ")
            for clave, valores in L.first.items():
                print(f"{clave} : {valores}")
            print("")
            print("Follow: ")
            for clave, valores in L.follow.items():
                print(f"{clave} : {valores}")
            print("")
            print("La tabla para analisis sintactico es: ")
            L.calculateTabla()
            print(L.tabla)
            print("")
            ################################
            listaCadenasComprobacion =["i+i","j","(i*i)"]
            listaCadenasFirst =["i+i","j","(i*i)"]
            ################################
            print("Validacion de cadenas por lista directa en el codigo: ")
            for cadena in listaCadenasComprobacion:
                respuesta = L.analizarCadena(cadena)
                print(f"{cadena} : {respuesta}")
                print("")
            print("")
            print("first de cadenas por lista directa en el codigo: ")
            for cadena in listaCadenasFirst:
                respuesta = L.firstCadena(cadena,False)
                print(f"{cadena} : {respuesta}")
                print("")
        else:
            print("la gramatica no es LL1")

    elif opcion == 2:
        gramatica = {}
        numNoTerminales = int(input("Cuantos no-terminales hay? "))
        for i in range(numNoTerminales):
            noTerminal = input("no-terminal "+str(i+1)+": ")
            gramatica[noTerminal] = []
            print(
                "Ingresa las derivaciones empezando con el noTerminal inicial , cuando termine con cada una digite '$' para seguir con la siguiente")
            derivacion = input("")
            while(derivacion != "$"):
                gramatica[noTerminal].append(derivacion)
                derivacion = input("")
        
        B = BottonUpParsing(gramatica)
        B.funcionTerminales()
        B.noterminalprima()
        print(B.SLR())
        
    else:
        print("Seleccione una opcion valida")
