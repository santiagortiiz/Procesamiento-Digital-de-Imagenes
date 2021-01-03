# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:51:28 2020

@author: SANTIAGO
"""
#%% Librerias para el diseño de la interfaz de Usuario: "Front-end"

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout                           # Librerias necesarias para crear ventanas
from PyQt5.uic import loadUi                                                                # Libreria para cargar diseños en QtDesigner

from matplotlib.figure import Figure                                                        # Librerias para crear Figuras
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.gridspec as gridspec

#%% Objetos Figuras para graficar

class FiguraCanvas_1(FigureCanvas):                                                         # Clase Figura creada para graficar 
    def __init__(self, parent = None, ancho = 10, alto = 10, dpi = 100):                    # las imagenes médicas en formato DICOM                 
        self.Figura_1 = Figure(figsize = (ancho, alto), dpi = dpi)    
        self.Figura_1.set_facecolor('#cfebfb') # #052b2e #dffdfd <- #99f7f7
        
        gs = gridspec.GridSpec(1, 3, width_ratios=[50,50,50], height_ratios=[50])           # Se crea un gridspec para mejor el 
        self.plano_axial = self.Figura_1.add_subplot(gs[0])                                 # tamaño de las imagenes graficadas
        self.plano_coronal = self.Figura_1.add_subplot(gs[1])
        self.plano_sagital = self.Figura_1.add_subplot(gs[2])
        
        self.plano_axial.set_title("Plano Transversal")
        self.plano_coronal.set_title("Plano Frontal")
        self.plano_sagital.set_title("Plano Sagital")
        self.contador_imagen_guardada = 0
        #self.Figura_1.set_tight_layout(True)
        
        FigureCanvas.__init__(self, self.Figura_1)
        
    def graficar_axial(self,datos):                                                         # Plano Axial o Transversal
        self.plano_axial.clear()
        self.plano_axial.imshow(datos, cmap="gray")
        self.plano_axial.axis("off") 
        self.plano_axial.figure.canvas.draw()

    def graficar_coronal(self,datos):                                                       # Plano Coronal o Frontal
        self.plano_coronal.clear()
        self.plano_coronal.imshow(datos, cmap="gray")
        self.plano_coronal.axis("off") 
        self.plano_coronal.figure.canvas.draw()
        
    def graficar_sagital(self,datos):                                                       # Plano Sagital (Divide en mitad izquierda y derecha)
        self.plano_sagital.clear()
        self.plano_sagital.imshow(datos, cmap="gray")
        self.plano_sagital.axis("off") 
        self.plano_sagital.figure.canvas.draw()
        
    def guardar_vista_axial(self):
        self.contador_imagen_guardada = self.contador_imagen_guardada + 1                                                      
        extent = self.plano_axial.get_window_extent().transformed(self.Figura_1.dpi_scale_trans.inverted())
        self.Figura_1.savefig('vista_axial_' + str(self.contador_imagen_guardada) + '.jpeg', bbox_inches=extent)                       # Se guarda la sección de la figura 
                                                                                            # que corresponde al plano deseado
    def guardar_vista_coronal(self):
        self.contador_imagen_guardada = self.contador_imagen_guardada + 1 
        extent = self.plano_coronal.get_window_extent().transformed(self.Figura_1.dpi_scale_trans.inverted())
        self.Figura_1.savefig('vista_coronal_' + str(self.contador_imagen_guardada) + '.jpeg', bbox_inches=extent)
    
    def guardar_vista_sagital(self):
        self.contador_imagen_guardada = self.contador_imagen_guardada + 1 
        extent = self.plano_sagital.get_window_extent().transformed(self.Figura_1.dpi_scale_trans.inverted())
        self.Figura_1.savefig('vista_sagital_' + str(self.contador_imagen_guardada) + '.jpeg', bbox_inches=extent)


class FiguraCanvas_2(FigureCanvas):                                                         # Clase figura creada para graficar
    def __init__(self, parent = None, ancho = 100, alto = 100, dpi = 100):                  # las imagenes JPEG cargadas
        self.Figura_2 = Figure(figsize = (ancho, alto), dpi = dpi)      
        self.Figura_2.set_facecolor('#3a0b23')
        
        self.imagen_jpeg = self.Figura_2.add_subplot(111)     
        self.Figura_2.set_tight_layout(True)
        
        FigureCanvas.__init__(self, self.Figura_2)
        
    def graficar_imagen_jpeg(self,datos):                                                   # Imagen JPEG cargada
        self.imagen_jpeg.clear()
        self.imagen_jpeg.imshow(datos)
        self.imagen_jpeg.axis("off") 
        self.imagen_jpeg.figure.canvas.draw()
        
#%% Objetos Ventanas presentes en la Interfaz de Usuario

class InterfazGrafica(QMainWindow):
    def __init__(self, ppal = None):
        super(InterfazGrafica,self).__init__()                                              # Carga la ventana de QtDesigner
        loadUi('InterfazGrafica.ui', self)  
        
        self.estructura()                                                                   # Llama la estructura de la ventana
        
        self.corte_axial = 0                                                                # Los cortes corresponden a la sección
        self.corte_coronal = 0                                                              # visualizada
        self.corte_sagital = 0
        
        self.angulo_axial = 0                                                               # Los angulos corresponden a la orientación
        self.angulo_coronal = 0                                                             # de la sección visualizada 
        self.angulo_sagital = 0
        
        self.metadatos_del_estudio = None
        self.archivoCargado = ''
        
    def asignarControlador(self, controlador):                                              # Se asigna el controlador a la ventana de inicio
        self.__controlador = controlador   
        
    def estructura(self):                                                                   
        layout_1 = QVBoxLayout()
        self.espacio_grafico_1.setLayout(layout_1)                                          # Se inserta un QVBox en el espacio_grafico_1,
        self.figura_1 = FiguraCanvas_1(self.espacio_grafico_1)                              # se Instancia el objeto FiguraCanvas en figura_1
        layout_1.addWidget(self.figura_1)                                                   # y se añade al espacio_grafico_1 que esta en layout_1

        layout_2 = QVBoxLayout()
        self.espacio_grafico_2.setLayout(layout_2)                                          
        self.figura_2 = FiguraCanvas_2(self.espacio_grafico_2)                                
        layout_2.addWidget(self.figura_2)
        
        self.estaciones_de_la_App.hide()                                                    # Al iniciar la aplicacion se ocultan
        self.estadoPaciente.hide()                                                          # los objetos de cada estación
        self.ocultar_objetos_estacion_1()
        self.ocultar_objetos_estacion_2()
        self.ocultar_objetos_estacion_3()
        
#%% Rutina de carga de archivos DICOM
        
    def cargar_DICOM(self):
        directorio = QFileDialog.getExistingDirectory(self, "Seleccione un directorio", ".",
                                                      QFileDialog.ShowDirsOnly)             # Se le pide al usuario ingresar un directorio y sí ingresa uno
                                                                                            # con archivos .dcm se procede a graficar un corte inicial de la
        if directorio != "":                                                                # estructura anatómica en cada plano
            (directorio_valido, 
             dimension_volumen, 
             imagen_referencia) = self.__controlador.cargar_DICOM(directorio) 
            
            if directorio_valido == True:
                 
                self.mostrar_objetos_estacion_1()
                self.mostrar_objetos_estacion_2()
                self.botonCargarJPEG.show()
                self.reiniciar_parametros(dimension_volumen)                                # Se reinician los parametros
                self.graficar_3_planos_anatomicos()                                         # Se llaman los metodos de visualizacion
                self.metadatos_del_estudio = imagen_referencia
                self.mostrar_metadatos()
                
#%% Visualización de todos los planos Anatómicos
                
    def graficar_3_planos_anatomicos(self):                                                 # Llama las funciones graficar
        self.graficar_vista_axial()                                                         # de cada plano anatómico
        self.graficar_vista_coronal()
        self.graficar_vista_sagital()
                
#%% Visualización de cada plano Anatómico
                
    def graficar_vista_axial(self):
        self.figura_1.graficar_axial(
            self.__controlador.graficar_vista_axial(self.corte_axial, self.angulo_axial))
        
    def graficar_vista_coronal(self):
        self.figura_1.graficar_coronal(
            self.__controlador.graficar_vista_coronal(self.corte_coronal, self.angulo_coronal))
        
    def graficar_vista_sagital(self):
        self.figura_1.graficar_sagital(
            self.__controlador.graficar_vista_sagital(self.corte_sagital, self.angulo_sagital))
        
#%% Barrido de cada plano Anatómico
        
    def barrido_axial(self):
        self.corte_axial = self.barridoAxial.value()                                        # Se leen los valores de ubicación de
        self.graficar_vista_axial()                                                         # cada QSlider correspondiente a cada
        print(self.corte_axial)                                                             # corte Anatómico, y se le pide dicho
    def barrido_coronal(self):                                                              # corte al controlador
        self.corte_coronal = self.barridoCoronal.value()
        self.graficar_vista_coronal()
        print(self.corte_coronal)
    def barrido_sagital(self):
        self.corte_sagital = self.barridoSagital.value()
        self.graficar_vista_sagital()
        print(self.corte_sagital)
        
#%% Rotación de cada plano Anatómico
        
    def rotar_vista_axial(self):                                                            # Se gira el plano anatómico 
        self.angulo_axial = self.angulo_axial + 90                                          # clickeado 90 grados y se grafica
        if self.angulo_axial == 360: 
            self.angulo_axial = 0
        self.graficar_vista_axial()
        
    def rotar_vista_coronal(self):
        self.angulo_coronal = self.angulo_coronal + 90
        if self.angulo_coronal == 360: 
            self.angulo_coronal = 0
        self.graficar_vista_coronal()
        
    def rotar_vista_sagital(self):
        self.angulo_sagital = self.angulo_sagital + 90
        if self.angulo_sagital == 360: 
            self.angulo_sagital = 0
        self.graficar_vista_sagital()
    
#%%
    def guardar_vista_axial(self):                                                          # Se llaman los métodos guardar
        self.figura_1.guardar_vista_axial()                                                 # de cada vista dentro de la figura 1
        
    def guardar_vista_coronal(self):
        self.figura_1.guardar_vista_coronal()
    
    def guardar_vista_sagital(self):
        self.figura_1.guardar_vista_sagital()
     
#%% Inicialización de parámetros
    
    def reiniciar_parametros(self, dimension_volumen):
        self.barridoAxial.setMaximum(dimension_volumen[2]-1)                                # Se ajustan los rangos de barrido de cada plano anatómico
        self.barridoCoronal.setMaximum(dimension_volumen[0]-1)
        self.barridoSagital.setMaximum(dimension_volumen[1]-1)
                
        self.barridoAxial.setValue(0)                                                       # Se reinicia la posición inicial de cada plano anatómico
        self.barridoCoronal.setValue(0)
        self.barridoSagital.setValue(0)
        
        self.corte_axial = 0                                                                # Se reinician los parámetros de corte y angulo                                              
        self.corte_coronal = 0                                                              # siempre que se cargue un archivo nuevo
        self.corte_sagital = 0
        
        self.angulo_axial = 0                                                              
        self.angulo_coronal = 0                                                             
        self.angulo_sagital = 0
        
        self.metadatos_del_estudio = None                                                   # Se limpian los metadatos mostrados
        self.mostrar_metadatos()                                                            # en la estacion 2
    
#%%
    def mostrar_metadatos(self):
        self.campo_metadatos.setText(str(self.metadatos_del_estudio))                       # En el campo de metadatos se imprime la
                                                                                            # información cargada en la imagen de referencia
    def buscar_metadatos(self):
        palabras_clave = str(self.buscador_de_metadatos.text())                             # Toma las palabras escritas en el buscador
        resultado_de_busqueda = self.__controlador.buscar_metadatos(palabras_clave)         # y se las envia al controlador para ejecutar
        self.campo_resultados_busqueda.clear()                                              # la búsqueda, cuyos resultados se imprimen
        self.campo_resultados_busqueda.setPlainText("\n".join(map(str, resultado_de_busqueda))) # en la estacion 2
        
#%%                                                                                         # A tener en cuenta: LA IMAGEN CARGADA
    def cargar_imagen_jpeg(self):                                                           # DEBE ESTAR EN LA CARPETA:
        self.archivoCargado, _ = QFileDialog.getOpenFileName(self,"Seleccione una Imagen JPEG","", # Conversor_jpeg_DICOM <--
                                                             "Images (*.jpeg *.jpg)")
                                                                                            # Se le pide al usuario ingresar una
        if self.archivoCargado != "":                                                       # imagen y se grafica, a la vez se
            imagen_cargada = self.__controlador.cargar_imagen_jpeg(self.archivoCargado)     # muestran los objetos presentes en 
            self.figura_2.graficar_imagen_jpeg(imagen_cargada)                              # la estación
            self.mostrar_objetos_estacion_3()
        
    def convertir_jpeg_a_DICOM(self):                                                       # Se recolecta la informacion de la interfaz
        nombre_institucion = "-k 0008,0080=" + '"' + str(self.lineEdit_1.text()) + '"' + ' '# y se ordena en forma de comando de ejecucion
        direccion = "-k 0008,0081=" + '"' + str(self.lineEdit_2.text()) + '"' + ' '         # para que el modelo lo ejecute en el cmd
        descripcion_estudio = "-k 0008,0030=" + '"' + str(self.lineEdit_3.text()) + '"' + ' '
        nombre_paciente = "-k 0010,0010=" + '"' + str(self.lineEdit_4.text()) + '"' + ' '
        ID_paciente = "-k 0010,0020=" + '"' + str(self.lineEdit_5.text()) + '"' + ' '
        fecha_nacimiento = "-k 0010,0030=" + '"' + str(self.lineEdit_6.text()) + '"' + ' '
        sexo_paciente = "-k 0010,0040=" + '"' + str(self.lineEdit_7.text()) + '"' + ' '
        edad_paciente = "-k 0010,1010=" + '"' + str(self.lineEdit_8.text()) + '"'
        nombre_imagen_dcm = str("Conversor_jpeg_DICOM\\") + str(self.lineEdit_9.text()).replace(' ','_') + ".dcm "
        nombre_imagen_jpeg =str(self.archivoCargado[74:])
        formulario_metadatos = str(nombre_institucion + direccion + descripcion_estudio +
                                   nombre_paciente + ID_paciente + fecha_nacimiento +
                                   sexo_paciente + edad_paciente)
        hogar_DCMTK = "dcmtk\\tools\\dcmtk-3.6.5-win64-dynamic\\bin\\img2dcm "
        
        comando = str(hogar_DCMTK + 
                      "Conversor_jpeg_DICOM\\" + nombre_imagen_jpeg + ' ' +
                      nombre_imagen_dcm + formulario_metadatos)
       
        self.__controlador.convertir_jpeg_a_DICOM(comando)
        
#%% Los siguientes métodos permiten jugar con la estética de la interfaz
    
    def comenzar_aplicacion(self):
        self.estaciones_de_la_App.show()                                                    # Muestra los objetos de inicio
        self.estadoPaciente.show()
        self.Comenzar.hide()
        self.ocultar_objetos_estacion_1()

#%%        
    def cambio_de_estacion(self):                                                           # Sí el usuario cambia de estacion
        estacion_actual = self.estaciones_de_la_App.currentIndex()                          # se cambia la imagen de fondo
        
        if estacion_actual == 0:
            self.fondo_2.hide()
            self.fondo_3.hide()
            
            self.fondo_1.show()
            
        elif estacion_actual == 1:
            self.fondo_1.hide()
            self.fondo_3.hide()
            
            self.fondo_2.show()
            
        elif estacion_actual == 2:
            self.fondo_1.hide()
            self.fondo_2.hide()
            
            self.fondo_3.show()
  
#%%
    def continuar_pausar_aplicacion(self):                                                  # Permite ver la imagen de fondo
        estado_paciente = self.estadoPaciente.currentText()                                 # de la estacion actual en cualquier
                                                                                            # momento
        if estado_paciente == "Todo bajo control":
            self.mostrar_objetos_estacion_1()
            self.mostrar_objetos_estacion_2()
            self.mostrar_objetos_estacion_3()
            
        elif estado_paciente == "Un descansito doctor":
            self.ocultar_objetos_estacion_1()
            self.ocultar_objetos_estacion_2()
            self.ocultar_objetos_estacion_3()
                
        elif estado_paciente == "Todo un exito, salir":
            self.estaciones_de_la_App.setCurrentIndex(0)
            self.ocultar_objetos_estacion_1()
            self.ocultar_objetos_estacion_2()
            self.ocultar_objetos_estacion_3()
            
            self.campo_metadatos.clear()
            self.buscador_de_metadatos.clear()
            self.campo_resultados_busqueda.clear()
            
            self.estaciones_de_la_App.hide()
            self.estadoPaciente.hide()
            self.Comenzar.show()

#%%         
    def ocultar_objetos_estacion_1(self):
        self.figura_1.hide()
        self.botonRotarAxial.hide()
        self.botonRotarCoronal.hide()
        self.botonRotarSagital.hide()
        
        self.barridoAxial.hide()
        self.barridoCoronal.hide()
        self.barridoSagital.hide()
        
        self.guardar_1.hide()
        self.guardar_2.hide()
        self.guardar_3.hide()
        
    def ocultar_objetos_estacion_2(self):
        self.Titulo_Buscador.hide()
        self.campo_metadatos.hide()
        self.buscador_de_metadatos.hide()
        self.campo_resultados_busqueda.hide()
    
    def ocultar_objetos_estacion_3(self):
        self.botonConvertirJPEG2DICOM.hide()
        self.figura_2.hide()
        
        self.Titulo_Formulario.hide()
        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        
        self.lineEdit_1.hide()
        self.lineEdit_2.hide()
        self.lineEdit_3.hide()
        self.lineEdit_4.hide()
        self.lineEdit_5.hide()
        self.lineEdit_6.hide()
        self.lineEdit_7.hide()
        self.lineEdit_8.hide()
        self.lineEdit_9.hide()
   
#%%
    def mostrar_objetos_estacion_1(self):
        self.figura_1.show()
        self.botonRotarAxial.show()
        self.botonRotarCoronal.show()
        self.botonRotarSagital.show()
        
        self.barridoAxial.show()
        self.barridoCoronal.show()
        self.barridoSagital.show()
        
        self.guardar_1.show()
        self.guardar_2.show()
        self.guardar_3.show()
                       
    def mostrar_objetos_estacion_2(self):
        self.Titulo_Buscador.show()
        self.campo_metadatos.show()
        self.buscador_de_metadatos.show()
        self.campo_resultados_busqueda.show()
    
    def mostrar_objetos_estacion_3(self):
        self.botonCargarJPEG.show()
        self.botonConvertirJPEG2DICOM.show()
        self.figura_2.show()
        
        self.Titulo_Formulario.show()
        self.label_2.show()
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()
        self.label_7.show()
        self.label_8.show()
        self.label_9.show()
        self.label_10.show()
        
        self.lineEdit_1.show()
        self.lineEdit_2.show()
        self.lineEdit_3.show()
        self.lineEdit_4.show()
        self.lineEdit_5.show()
        self.lineEdit_6.show()
        self.lineEdit_7.show()
        self.lineEdit_8.show()
        self.lineEdit_9.show()
        