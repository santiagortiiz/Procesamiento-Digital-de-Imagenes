# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:51:28 2020

@author: SANTIAGO
"""
#%% Librerias para el diseño de la interfaz de Usuario

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene;                                    # Librerias necesarias para crear ventanas
from PyQt5.uic import loadUi                                                                # Libreria para cargar diseños en QtDesigner

from PyQt5 import QtCore
import pyqtgraph as pg
import numpy as np
       
#%% Objetos Ventanas presentes en la Interfaz de Usuario

class InterfazGrafica(QMainWindow):
    def __init__(self, ppal = None):
        super(InterfazGrafica,self).__init__()                                           
        loadUi('InterfazGrafica.ui',self)  
        self.estructura() 
        
        # Componentes
        self.cronometro = QtCore.QTimer(self);
        self.cronometro.timeout.connect(self.recuperar_frame)

        # Banderas
        self.camara_activada = False
        
    def asignarControlador(self, controlador):                                              # Se asigna el controlador a la ventana de inicio
        self.__controlador = controlador   
        
    def estructura(self): 
                                                                 
#%%     Espacio Grafico de la Camara
        # Opcion 1: QGraphicsView
        self.escena_1 = pg.ImageItem()                                                      # Se crea un objeto ImageItem como escena.
        escena_1 = QGraphicsScene()                                                         # Se crea un objeto QGraphicsScene y se 
        escena_1.addItem(self.escena_1)                                                     # le asigna el objeto ImageItem.
        self.espacio_grafico_1.setScene(escena_1)                                           # Se añade el objeto QGraphicsScene al
                                                                                            # objeto QGraphicsView de la interfaz.
        # Opcion 2: QPlotWidget
        #self.escena = pg.ImageItem()                                                       # Se crea un objeto ImageITem y se le asigna
        #self.espacio_grafico_1.addItem(self.escena)                                        # al objeto QPlotWidget de la interfaz.

#%%     Espacio grafico de la imagen Procesada 
        self.escena_2 = pg.ImageItem()                                                       
        escena_2 = QGraphicsScene()                                                            
        escena_2.addItem(self.escena_2)                                                        
        self.espacio_grafico_2.setScene(escena_2)

#%%     Espacio grafico del procesador de movimiento
        self.escena_3 = pg.ImageItem()                                                       
        escena_3 = QGraphicsScene()                                                            
        escena_3.addItem(self.escena_3)                                                        
        self.espacio_grafico_5.setScene(escena_3)      

        self.ocultar_componentes()                                     
       
#%%     Funciones de la Camara
        
    def activar_camara(self):
        self.camara_activada = self.__controlador.activar_camara()                          # Cuando la camara esta activa la bandera es verdadera
        if (self.cronometro.isActive() == False):                                           # y se activa el cronometro si aun no lo estaba
            self.mostrar_componentes()
            self.cronometro.start(20)
            
    def test(self):
        if (self.camara_activada == False):                                                 # Efecto One-Shot para testear
            self.mostrar_componentes()
            self.camara_activada = self.__controlador.activar_camara()
            self.recuperar_frame()
        else:
            self.recuperar_frame()
            
        if (self.cronometro.isActive()):
            self.cronometro.stop()
            
    def ajustar_parametros(self):                                                           # Configuraciones recomendadas segun el color
        configuracion = self.comboBox_ajustar_parametros.currentText()                      # del fondo y del marcador
        
        if (configuracion == "Marcador Blanco"):
            self.comboBox_color.setCurrentIndex(0)
            self.checkBox_extraer_color.setChecked(True)
            self.checkBox_ecualizar_color.setChecked(False)
            self.checkBox_gamma.setChecked(False)
            self.comboBox_binarizar.setCurrentIndex(1)
            self.doubleSpinBox_umbral.setValue(245)
            self.comboBox_transformacion_morfologica.setCurrentIndex(4)
            self.spinBox_iteraciones.setValue(3)
            self.checkBox_contornos.setChecked(True)

    def apagar_camara(self):                                                                # Se apaga la camara
        self.camara_activada = self.__controlador.apagar_camara()
        if (self.cronometro.isActive() == True):
            self.ocultar_componentes()
            self.cronometro.stop()

#%%  
    def recuperar_frame(self):
        if (self.camara_activada == True):
            
            frame_original = self.__controlador.recuperar_frame()                           # Recupera el Frame capturado por la camara
            proesamientos_aplicados = self.procesar_frame()                                 # aplica el flujo de procesamiento indicado
            self.determinar_ventana_actual(proesamientos_aplicados, frame_original)         # por el usuario y se determinan las  
                                                                                            # ventanas observadas actualmente
#%%     FLUJO DE PROCESAMIENTO

    def procesar_frame(self):
        frame_normalizado = False
        proesamientos_aplicados = 0
        
        # Extraccion de color
        if (self.checkBox_extraer_color.isChecked()):                                       
            proesamientos_aplicados += 1                                                   
            color = self.comboBox_color.currentText()
            self.__controlador.extraer_color(color)
        
            # Ecualizacion del color extraido
            if (self.checkBox_ecualizar_color.isChecked()):
                self.__controlador.ecualizar_color(color)
 
        # Correccion Gamma
        if (self.checkBox_gamma.isChecked()):
            proesamientos_aplicados += 1
            frame_normalizado = True
            factor_gamma = self.doubleSpinBox_gamma.value()
            self.__controlador.aplicar_correccion_gamma(factor_gamma)
            
        # Binarizacion
        if (self.comboBox_binarizar.currentText() != 'Binarizar'):
            proesamientos_aplicados += 1
            
            if (frame_normalizado == True):
                self.doubleSpinBox_umbral.setRange(0.00, 1.00)
                self.doubleSpinBox_umbral.setSingleStep(0.01)
            else:
                self.doubleSpinBox_umbral.setRange(0, 255)
                self.doubleSpinBox_umbral.setSingleStep(5)
                
            tipo_binarizacion = self.comboBox_binarizar.currentText()
            umbral = self.doubleSpinBox_umbral.value()
            self.__controlador.binarizar(tipo_binarizacion, umbral)
            
        # Transformacion Morfologica
        if (self.comboBox_transformacion_morfologica.currentText() != 'Transf. Morfologica'):
            transformacion = self.comboBox_transformacion_morfologica.currentText()
            iteraciones = self.spinBox_iteraciones.value()
            self.__controlador.aplicar_transformacion_morfologica(transformacion, iteraciones)
        
        # Identificacion de Contornos
        if (self.checkBox_contornos.isChecked()):
            color = self.comboBox_color.currentText()
            self.__controlador.identificar_contornos(color)
            
            # Caracterizacion de contornos
            contorno_de_interes = self.spinBox_contorno.value()
            movimiento_completado = self.__controlador.caracterizar_contornos(contorno_de_interes)
            
            if (movimiento_completado == True):
                self.__controlador.clasificar_movimiento()
            
        return proesamientos_aplicados # Indicador de la cantidad de procesamientos aplicados
  
#%%     INVOCA METODOS DE GRAFICACION   
     
    def determinar_ventana_actual(self, proesamientos_aplicados, frame_original):           # Se determina la ventana que esta observando
                                                                                            # el usuario, para realizar el procesamiento
        if (self.tabWidget_1.currentIndex() == 0):# Imagen original                         # unicamente de la informacion de interes
            self.graficar_frame_original(frame_original)
            
        elif (self.tabWidget_1.currentIndex() == 1): # Histograma original
            histograma_original = self.__controlador.calcular_histograma_original()
            self.graficar_histograma_original(histograma_original)
        
        if (proesamientos_aplicados > 0):
            if (self.tabWidget_2.currentIndex() == 0): # Imagen procesada
                frame_procesado = self.__controlador.recuperar_frame_procesado()
                self.graficar_frame_procesado(frame_procesado)
        
            elif (self.tabWidget_2.currentIndex() == 1): # Histograma procesado
                histograma_procesado = self.__controlador.calcular_histograma_procesado()
                self.graficar_histograma_procesado(histograma_procesado)
   
            elif (self.tabWidget_2.currentIndex() == 2): # Imagen de movimientos
                marcador = self.__controlador.recuperar_marcador()
                self.graficar_marcador(marcador)
                
#%%     GRAFICA DE FRAMES

    def graficar_frame_original(self, frame_original):
        if (type(frame_original) != bool):
            self.escena_1.setImage(frame_original)
        
    def graficar_frame_procesado(self, frame_procesado):
        self.escena_2.setImage(frame_procesado)
        
    def graficar_marcador(self, marcador):
        self.escena_3.setImage(marcador)
  
#%%     GRAFICA DE HISTOGRAMAS

    def graficar_histograma_original(self, histograma_original):
        rango_de_bits = np.arange(256)
        histograma_R = histograma_original[0]
        histograma_G = histograma_original[1]
        histograma_B = histograma_original[2]
        
        self.espacio_grafico_3.clear()
        
        if (self.comboBox_histograma.currentText() == 'Histograma RGB'):
            self.espacio_grafico_3.plot(rango_de_bits, histograma_R, pen = 'r')
            self.espacio_grafico_3.plot(rango_de_bits, histograma_G, pen = 'g')
            self.espacio_grafico_3.plot(rango_de_bits, histograma_B, pen = 'b')
            
        elif (self.comboBox_histograma.currentText() == 'Histograma Rojo'):
            self.espacio_grafico_3.plot(rango_de_bits, histograma_R, pen = 'r')
            
        elif (self.comboBox_histograma.currentText() == 'Histograma Verde'):
            self.espacio_grafico_3.plot(rango_de_bits, histograma_G, pen = 'g')
            
        elif (self.comboBox_histograma.currentText() == 'Histograma Azul'):
            self.espacio_grafico_3.plot(rango_de_bits, histograma_B, pen = 'b')
    
    def graficar_histograma_procesado(self, histograma_procesado):
        histograma_R = histograma_procesado[0]
        histograma_G = histograma_procesado[1]
        histograma_B = histograma_procesado[2]
        
        self.espacio_grafico_4.clear()
        
        if (self.checkBox_gamma.isChecked() == False):                                      # Se analiza si el rango de valores
            rango_de_bits = np.arange(256)                                                  # de la imagen es normal o se encuentra
                                                                                            # normalizado para  calcular el rango
        elif (self.checkBox_gamma.isChecked() == True):                                     # del eje X del histograma recibido
            rango_de_bits = np.arange(256)/255
            
        if (self.comboBox_histograma.currentText() == 'Histograma RGB'):
            self.espacio_grafico_4.plot(rango_de_bits, histograma_R, pen = 'r')
            self.espacio_grafico_4.plot(rango_de_bits, histograma_G, pen = 'g')
            self.espacio_grafico_4.plot(rango_de_bits, histograma_B, pen = 'b')
            
        elif (self.comboBox_histograma.currentText() == 'Histograma Rojo'):
            self.espacio_grafico_4.plot(rango_de_bits, histograma_R, pen = 'r')
            
        elif (self.comboBox_histograma.currentText() == 'Histograma Verde'):
            self.espacio_grafico_4.plot(rango_de_bits, histograma_G, pen = 'g')
            
        elif (self.comboBox_histograma.currentText() == 'Histograma Azul'):
            self.espacio_grafico_4.plot(rango_de_bits, histograma_B, pen = 'b')
        
#%%    Aspectos Esteticos de la interfaz 

    def mostrar_componentes(self):
        self.tabWidget_1.show()
        self.tabWidget_2.show()
        
        self.label.show()
        self.label_3.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.comboBox_ajustar_parametros.show()
        self.comboBox_histograma.show()
        self.comboBox_color.show()
        self.checkBox_extraer_color.show()
        self.checkBox_ecualizar_color.show()
        self.checkBox_gamma.show()
        self.comboBox_binarizar.show()
        self.comboBox_transformacion_morfologica.show()
        self.doubleSpinBox_gamma.show()
        self.doubleSpinBox_umbral.show()
        self.spinBox_iteraciones.show()
        self.checkBox_contornos.show()
        self.label.show()
        self.spinBox_contorno.show()
        
    def ocultar_componentes(self):
        self.tabWidget_1.hide()
        self.tabWidget_2.hide()
    
        self.label.hide()
        self.label_3.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.comboBox_ajustar_parametros.hide()
        self.comboBox_histograma.hide()
        self.comboBox_color.hide()
        self.checkBox_extraer_color.hide()
        self.checkBox_ecualizar_color.hide()
        self.checkBox_gamma.hide()
        self.comboBox_binarizar.hide()
        self.comboBox_transformacion_morfologica.hide()
        self.doubleSpinBox_gamma.hide()
        self.doubleSpinBox_umbral.hide()
        self.spinBox_iteraciones.hide()
        self.checkBox_contornos.hide()
        self.label.hide()
        self.spinBox_contorno.hide()
    
    
    
    