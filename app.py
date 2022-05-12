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
    ID_IMAGES=0
    MEJORES_GENERACION = []
    PEORES_GENERACION = []
    PROMEDIO_GENERACIONES = []
    ITERACION_GENERACION = 1
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.boton1.clicked.connect(self.setPlot)
        self.boton2.clicked.connect(self.setTexto)
        self.enviar.clicked.connect(self.getTexto)
        self.CalcularBoton.clicked.connect(self.generaciones)


    def setPlot(self):
        print("mat plot lib")
        x=[3.6  ,3.6  ,5      ,5.4   ,6,6.1  ,6.2  ,6.2 ]
        y=[-5.74,-5.74, -23.97,-22.53,-10.06,-6.78,-3.19,-3.19]

        plt.plot(x,y, label='linear')        
        plt.legend()
        plt.show()

    def setTexto(self):
        print("texto en caja")        
        self.poblacionInicialText.setText("6")
        self.precisionText.setText("0.001")
        self.rangoInicioText.setText("-4")
        self.rangoFinText.setText("4")
        self.poblacionMaximaText.setText("8")
        self.decendenciaText.setText("0.001")
        self.mutacionIndividuoText.setText("0.25")
        self.mutacionGenText.setText("0.40")
        #self.FuncionText.setText("x**2*sin(x)")
        self.FuncionText.setText("0.75*cos(1.50*x)*sin(1.50*x)-0.25*cos(0.25*x) ")
        

    def getTexto(self):
        print("enviar")        
        textoValor = self.texto.toPlainText()
        print(textoValor)

    def generaciones(self):
        print("Generaciones")
        generaciones = int(self.numGeneracionText.text())
        for num in range(generaciones):
            print("\nGeneracion: "+ str( num ))
            self.Calcular()

    def Calcular(self):
        print("Calculando")        
        
        funcion = self.FuncionText.text()

        poblacionInicial = self.poblacionInicialText.text()
        precision = self.precisionText.text()
        
        rangoInicio = self.rangoInicioText.text()
        rangoFin = self.rangoFinText.text()
        
        poblacionMaxima = self.poblacionMaximaText.text()

        """ decendencia = self.decendenciaText.text() """


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
            """ print(str(rangofin) +" 1> "+str(rangoinicio))
            print(str(rangofin - rangoinicio)) """
            rangoPrecision = (rangofin - rangoinicio) / precision
        else:
            """ print( str(rangoinicio) +" 2> "+str(rangofin) )            
            print(str(rangoinicio - rangofin)) """
            rangoPrecision = (rangoinicio - rangofin) / precision

        rangoPrecision = (rangofin - rangoinicio) / precision
        
        self.CantidadSolucionesLabel.setText(str(rangoPrecision+1))
        numDeBits = self.numBits(rangoPrecision)
        
        numeroBin=0
        arrayBits = []

        for x in range(int(poblacion)):
            numeroBin = random.randint(1, int(rangoPrecision))
            print("sujeto "+str(x)+"; valor: "+str(numeroBin))
            
            temp = format(numeroBin, "b")
            """ print(temp)
            print(len(temp))   """          
            
            binarioArrayTemp=[x, temp, numeroBin] #identificador A-B-C...w
            arrayBits.append(binarioArrayTemp)    #enviar "numeroBin" es el random para el binario

        self.completarNumBit(arrayBits, numDeBits)
    
    def numBits(self, rango):
        print("rango preci: "+str(rango))        
        
        bitsTemp = 0
        conta=0
        while (rango >= bitsTemp):
            conta+=1
            bitsTemp = 2**conta
            """ print(str(conta) +" - "+str(bitsTemp)) """

        self.numBitsLabel.setText(str(conta))

        return conta

    def completarNumBit(self, arrayBit, numDeBits):
        
        binariosGeneradosFinales = ""
        for dato in arrayBit:
            """ print("dato bi: "+dato[1]) """
            faltaanCeros = numDeBits - len(dato[1])            

            datoAux = dato[1]
            dato[1]=""

            for x in range(0,faltaanCeros):
                dato[1] += "0"
            
            dato[1] += datoAux
            print("final bits: "+dato[1])
            binariosGeneradosFinales += str(dato[0])+" : "+str(dato[1]) + " <-> " +str(dato[2])
            binariosGeneradosFinales += "\n"

        self.binariosGeneradosLabel.setText(binariosGeneradosFinales)
        self.seleccionTcT(arrayBit)

    # seleccion Todos con Todos
    def seleccionTcT(self, arrayBits):
        print("Todos con Todos")

        seleccion=[]        

        print(len(arrayBits))   

        auxDisminuir=1
        for x in range(0,len(arrayBits)):

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
                """ print("> "+str(x)) """
                seleccion.remove(x)
        
        self.cruza(seleccion, arrayBits)
    
    def cruza(self, seleccion, arrayBits):
        print(" \n inicia Cruza: "+ str(seleccion))
        print(" \n bits list: "+ str(arrayBits))

        hijosCruza = []

        for datoBin in seleccion:
            idA = str(arrayBits[datoBin[0]][0])
            idB = str(arrayBits[datoBin[1]][0])

            """ print("A "+ str(datoBin[0]) +" corte: "+str(datoBin[3])  +" id: "+ idA +" bit: "+ str(arrayBits[datoBin[0]][1]) +" valor: "+ str(arrayBits[datoBin[0]][2]))
            print("B "+ str(datoBin[1])+ " corte: "+str(datoBin[3])  +" id: "+ idB +" bit: "+ str(arrayBits[datoBin[1]][1]) +" valor: "+ str(arrayBits[datoBin[1]][2]))
            print("\n") """

            hijo1 = list(arrayBits[datoBin[0]][1])
            hijo2 = list(arrayBits[datoBin[1]][1])

            """ print("hijo 1: "+str(hijo1))
            print("hijo 2: "+str(hijo2)) """

            rang1 = int(datoBin[3])
            rang2 = len(str(arrayBits[datoBin[0]][1]))
            """ print(rang2) """

            corteA = ""
            corteA1 = ""
            for corte1 in range( 0, rang2):
                if corte1 >= rang1:
                    corteA+=hijo1[corte1]
                else:
                    corteA1+=hijo1[corte1]

            """ print("CA: "+corteA)
            print("CA1: "+corteA1) """

            corteB = ""
            corteB1 = ""
            for corte2 in range( 0, rang2):
                if corte2 >= rang1:
                    corteB+=hijo2[corte2]
                else:
                    corteB1+=hijo2[corte2]
                            
            """ print("CB: "+corteB)
            print("CB1: "+corteB1) """

            hijoA = corteA1 + corteB
            hijoB = corteB1 + corteA

            """ print("hijo A: "+ hijoA)
            print("hijo A: "+ hijoB) """
            
            hijosCruza.append([idA+idB+"-1" , hijoA])
            hijosCruza.append([idA+idB+"-2" , hijoB])

        self.mutacion(hijosCruza, arrayBits)
        

    def mutacion(self, listHijosCruza, arrayBits):
        mutacionIndividuo = self.mutacionIndividuoText.text()

        print("mutacion individuo: "+mutacionIndividuo)        

        for individuo in listHijosCruza:
            probabilidadMutacionIndividuo = (random.randint(1, 100)) / 100
            individuo.append(probabilidadMutacionIndividuo)

        hijosMutacion = []

        for indiv in listHijosCruza:
            """ print(str(indiv)) """
            if indiv[2] <= float(mutacionIndividuo):
                hijosMutacion.append(indiv)

        hijosMutados = self.mutarGen(hijosMutacion)

        print("regresar hijos mutados a lista principal de seleccion")
        for indice in range( len(listHijosCruza) ):
            for indiceMut in hijosMutados:                
                if listHijosCruza[indice][0] == indiceMut[0]:                    
                    listHijosCruza[indice][1] = indiceMut[1]
        
        """ muestra lista de cruza con los mutados """
        
        for indiv in range(0, len(listHijosCruza)):
            """ print(str(listHijosCruza[indiv])) """
            binario = listHijosCruza[indiv][1]
            valor = int(binario, 2)
            """ print(" - "+ str(valor)) """

            listHijosCruza[indiv].append(valor)
        
        """ for indiv in listHijosCruza:
            print(str(indiv)) """
        
        self.limpieza(listHijosCruza, arrayBits)
    
    def limpieza(self, listHijos, arrayBits):
        rango = float(self.CantidadSolucionesLabel.text()) - 1
        print("\nLimpieza rango: " + str(rango) )
        for hijo in listHijos:
            if hijo[3] <= rango:
                """ print(hijo) """
                arrayBits.append([ hijo[0] , hijo[1], hijo[3]])

        """ print("\n Paddres: ")
        for padresEhijos in arrayBits:
            print(str(padresEhijos)) """
        
        print("\nHijos y padres juentos:")
        poblacionMaxima = self.poblacionMaximaText.text()

        self.calcularCoordenadas(arrayBits)
        podaSelect = self.usarPodacheck.isChecked()
        
        print( "checked is: "+str(podaSelect) )
        if podaSelect:
            if len(arrayBits) > int(poblacionMaxima) :
                print("debe ver poda: padre> "+ str(len(arrayBits)))
                """ print("pob max: "+poblacionMaxima) """
                
                self.Poda(arrayBits)
            else:            
                print("No ocupa poda: padre>"+ str(len(arrayBits)))
                self.calcularCoordenadas(arrayBits)
            
    def Poda(self, arrayBits):
        print("\nInicia poda")
        
        for index in arrayBits:            
            print( str(index))

        """ agregando probabilidad de poda """
        for index in range( len(arrayBits) ):
            """ print( str(arrayBits[index]) ) """
            probabilidadPoda = (random.randint(1, 100)) / 100
            arrayBits[index].append(probabilidadPoda)    
        
        """ calculando PODA """
        poblacionMaxima = int(self.poblacionMaximaText.text())
        individuos = len(arrayBits)
        pp = poblacionMaxima / individuos
        self.infoPodaLabel.setText("poblacion maxima: "+str(poblacionMaxima)+"/ individuos: "+str(individuos))

        self.podaProbabilidad.setText(str(pp))

        #print("\n+ probabilidad:")        

        print("\nborrando mayores a poda:")

        listaPodado = []
        for index in arrayBits:
            if index[3] <= pp:
                """ print( str(index)) """
                listaPodado.append(index)


        if self.maximoRadio.isChecked():
            print("\n Mayor a menor:")
            listaPodado = sorted(listaPodado, key=lambda individuo: individuo[3], reverse=True)
            listaPodTempMax = []
            for index in range(len(listaPodado)):        
                
                if index < poblacionMaxima:
                    print( str(index) , str(listaPodado[index]))
                    listaPodTempMax.append(listaPodado[index])
                else:
                    print("fuera de limite de poblacion")
            
            self.calcularCoordenadas(listaPodTempMax)
        else:
            print("No ha seleccionado minimo")

        
        if self.minimoRadio.isChecked() :
            print("\n Menor a mayor:")
            listaPodado = sorted(listaPodado, key=lambda individuo: individuo[3], reverse=False)
            listaPodTempMin = []
            for index in range(len(listaPodado)):            
                if index < poblacionMaxima:
                    print( str(index) , str(listaPodado[index]))
                    listaPodTempMin.append(listaPodado[index])
                else:
                    print("fuera de limite de poblacion")
            
            self.calcularCoordenadas(listaPodTempMin)
        else:
            print("No ha seleccionado maximo")
                

    def calcularCoordenadas(self, listaIndividuos):
        print("Calculando")

        for i in range(len(listaIndividuos)):            
            listaIndividuos[i][2] = int( str(listaIndividuos[i][1]) , 2)
        
        """ print("\nCompuesto bit num") """
        xImax = []
        fXmax = []
        
        xImin = []
        fXmin = []

        fXprom = []
        xIprom = []
        coordenadasOrdenado = []

        rangoInicio = int(self.rangoInicioText.text())
        presicion = float(self.precisionText.text())
        funcion = self.FuncionText.text()
        
        #self.MEJORES_GENERACION.append([])

        for i in listaIndividuos:    
            print(str(i))        
            xiFun = float( rangoInicio + (float(i[2]) * presicion) )            

            x = xiFun #se usa dentro de eval como expresion regular
            fxFun = eval(funcion)
            
            coordenadasOrdenado.append( [xiFun, fxFun] )

        print("\nLIsta con coordenandas antes de max y min")
        for datoCor in coordenadasOrdenado:
            print( str(datoCor) )

        listaIndividuos = sorted(coordenadasOrdenado, key=lambda individuo: individuo[1], reverse=True)

        for datoCor in listaIndividuos:
            print( str(datoCor) )

        print("\nLlista generacion 1")
        print( "maximo"+ str(listaIndividuos[0]) )
        print( "minimo"+ str(listaIndividuos[ len(listaIndividuos)-1 ]) )
        
        maximoCoord = float(listaIndividuos[0][1])
        minimoCoord = float( listaIndividuos[ len(listaIndividuos)-1 ][1] )

        #xiFun = float( rangoInicio + (float( maximoCoord ) * presicion) )
        xiFun = maximoCoord
        x = xiFun #se usa dentro de eval como expresion regular
        fxFun = eval(funcion)
        
        #self.MEJORES_GENERACION.append([xiFun, fxFun])
        self.MEJORES_GENERACION.append([self.ITERACION_GENERACION, fxFun])        

        #xiFun = float( rangoInicio + (float( minimoCoord ) * presicion) )
        xiFun = minimoCoord
        x = xiFun #se usa dentro de eval como expresion regular
        fxFun = eval(funcion)
        #self.PEORES_GENERACION.append([xiFun, fxFun])
        self.PEORES_GENERACION.append([self.ITERACION_GENERACION, fxFun])
        
        #coordenadasOrdenado = sorted(coordenadasOrdenado, key=lambda xCoord: xCoord[0], reverse=False) # menor -mayor en x

        """ print("\nCoordenadas para graficar")
        for coor in coordenadasOrdenado:
            print(str(coor))
            xI.append(coor[0])
            fX.append(coor[1]) """
        
        if int(self.ITERACION_GENERACION) == int(self.numGeneracionText.text()) : #int( self.numGeneracionText()
            print("\nCoordenadas para graficar")
            for coor in self.MEJORES_GENERACION:
                print(str(coor))
                xImax.append(coor[0])
                fXmax.append(coor[1])            

            for coor in self.PEORES_GENERACION :
                print(str(coor))
                xImin.append(coor[0])
                fXmin.append(coor[1])

            for coor in range( len( self.MEJORES_GENERACION) ):
                promedio = (float(self.MEJORES_GENERACION[coor][1]) + float(self.PEORES_GENERACION[coor][1])) / 2
                xIprom.append( self.MEJORES_GENERACION[coor][0] )
                fXprom.append(promedio)
            
            print("\nAntes de graficar")
            for coor in self.MEJORES_GENERACION:
                print(str(coor))
            #self.ITERACION_GENERACION = 0    
            
            self.graficarDatos(xImax, fXmax, xImin, fXmin, xIprom, fXprom)
            #self.graficarDatos(xImin, fXmin)
            self.ITERACION_GENERACION = 1

        else:
            print("menor a iteracion")
            self.ITERACION_GENERACION +=1
    
    def graficarDatos(self, xMax, yMax, xMin, yMin, xProm, yProm):
        print("Graficando")            

        fig= plt.figure(figsize=(10,5))
        fig.tight_layout()
        plt.subplot(1, 1, 1)
        plt.plot(xMax,yMax, label='Maximos')
        plt.plot(xMin,yMin, label='Minimos')
        plt.plot(xProm,yProm, label='Promedio')

        self.MEJORES_GENERACION.clear()
        self.PEORES_GENERACION.clear()
        self.PROMEDIO_GENERACIONES.clear()
        
        # plt.plot(xMax,yMax, label='Maximos')
        # plt.plot(xMin,yMin, label='Minimos')
        # plt.plot(xProm,yProm, label='Promedio')
        
        #plt.scatter(x,y, label='Maximos')        
        plt.legend()

        plt.savefig("graficas/Grafica-"+ str( self.ID_IMAGES ) + ".png")
        self.ID_IMAGES+=1

        plt.show()
            
    
    def mutarGen(self, hijosMutar):
        print("Mutar Gen: ")
        for i in hijosMutar:
            bitsMutar = list(i[1])
            """ print("origin: "+str(bitsMutar)) """
            
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

            """ print("xor: "+str(bitsMutar)) """
            i[1] = mutarBitAux

        """ print("Mutados \n")
        for j in hijosMutar:
            print( "> "+str(j)) """
        
        return hijosMutar


if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_() #evita cerrar la ventana