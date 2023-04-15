from tdParsing import TopDownParsing

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
                "Ingresa las derivaciones , cuando termine con cada una digite '$' para seguir con la siguiente")
            derivacion = input("")
            while(derivacion != "$"):
                gramatica[noTerminal].append(derivacion)
                derivacion = input("")
        L = TopDownParsing(gramatica)
        print("First: ")
        L.NT()
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
        print("En proceso2")
    else:
        print("Seleccione una opcion valida")
