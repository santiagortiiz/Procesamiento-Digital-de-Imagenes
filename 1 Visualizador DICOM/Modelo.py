# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:51:26 2020

@author: SANTIAGO
"""
 
#%% Librerias de procesamiento de información: "Back-end"

import os
import string
import numpy as np
import pydicom
from scipy import ndimage
from PIL import Image
                                                                                                
#%% Clase que procesa la información, aqui se definen los atributos y se asigna el controlador

class Procesador(object):
    def __init__(self):  
        self.imagen_referencia = None
        self.volumen = None                                                                 # Se inicializan los atributos que tendra el modelo 
        self.filas = 0                                                                      # para realizar el procesamiento necesario para
        self.columnas = 0                                                                   # la VISUALIZACION de la señal cargada.
        self.cortes = 0
        
        self.corte_axial = 0                                                                # Los cortes corresponden a la sección
        self.corte_coronal = 0                                                              # visualizada
        self.corte_sagital = 0
        
        self.angulo_axial = 0                                                               # Los angulos corresponden a la orientación
        self.angulo_coronal = 0                                                             # de la sección visualizada 
        self.angulo_sagital = 0
        
        self.puntuacion = set(string.punctuation)
        self.metadatos = []
        
    def asignarControlador(self,controlador):                                               # Se asigna el controlador al modelo
        self.__controlador = controlador
      
#%% A partir de esta sección se definen los métodos que tendra la clase para procesar información 
        
    def cargar_DICOM(self, directorio):                                                     # Se recorre el directorio cargado (raiz) y
        archivos_dcm = []                                                                   # se verifica si tiene archivos .dcm, en caso
        for directorio_raiz, directorios_ramas, archivos in os.walk(directorio):            # de existir se listan. De lo contrario
            for archivo in archivos:                                                        # se retorna Falso y termina la ejecución del
                if ".dcm" in archivo.lower():                                               # método cargar_DICOM
                    archivos_dcm.append(os.path.join(directorio_raiz, archivo))        
        if len(archivos_dcm) == 0:
            return False
        print("archivos_dcm: " + str(len(archivos_dcm)))
        
        # Para reconstruir el volúmen 3D a partir del conjunto de imagenes planares se requiere
        # tomar como referencia las filas, columnas y cantidad de cortes que lo segmentan
        
        self.imagen_referencia = pydicom.read_file(archivos_dcm[0], force = True)    
        for elemento in self.imagen_referencia:                                             # Se almacenan los metadatos en
            self.metadatos.append(str(elemento))                                            # forma de lista para desarrollar
                                                                                            # un buscador en el modelo
        self.filas = int(self.imagen_referencia.Rows)
        self.columnas = int(self.imagen_referencia.Columns)
        self.planos_por_imagen = int(self.imagen_referencia.SamplesPerPixel)
        self.cortes = len(archivos_dcm)
        
        self.volumen = np.zeros((self.filas, self.columnas, self.cortes),                   # Volumen de Referencia
                                  dtype = self.imagen_referencia.pixel_array.dtype)
        
        parametros_de_referencia = [self.filas, self.columnas, 
                                    self.planos_por_imagen, self.cortes]
        
        print("parametros_de_referencia: ")
        print(parametros_de_referencia)
        
        # Luego de tener las dimensiones de referencia del volumen, se rellena con cada una
        # de las imagenes 2D de los archivos .dcm para generar la estructura anatómica 3D
    
        tamaños_diferente_a_la_referencia = 0
        
        for i, corte in enumerate(archivos_dcm):
            
            imagen_2D = pydicom.read_file(corte)  
            
            if hasattr(imagen_2D, "PixelData"): 
                filas = imagen_2D.Rows
                columnas = imagen_2D.Columns
                planos_por_imagen = imagen_2D.SamplesPerPixel
                
                parametros_del_corte = [filas, columnas, planos_por_imagen, self.cortes]
                                                                                               # Sólo se agrega la imagen al volumen
            
                                                            # sí posee el atributo PixelData
                if (planos_por_imagen == 1) and (parametros_de_referencia == parametros_del_corte):
                    self.volumen[:, :, i] = imagen_2D.pixel_array                           # Volumen 3D generado y guardado
                
                elif (planos_por_imagen > 1) and (parametros_de_referencia == parametros_del_corte):
                    dimensiones_corte = imagen_2D.pixel_array.shape
                    print("dimensiones del corte en el else" + str(dimensiones_corte))
                    self.volumen[:,:, i] = imagen_2D.pixel_array[:,:,0]   
                    #self.volumen[:,:, :] = imagen_2D.pixel_array[:,:,np.newaxis] 
                    
                else:
                    tamaños_diferente_a_la_referencia = tamaños_diferente_a_la_referencia + 1
                    print(parametros_del_corte) 
                    
        print("\nEste estudio tiene {} imagenes de tamaños atípicos que no fueron leidas".format(tamaños_diferente_a_la_referencia))

        return True, self.volumen.shape, self.imagen_referencia

#%%
    def graficar_vista_axial(self, corte, angulo):                                          # Lee el angulo y el corte solicitado       
        self.corte_axial = corte                                                            # para enviarlo al modelo
        self.angulo_axial = angulo
        return ndimage.rotate(self.volumen[:,:,self.corte_axial], self.angulo_axial)                                         
                                                                                         
    def graficar_vista_coronal(self,corte, angulo):
        self.corte_coronal = corte
        self.angulo_coronal = angulo
        return ndimage.rotate(self.volumen[self.corte_coronal,:,:], self.angulo_coronal)
    
    def graficar_vista_sagital(self,corte, angulo):
        self.corte_sagital = corte
        self.angulo_sagital = angulo
        return ndimage.rotate(self.volumen[:,self.corte_sagital,:], self.angulo_sagital)
    
#%%
    def cargar_imagen_jpeg(self, archivo):                                                  # Carga la imagen jpeg
        return Image.open(archivo)
    
    def convertir_jpeg_a_DICOM(self, comando):                                              # Ejecuta el comando para convertir
        os.system(comando)                                                                  # formato jpeg -> DICOM

#%%
    def buscar_metadatos(self, palabras_clave):                                             # Recorre los elementos en los metadatos,
        resultado_de_busqueda = []                                                          # loa convierte a elementos dentro de una
        for elemento in self.metadatos:                                                     # lista, eliminando signos de puntuación
            elemento = ''.join([caracter for caracter in elemento if not caracter in self.puntuacion]).split()
            if palabras_clave in elemento:                                                  # y compara las palabras clave con los 
                resultado_de_busqueda.append(elemento)                                      # elementos de la lista para agregar
                                                                                            # a los resultados, aquellos elementos
        if len(resultado_de_busqueda) == 0:                                                 # que tengan almenos 1 coincidencia
            resultado_de_busqueda.append("No se encontraron coincidencias")
        
        return resultado_de_busqueda
        
    