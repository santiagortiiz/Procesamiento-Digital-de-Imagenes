# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 12:57:53 2020

@author: SANTIAGO
"""

# USO: Poner el nombre del directorio y ejecutar, la carpeta debe estar en el lugar del directorio"

import os
from PIL import Image

#%% Convertir Imagenes PNG a JPEG

'''
directorio_fuente = str("No DICOM/CT_NonCOVID")
directorio_destino = "Imagenes JPEG/CT No Covid/"
numero = 0

for directorio_raiz, directorios_ramas, archivos in os.walk(directorio_fuente): 
    for archivo in archivos:
        imagen = Image.open(directorio_fuente + '/' + str(archivo))
        imagen = imagen.convert('RGB')
        imagen.save(directorio_destino + str(numero) + ".jpeg")
        numero = numero + 1
'''

#%% RENOMBRAR ARCHIVOS
''' 
directorio = "GSPS_knee"

#for file in os.listdir("/home/career_karma"):
#	os.rename(file, f"/home/career_karma/old_{file}")

for directorio_raiz, directorios_ramas, archivos in os.walk(directorio): 
    for archivo in archivos:
        if (".dcm" in archivo.lower()) == False:
            os.rename(directorio + '/' + str(archivo), directorio + '/' + str(archivo) + ".dcm")
            
'''          
#%%
            