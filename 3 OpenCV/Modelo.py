# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:51:26 2020

@author: SANTIAGO
"""
 
#%% Librerias de procesamiento de información: "Back-end"
import cv2
import numpy as np
                                                                                                
#%%
class Procesador(object):
    def __init__(self):  
        self.camara = cv2.VideoCapture(0)                                                   # Se inicializan los atributos por defecto que tendra el modelo 
        self.frame = None
        self.frame_procesado = None
        self.umbral = 0
        self.kernel = np.ones((13,13),np.uint8)
        self.contornos = None
        self.centroides_x = []
        self.centroides_y = []        
        self.marcador = None
        self.contador_movimientos = 0
        
    def asignarControlador(self,controlador):                                               # Se asigna el controlador al modelo
        self.__controlador = controlador;
      
#%%     Camara
        
    def activar_camara(self):                                                               # Se abre la camara si no estaba previamente abierta
        if (self.camara.isOpened()):
            return True
        else:
            self.camara.open(0)
            return True
        
    def recuperar_frame(self):                                  
        ret, frame = self.camara.read()                                                     # Se captura el frame del objeto videoCapture
            
        if (ret == True):                                                                   # Si pudo leerse con exito, se establece el
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                             # espacio de color RGB y se ajusta a la pantalla
            #self.frame = cv2.flip(frame)                                                   # rotandolo 90 grados
            self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)             # Se crea un frame sobre el cual van los procesamientos
            self.frame_procesado = np.copy(self.frame)
            return self.frame                                                               # Se retorna el frame capturado por la camara
        
        else:
            return False
        
    def recuperar_frame_procesado(self):                                                    # Retorna el frame procesado
        return self.frame_procesado
    
    def inicializar_marcador(self):                                                         # Genera un frame en blanco sobre el cual 
        self.marcador = np.ones_like(self.frame[:,:,0])                                     # se identifica el marcador
        
    def recuperar_marcador(self):                                                           # Se recupera el frame del marcador
        return self.marcador
        
    def apagar_camara(self):                                                                # Se apaga la camara y retorna un Falso
        if (self.camara.isOpened()):
            self.camara.release()
            print("\n la camara estaba abierta y se ha cerrado con extio")
            
        return False

#%%     Procesamiento de Frame
            
    def extraer_color(self, color):                                                         # Coloca en 0 los pixeles de los canales
                                                                                            # que no corresponden al color seleccionado
        if (color == 'Rojo'):
            self.frame_procesado[:,:,1] = 0
            self.frame_procesado[:,:,2] = 0
        
        elif (color == 'Verde'):
            self.frame_procesado[:,:,0] = 0
            self.frame_procesado[:,:,2] = 0
        
        elif (color == 'Azul'):
            self.frame_procesado[:,:,0] = 0
            self.frame_procesado[:,:,1] = 0
    
    def ecualizar_color(self, color):                                                       # Ecualiza el histograma del color seleccionado                                                    
        if (color == 'Rojo'): 
            color = 0
        elif (color == 'Verde'): 
            color = 1
        elif (color == 'Azul'): 
            color = 2
            
        self.frame_procesado[:,:,color] = cv2.equalizeHist(self.frame_procesado[:,:,color])
 
    def aplicar_correccion_gamma(self, factor_gamma):                                       # Aplica la correccion Gamma al frame procesado
        frame_normalizado = np.array(self.frame_procesado, np.float32)/255                  # Inicialmente se normaliza el frame
        frame_gamma = frame_normalizado**factor_gamma                                       # y luego se aplica el factor gamma
        self.frame_procesado = np.copy(frame_gamma)
        
    def binarizar(self, tipo_binarizacion, umbral):                                         # Binariza la imagen segun el metodo y umbral
        if (tipo_binarizacion == "THRESH_BINARY"):                                          # seleccionado
            self.umbral, self.frame_procesado = cv2.threshold(self.frame_procesado, umbral, 255, cv2.THRESH_BINARY)
        
        elif (tipo_binarizacion == "THRESH_BINARY_INV"):
            self.umbral, self.frame_procesado = cv2.threshold(self.frame_procesado, umbral, 255, cv2.THRESH_BINARY_INV)
        
        elif (tipo_binarizacion == "THRESH_TRUNC"):
            self.umbral, self.frame_procesado = cv2.threshold(self.frame_procesado, umbral, 255, cv2.THRESH_TRUNC)
        
        elif (tipo_binarizacion == "THRESH_TOZERO"):
            self.umbral, self.frame_procesado = cv2.threshold(self.frame_procesado, umbral, 255, cv2.THRESH_TOZERO)
        
        elif (tipo_binarizacion == "THRESH_TOZERO_INV"):
            self.umbral, self.frame_procesado = cv2.threshold(self.frame_procesado, umbral, 255, cv2.THRESH_TOZERO_INV)
      
    def aplicar_transformacion_morfologica(self, transformacion, iteraciones):              # Aplica la correccion morfologica
        if (transformacion == 'erosionar'):                                                 # seleccionada y la repita el numero de iteraciones
            self.frame_procesado = cv2.erode(self.frame_procesado, self.kernel, iterations = iteraciones)
    
        elif (transformacion == 'dilatar'):
            self.frame_procesado = cv2.dilate(self.frame_procesado, self.kernel, iterations = iteraciones)  
        
        elif (transformacion == 'apertura'):
            self.frame_procesado = cv2.morphologyEx(self.frame_procesado, cv2.MORPH_OPEN, self.kernel, iterations = iteraciones)  

        elif (transformacion == 'cierre'):
            self.frame_procesado = cv2.morphologyEx(self.frame_procesado, cv2.MORPH_CLOSE, self.kernel, iterations = iteraciones)  
    
    def identificar_contornos(self, color):                                                 # Identifica los contornos sobre el frame procesado
        if (color == 'Rojo'):                                                               # y los dibuja sobre la imagen
            color = 0
            
        elif (color == 'Verde'): 
            color = 1
            
        elif (color == 'Azul'): 
            color = 2

        self.contornos, jerarquia = cv2.findContours(self.frame_procesado[:,:,color], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        self.frame_procesado = cv2.drawContours(self.frame.copy(), self.contornos, -1, (200,0,0), 15)
            
    def caracterizar_contornos(self, contorno_de_interes):
        areas = [cv2.contourArea(contorno) for contorno in self.contornos]                  # Calcula las areas de los contornos encontrados
        
        try:
            contorno_de_interes = self.contornos[areas.index(max(areas)) - contorno_de_interes] # Selecciona el contorno de mayor area
            momentos = cv2.moments(contorno_de_interes)                                     # Calcula los momentos que caracterizan el contorno de interes
            
            centroide_x = int(momentos['m10']/momentos['m00'])                              # Se calcula el centroide del contorno
            centroide_y = int(momentos['m01']/momentos['m00'])
            
            radio = 30                                                                      # Se establecen los parametros del contorno
            color = (0,0,255)
            espesor = 1
            
            self.frame_procesado = cv2.circle(self.frame_procesado,(centroide_x, centroide_y), radio, color, espesor) # Se grafica el centroide
            self.marcador = cv2.circle(self.marcador,(centroide_x, centroide_y), 5, color, -1) # Se grafica el centroide en el frame marcador
           
            if (self.contador_movimientos == 0):                                            # Si es el primer movimiento se inicializa
                self.inicializar_marcador()                                                 # el frame del marcador
                
            self.contador_movimientos += 1
            
            if (self.contador_movimientos == 1):                                            # Se añaden el 1 y el ultimo movimiento
                self.centroides_x.append(centroide_x)                                       # a la lista de centroides
                self.centroides_y.append(centroide_y)
                
            elif (self.contador_movimientos == 20):
                self.centroides_x.append(centroide_x)
                self.centroides_y.append(centroide_y)
                return True
            
            elif (self.contador_movimientos == 40):                                         # Luego de 40 movimientos capturados se reinicia
                self.contador_movimientos = 0
            
            return False
            
        except:
            print("\nContorno no identificado")
            return False
            
    def clasificar_movimiento(self):
        tolerancia = 40
        derecha = False
        izquierda = False
        arriba = False
        abajo = False
        superior_izquierda = False
        superior_derecha = False
        inferior_izquierda = False
        inferior_derecha = False
        
        x_1 = self.centroides_x[0]                                                          # Punto inicial del movimiento
        y_1 = self.centroides_y[0]
         
        x_2 = self.centroides_x[1]                                                          # Punto final del movimiento
        y_2 = self.centroides_y[1]
        
        self.centroides_x.clear()                                                           # Reiniciar centroides
        self.centroides_y.clear() 
        
                                                                                            # Criterios de identificacion de movimiento
        if (y_2 > y_1 and np.abs(y_2 - y_1) > tolerancia  and np.abs(x_2 - x_1) < tolerancia):
            derecha = True
            
        if (y_1 > y_2 and np.abs(y_2 - y_1) > tolerancia  and np.abs(x_2 - x_1) < tolerancia):
            izquierda = True
        
        if (x_1 > x_2 and np.abs(x_2 - x_1) > tolerancia  and np.abs(y_2 - y_1) < tolerancia):
            arriba = True
            
        if (x_2 > x_1 and np.abs(x_2 - x_1) > tolerancia  and np.abs(y_2 - y_1) < tolerancia):
            abajo = True
        
        if  (x_2 > x_1 and np.abs(x_2 - x_1) > tolerancia and np.abs(y_2 - y_1) > tolerancia):
            if (y_2 > y_1):
                inferior_derecha = True        
                
            elif (y_1  > y_2):
                inferior_izquierda = True
        
        if  (x_1 > x_2 and np.abs(x_2 - x_1) > tolerancia and np.abs(y_2 - y_1) > tolerancia):
            if (y_2 > y_1):
                superior_derecha = True        
                
            elif (y_1  > y_2):
                superior_izquierda = True
                                                                                            # Indicador triangular del movimiento
        # Arriba
        if (arriba == True):
            x1 = 0
            y1 = 320
            x2 = 60
            y2 = 260
            x3 = 60
            y3 = 380
            
        # Abajo
        elif (abajo == True):
            x1 = 430
            y1 = 280
            x2 = 480
            y2 = 320
            x3 = 430
            y3 = 360
        
        # Derecha
        elif (derecha == True):
            x1 = 280
            y1 = 560
            x2 = 240
            y2 = 640
            x3 = 200
            y3 = 560
        
        # Izquierda
        elif (izquierda == True):
            x1 = 240
            y1 = 0
            x2 = 280
            y2 = 60
            x3 = 200 
            y3 = 60
           
        # Suerior Izquierda
        elif (superior_izquierda == True):
            x1 = 0
            y1 = 0
            x2 = 100
            y2 = 0
            x3 = 0 
            y3 = 100
        
        # Suerior Derecha
        elif (superior_derecha == True):
            x1 = 0
            y1 = 640
            x2 = 100
            y2 = 640
            x3 = 0 
            y3 = 540
        
        # Inferior Derecha
        elif (inferior_derecha == True):
            x1 = 480
            y1 = 560
            x2 = 480
            y2 = 640
            x3 = 400
            y3 = 640
        
        # Inferior Izquierda
        elif (inferior_izquierda == True):
            x1 = 410
            y1 = 0
            x2 = 480
            y2 = 0
            x3 = 480 
            y3 = 80
        
        try:
            direccion = np.array( [ [x1, y1], [x2, y2], [x3, y3] ])
            self.marcador = cv2.drawContours(self.marcador, [direccion], -1, (0,0,0), 5)
        
        except:
            print("No se logró clasificar el movimiento")
         
        
#%%     Calculo de Histogramas
    def calcular_histograma_original(self):                                                 # Histogramas del frame original
        histograma_R = cv2.calcHist([self.frame[:,:,0]],[0],None,[256],[0,256])
        histograma_G = cv2.calcHist([self.frame[:,:,1]],[0],None,[256],[0,256])
        histograma_B = cv2.calcHist([self.frame[:,:,2]],[0],None,[256],[0,256])
        
        return [histograma_R[:,0], histograma_G[:,0], histograma_B[:,0]]
    
    def calcular_histograma_procesado(self):                                                # Histogramas del frame procesado
        if (np.max(self.frame_procesado) <= 1):                                             # Hist. de la imagen binaria
            histograma_procesado_R = cv2.calcHist([self.frame_procesado],[0],None,[256],[0,1])
            histograma_procesado_G = cv2.calcHist([self.frame_procesado],[1],None,[256],[0,1])
            histograma_procesado_B = cv2.calcHist([self.frame_procesado],[2],None,[256],[0,1])    
        
        else:                                                                               # Hist. de la imagen normal
            histograma_procesado_R = cv2.calcHist([self.frame_procesado],[0],None,[256],[0,256])
            histograma_procesado_G = cv2.calcHist([self.frame_procesado],[1],None,[256],[0,256])
            histograma_procesado_B = cv2.calcHist([self.frame_procesado],[2],None,[256],[0,256])
        
        return [histograma_procesado_R[:,0], histograma_procesado_G[:,0], histograma_procesado_B[:,0]]
         
        
        
        