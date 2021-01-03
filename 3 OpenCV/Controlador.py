# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:51:27 2020

@author: SANTIAGO
"""

#%% Librerias e Importación de Objetos de la Vista y el Modelo

import sys

from Vista import InterfazGrafica;
from Modelo import Procesador;
from PyQt5.QtWidgets import QApplication;

class Controlador(object):                                                                  # Se crea la clase contenedora de
    def __init__(self, vista, procesador):                                                  # la ventana que enlazara la
        self.__mi_vista = vista;                                                            # interfaz y el modelo del sistema
        self.__mi_modelo = procesador;

#%% Canal de comunicación/peticiones que realiza la vista al modelo
        
#%%    # Camara y Marcador
        
    def activar_camara(self):
        return self.__mi_modelo.activar_camara()
    
    def apagar_camara(self):
        return self.__mi_modelo.apagar_camara()
    
    def recuperar_frame(self):
        return self.__mi_modelo.recuperar_frame()

    def recuperar_frame_procesado(self):
        return self.__mi_modelo.recuperar_frame_procesado()
    
    def inicializar_marcador(self):
        self.__mi_modelo.inicializar_marcador()
        
    def recuperar_marcador(self):
        return self.__mi_modelo.recuperar_marcador()
        
 
#%%    # Procesamiento y Clasificacion
    
    def aplicar_correccion_gamma(self, factor_gamma):
        self.__mi_modelo.aplicar_correccion_gamma(factor_gamma)
    
    def extraer_color(self, color):
        self.__mi_modelo.extraer_color(color)
    
    def ecualizar_color(self, color):
        self.__mi_modelo.ecualizar_color(color)
        
    def binarizar(self, tipo_binarizacion, umbral):
        self.__mi_modelo.binarizar(tipo_binarizacion, umbral)
        
    def aplicar_transformacion_morfologica(self, transformacion, iteraciones):
        self.__mi_modelo.aplicar_transformacion_morfologica(transformacion, iteraciones)
    
    def identificar_contornos(self, color):
        self.__mi_modelo.identificar_contornos(color)
    
    def caracterizar_contornos(self, contorno_de_interes):
        return self.__mi_modelo.caracterizar_contornos(contorno_de_interes)
    
    def clasificar_movimiento(self):
        self.__mi_modelo.clasificar_movimiento()
        

#%%    # Histogramas
        
    def calcular_histograma_original(self):
        return self.__mi_modelo.calcular_histograma_original()
        
    def calcular_histograma_procesado(self):
        return self.__mi_modelo.calcular_histograma_procesado()
    
#%% Generador de la aplicación
        
class Aplicacion(object):                                                                   # Se crea la clase que pone en marcha
    def __init__(self):                                                                     # la aplicacion
        self.__app = QApplication(sys.argv)                                                
        
        self.__mi_vista = InterfazGrafica()                                                 # Se crean los objetos de la aplicacion  
        self.__mi_modelo = Procesador()
        
        self.__mi_controlador = Controlador(self.__mi_vista, self.__mi_modelo)              # Al controlador se le asignan los objetos 
                                                                                            # vista y modelo, y de forma análoga, a los 
        self.__mi_vista.asignarControlador(self.__mi_controlador)                           # objetos se les asigna el controlador  
        self.__mi_modelo.asignarControlador(self.__mi_controlador)                          # para que esten entrelazados
        
    def main(self):
        self.__mi_vista.show()
        sys.exit(self.__app.exec_())
   
     
#%%
aplicacion = Aplicacion()
aplicacion.main()






