from tdParsing import TopDownParsing
from buParsing import BottonUpParsing

if __name__ == '__main__':
    print("| Desea analizar un:   |")
    print("| 1) Top-Down Parsing  |")
    print("| 2) Bottom-Up Parsing |")
    opcion = int(input(""))
    GramaticaCodigo = {"E": ["TA"], "A": ["+TA", "ε"],"T": ["FB"], "B": ["*FB", "ε"], "F": ["(E)", "i"]}
    #GramaticaCodigo = {"S":["L=R","R"],"L":["*R","i"],"R":["L", "i"]}

    if opcion == 1:
        gramatica = GramaticaCodigo
        '''
        numNoTerminales = int(input("Cuantos no-terminales hay? "))
        for i in range(numNoTerminales):
            noTerminal = input("no-terminal "+str(i+1)+": ")
            gramatica[noTerminal] = []
            print(
                "Ingresa las derivaciones empezando con el noTerminal inicial , cuando termine con cada una digite '$' para seguir con la siguiente")
            derivacion = input("")
            while(derivacion != "$"):
                gramatica[noTerminal].append(derivacion)
                derivacion = input("")'''
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
            
            '''
            print("Ingresa las cadenas a analizar: ")
            print("")
            listaCadenasComprobacion = []
            cadena = " "
            while cadena != "":
                cadena = str(input())
                if cadena == "":
                    break
                listaCadenasComprobacion.append(cadena)
            '''
            
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
        gramatica = GramaticaCodigo
        '''
        numNoTerminales = int(input("Cuantos no-terminales hay? "))
        for i in range(numNoTerminales):
            noTerminal = input("no-terminal "+str(i+1)+": ")
            gramatica[noTerminal] = []
            print(
                "Ingresa las derivaciones empezando con el noTerminal inicial , cuando termine con cada una digite '$' para seguir con la siguiente")
            derivacion = input("")
            while(derivacion != "$"):
                gramatica[noTerminal].append(derivacion)
                derivacion = input("")'''
        
        
        B = BottonUpParsing(gramatica)
        B.funcionTerminales()
        B.noterminalprima()
        B.impresionLR0()
        print(" ")
        print(" --------- ")
        tablaSLR = B.SLR()
        print(tablaSLR)
        print(" ")
        print(" --------- ")
        
        if tablaSLR != 'Error, la tabla presenta conflictos' :
            
            print("Ingresa las cadenas a analizar: ")
            listaCadenasComprobacion = []
            cadena = " "
            while cadena != "":
                cadena = str(input())
                if cadena == "":
                    break
                listaCadenasComprobacion.append(cadena)
            
            ################################
            #listaCadenasComprobacion =["i+i","j","(i*i)"]
            ################################
            
            #print("Validacion de cadenas por lista directa en el codigo: ")
            
            for cadena in listaCadenasComprobacion:
                respuesta = B.parsing(cadena)
                print("")
                print(f"{cadena} : {respuesta}")
                print("")
            print("")
        
    else:
        print("Seleccione una opcion valida")
