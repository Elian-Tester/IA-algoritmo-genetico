#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ast import arg
import sys

#Importar aquí las librerías a utilizar
import matplotlib.pyplot as plt
import random
from math import sin, cos, tan

from PyQt5 import uic, QtWidgets

qtCreatorFile = "vista.ui" #Aquí va el nombre de tu archivo

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.boton1.clicked.connect(self.setPlot)
        self.boton2.clicked.connect(self.setTexto)
        self.enviar.clicked.connect(self.getTexto)
        self.CalcularBoton.clicked.connect(self.Calcular)


    def setPlot(self):
        print("mat plot lib")
        x=[3.6  ,3.6  ,5      ,5.4   ,6,6.1  ,6.2  ,6.2 ]

        y=[-5.74,-5.74, -23.97,-22.53,-10.06,-6.78,-3.19,-3.19]
        
        y2=[1,3,4,1,15,4,7,2,6,6,1,7,11,10,14]
        plt.plot(x,y, label='linear')
        #plt.plot(x,y2, label='quadratic')
        #plt.show()      
        plt.legend()
        plt.show()

    def setTexto(self):
        print("texto en caja")        
        self.poblacionInicialText.setText("6")
        self.precisionText.setText("0.1")
        self.rangoInicioText.setText("3")
        self.rangoFinText.setText("8")
        self.poblacionMaximaText.setText("8")
        self.decendenciaText.setText("0.001")
        self.mutacionIndividuoText.setText("0.25")
        self.mutacionGenText.setText("0.40")

    def getTexto(self):
        print("enviar")        
        textoValor = self.texto.toPlainText()
        print(textoValor)

    def Calcular(self):
        print("Calculando")        
        
        funcion = self.FuncionText.text()

        poblacionInicial = self.poblacionInicialText.text()
        precision = self.precisionText.text()
        
        rangoInicio = self.rangoInicioText.text()
        rangoFin = self.rangoFinText.text()
        
        poblacionMaxima = self.poblacionMaximaText.text()

        decendencia = self.decendenciaText.text()


        print("Funcion: "+funcion)
        print("poblacion Inicial: "+poblacionInicial)
        print("precision: "+precision)
        print("rango Inicio: "+rangoInicio)
        print("rango Fin: "+rangoFin)
        print("poblacion Maxima: "+poblacionMaxima)        
        
        self.generarBinario(poblacionInicial, float(precision), int(rangoInicio),int(rangoFin))

    
    def generarBinario(self, poblacion, precision, rangoinicio, rangofin):
        print("geneando "+poblacion+ " sujetos / rango fin " + str(rangofin) )

        if rangofin > rangoinicio:
            print(str(rangofin) +" 1> "+str(rangoinicio))
            print(str(rangofin - rangoinicio))
            rangoPrecision = (rangofin - rangoinicio) / precision
        else:
            print( str(rangoinicio) +" 2> "+str(rangofin) )            
            print(str(rangoinicio - rangofin))
            rangoPrecision = (rangoinicio - rangofin) / precision

        rangoPrecision = (rangofin - rangoinicio) / precision
        #print("Rango precision: "+str(rangoPrecision))
        self.CantidadSolucionesLabel.setText(str(rangoPrecision+1))
        numDeBits = self.numBits(rangoPrecision)
        
        numeroBin=0
        arrayBits = []

        for x in range(int(poblacion)):
            numeroBin = random.randint(1, int(rangoPrecision))
            print("sujeto "+str(x)+"; valor: "+str(numeroBin))
            
            temp = format(numeroBin, "b")
            print(temp)
            print(len(temp))            
            
            binarioArrayTemp=[x, temp, numeroBin] #identificador A-B-C...w
            arrayBits.append(binarioArrayTemp)    #enviar "numeroBin" es el random para el binario

        #print("array bitss "+str(arrayBits))

        self.completarNumBit(arrayBits, numDeBits)
    
    def numBits(self, rango):
        print("rango preci: "+str(rango))        
        
        bitsTemp = 0
        conta=0

        while (rango >= bitsTemp):
            conta+=1
            bitsTemp = 2**conta
            print(str(conta) +" - "+str(bitsTemp))

        self.numBitsLabel.setText(str(conta))

        return conta

    def completarNumBit(self, arrayBit, numDeBits):
        
        binariosGeneradosFinales = ""
        for dato in arrayBit:
            print("dato bi: "+dato[1])
            faltaanCeros = numDeBits - len(dato[1])
            print(str(len(dato[1])) + " faltan: "+str( faltaanCeros ))

            datoAux = dato[1]
            dato[1]=""

            for x in range(0,faltaanCeros):
                dato[1] += "0"
            
            dato[1] += datoAux
            print("final bits: "+dato[1])
            binariosGeneradosFinales += str(dato[0])+" : "+str(dato[1]) + " <-> " +str(dato[2])
            binariosGeneradosFinales += "\n"

        #print("num bits completar: " + str(arrayBit))
        self.binariosGeneradosLabel.setText(binariosGeneradosFinales)
        self.seleccionTcT(arrayBit)

    # seleccion Todos con Todos
    def seleccionTcT(self, arrayBits):
        print("Todos con Todos")

        seleccion=[]        

        print(len(arrayBits))   
#        for x in arrayBits:
#            print(str(x[0]) +" : " + str(x[1]) + " - "+str(x[2]))

        print("for controlado")

        auxDisminuir=1
        for x in range(0,len(arrayBits)):
            #print(str(arrayBits[x][0]) +" : "+ str(arrayBits[x][1]) +" - "+ str(arrayBits[x][2]))

            for j in range(auxDisminuir, len(arrayBits)):
                print("x: "+str(x)+" J: "+str(j))
                
                probabilidadDesendencia = (random.randint(1, 100)) / 100
                corteCruza = random.randint(1, len(arrayBits[x][1]) - 1 )

                combinacion=[x, j, probabilidadDesendencia, corteCruza]
                
                seleccion.append(combinacion)
            
            auxDisminuir+=1

        print("seleccion: "+str(seleccion))

        probabDecendencia = self.decendenciaText.text()
        print("Decendencia: "+ probabDecendencia)

        for x in seleccion:
            if x[2] >= float(probabDecendencia):
                print("> "+str(x))
                seleccion.remove(x)

        
        print("actual: "+str(seleccion))
        
        self.cruza(seleccion, arrayBits)

        #abecedario = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
    
    def cruza(self, seleccion, arrayBits):
        print(" \n inicia Cruza: "+ str(seleccion))
        print(" \n bits list: "+ str(arrayBits))

        hijosCruza = []
        

        for datoBin in seleccion:
            idA = str(arrayBits[datoBin[0]][0])
            idB = str(arrayBits[datoBin[1]][0])

            print("A "+ str(datoBin[0]) +" corte: "+str(datoBin[3])  +" id: "+ idA +" bit: "+ str(arrayBits[datoBin[0]][1]) +" valor: "+ str(arrayBits[datoBin[0]][2]))
            print("B "+ str(datoBin[1])+ " corte: "+str(datoBin[3])  +" id: "+ idB +" bit: "+ str(arrayBits[datoBin[1]][1]) +" valor: "+ str(arrayBits[datoBin[1]][2]))
            print("\n")

            hijo1 = list(arrayBits[datoBin[0]][1])
            hijo2 = list(arrayBits[datoBin[1]][1])

            print("hijo 1: "+str(hijo1))
            print("hijo 2: "+str(hijo2))

            rang1 = int(datoBin[3])
            rang2 = len(str(arrayBits[datoBin[0]][1]))
            print(rang2)

            corteA = ""
            corteA1 = ""
            for corte1 in range( 0, rang2):
                if corte1 >= rang1:
                    corteA+=hijo1[corte1]
                else:
                    corteA1+=hijo1[corte1]

            print("CA: "+corteA)
            print("CA1: "+corteA1)

            corteB = ""
            corteB1 = ""
            for corte2 in range( 0, rang2):
                if corte2 >= rang1:
                    corteB+=hijo2[corte2]
                else:
                    corteB1+=hijo2[corte2]
                            
            print("CB: "+corteB)
            print("CB1: "+corteB1)

            hijoA = corteA1 + corteB
            hijoB = corteB1 + corteA

            print("hijo A: "+ hijoA)
            print("hijo A: "+ hijoB)
            
            hijosCruza.append([idA+idB+"-1" , hijoA])
            hijosCruza.append([idA+idB+"-2" , hijoB])

        self.mutacion(hijosCruza, arrayBits)
        

    def mutacion(self, listHijosCruza, arrayBits):
        mutacionIndividuo = self.mutacionIndividuoText.text()

        print("mutacion individuo: "+mutacionIndividuo)

        #print("list hijos: "+str(listHijosCruza))        

        for individuo in listHijosCruza:
            probabilidadMutacionIndividuo = (random.randint(1, 100)) / 100
            individuo.append(probabilidadMutacionIndividuo)

        #itera comentarios // puede borrar

        hijosMutacion = []

        for indiv in listHijosCruza:
            print(str(indiv))
            if indiv[2] <= float(mutacionIndividuo):
                hijosMutacion.append(indiv)

        hijosMutados = self.mutarGen(hijosMutacion)

        for indice in range( len(listHijosCruza) ):
            for indiceMut in hijosMutados:                
                if listHijosCruza[indice][0] == indiceMut[0]:
                    print("encontrado")
                    listHijosCruza[indice][1] = indiceMut[1]
        
        """ muestra lista de cruza con los mutados """
        
        for indiv in range(0, len(listHijosCruza)):
            print(str(listHijosCruza[indiv]))
            binario = listHijosCruza[indiv][1]
            valor = int(binario, 2)
            print(" - "+ str(valor))

            listHijosCruza[indiv].append(valor)
        
        for indiv in listHijosCruza:
            print(str(indiv))
        
        self.limpieza(listHijosCruza, arrayBits)
    
    def limpieza(self, listHijos, arrayBits):
        rango = float(self.CantidadSolucionesLabel.text()) - 1
        print("\nLimpieza rango: " + str(rango) )
        for hijo in listHijos:
            if hijo[3] <= rango:
                print(hijo)
                arrayBits.append([ hijo[0] , hijo[1], hijo[3]])

        print("\n Paddres: ")
        for padresEhijos in arrayBits:
            print(str(padresEhijos))

        poblacionMaxima = self.poblacionMaximaText.text()
        if len(arrayBits) > int(poblacionMaxima) :
            print("debe ver poda: padre> "+ str(len(arrayBits)))
            print("pob max: "+poblacionMaxima)
            
            self.Poda(arrayBits)
        else:            
            print("No ocupa poda: padre>"+ str(len(arrayBits)))
            print("pob max: "+poblacionMaxima)
            
    def Poda(self, arrayBits):
        print("\nInicia poda")        

        """ agregando probabilidad de poda """
        for index in range( len(arrayBits) ):
            print( str(arrayBits[index]) )
            probabilidadPoda = (random.randint(1, 100)) / 100
            arrayBits[index].append(probabilidadPoda)    
        
        """ calculando PODA """
        poblacionMaxima = int(self.poblacionMaximaText.text())
        individuos = len(arrayBits)
        pp = poblacionMaxima / individuos
        self.infoPodaLabel.setText("poblacion maxima: "+str(poblacionMaxima)+"/ individuos: "+str(individuos))

        self.podaProbabilidad.setText(str(pp))

        print("\n+ probabilidad:")
        
        for index in arrayBits:            
            print( str(index)) 

        print("\nborrando mayores a poda:")

        listaPodado = []
        for index in arrayBits:
            if index[3] <= pp:
                print( str(index))
                listaPodado.append(index)
        
        print("\npodado:")
        for index in listaPodado:            
            print( str(index)) 

        #print("\n Mayor a menor:")
        #for index in listaPodado:            
        #    print( str(index)) 

        print("\n Mayor a menor:")
        listaPodado = sorted(listaPodado, key=lambda individuo: individuo[3], reverse=True)
        # poblacionMaxima
        for index in range(len(listaPodado)):        
            
            if index < poblacionMaxima:
                print( str(index) , str(listaPodado[index]))
            else:
                print("fuera de limite")
        
        self.calcularCoordenadas(listaPodado)

        """ print("\n Menor a mayor:")
        listaPodado = sorted(listaPodado, key=lambda individuo: individuo[3], reverse=False)
        for index in listaPodado:            
            print( str(index)) """
                

    def calcularCoordenadas(self, listaPodado):
        print("Calculando")

        for i in range(len(listaPodado)):            
            listaPodado[i][2] = int( str(listaPodado[i][1]) , 2)
        
        print("\nCompuesto bit num")
        xI = []
        fX = []
        coordenadasOrdenado = []

        rangoInicio = int(self.rangoInicioText.text())
        presicion = float(self.precisionText.text())
        funcion = self.FuncionText.text()

        #sin ='math.sin'
        for i in listaPodado:
            print(str(i)) #pos [2]

            xiFun = float( rangoInicio + (float(i[2]) * presicion) )            
            print( str(rangoInicio) +" - "+ str( i[2] ) + " - " + str(presicion))
            print("res: "+ str(xiFun) )
            #xI.append( xiFun )

            x = xiFun #se usa dentro de eval como expresion regular
            fxFun = eval(funcion)
            print( str(xiFun) +" -> "+ str(fxFun) )
            #fX.append(fxFun)
            
            coordenadasOrdenado.append( [xiFun, fxFun] )
        
        coordenadasOrdenado = sorted(coordenadasOrdenado, key=lambda xCoord: xCoord[0], reverse=False) # menor -mayor en x

        print("\nCoordenadas para graficar")
        for coor in coordenadasOrdenado:
            print(str(coor))
            xI.append(coor[0])
            fX.append(coor[1])
            
        self.graficarDatos(xI, fX)
    
    def graficarDatos(self, x, y):
        print("Graficando")        
        
        plt.plot(x,y, label='linear')
        #plt.plot(x,y2, label='quadratic')
        
        plt.legend()
        plt.show()
            
    
    def mutarGen(self, hijosMutar):
        print("Mutar Gen: ")
        for i in hijosMutar:
            #print("< "+str(i))
            bitsMutar = list(i[1])
            print("origin: "+str(bitsMutar))
            
            mutarBitAux = ""
            for index in range(len(bitsMutar)):
                probabilidadMutacionGen = (random.randint(1, 100)) / 100

                if probabilidadMutacionGen <= float(self.mutacionGenText.text()):
                    if bitsMutar[index] == "0":
                        bitsMutar[index] = "1"
                        mutarBitAux+=bitsMutar[index]
                    else:
                        bitsMutar[index] = "0"
                        mutarBitAux+=bitsMutar[index]
                else:
                    mutarBitAux+=bitsMutar[index]

            print("xor: "+str(bitsMutar))
            i[1] = mutarBitAux

        print("Mutados \n")
        for j in hijosMutar:
            print( "> "+str(j))
        
        return hijosMutar


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_() #evita cerrar la ventana