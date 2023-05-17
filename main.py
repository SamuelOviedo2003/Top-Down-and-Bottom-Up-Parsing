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
        print("First: ")
        L.nT()
        L.calculateFirst()
        for clave, valores in L.first.items():
            print(f"{clave} : {valores}")
        print("")
        print("Follow: ")
        L.calculateFollow()
        for clave, valores in L.follow.items():
            print(f"{clave} : {valores}")
        print("")

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
        
        
        
    else:
        print("Seleccione una opcion valida")
