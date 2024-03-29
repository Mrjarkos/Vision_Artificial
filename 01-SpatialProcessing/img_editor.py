import sys
import os
import io
from browsefile import BrowseFile
from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets, QtGui, QtCore

import numpy as np
import matplotlib.pyplot as plt
from imageio import imread
import cv2
from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import random
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy import signal
from scipy.ndimage import gaussian_filter
import time

def average_filter(image,N):
    kernel = np.ones((N,N))/(N*N)
    newimage = cv2.filter2D(image,-1,kernel)
    return newimage

def gauss_filter(img, N, s):
    t=(((N - 1)/2)-0.5)/s
    return gaussian_filter(img, sigma=s, truncate=t)

def sobel_filter(image):
    if len(image.shape)==2:
        gx = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        gy = cv2.Sobel(image, cv2.CV_64F, 0, 1)
        
    else:
        #cv2.Sobel(imagen, 32 bits flotante, derivada en x, derivada en y)
        gx = cv2.Sobel(image[:,:,0], cv2.CV_64F, 1, 0)
        gy = cv2.Sobel(image[:,:,0], cv2.CV_64F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    return np.uint8(mag)

def gamma(image, gamma):
    #Crea una tabla con el factor gamma
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # Aplica el factor gamma a cada uno de los pixeles de la imagen
    return cv2.LUT(image, table)

def Cv_to_QPixmap(image):
    if len(image.shape)==2:
        height, width = image.shape
        qImg = QtGui.QImage( image.data, width, height, width, QtGui.QImage.Format_Grayscale8)
    else: 
        height, width, channel = image.shape
        bytesPerLine = 3*width
        print(f"Alto:{height}Ancho:{width}:chanel:{channel}")
        print(f"Bytes:{bytesPerLine}")
        qImg = QtGui.QImage( image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
    PIX2 = QtGui.QPixmap(qImg)
    return PIX2

def histogramer(image):
    figure = Figure(figsize=[4.7,3.8])
    axes = figure.gca()

    #si las dimensiones de la imagen son 2 es gris
    if len(image.shape)==2:
        #calcula el histograma convirtiendolo a arreglo
        hist = cv2.calcHist([image],[0],None,[256],[0,256])
        #Para graficar en python
        axes.plot(hist)
    else:
        for i,col in enumerate(('b','g','r')):
            hist = cv2.calcHist([image],[i],None,[256],[0,256])
            #Para graficar en python
            axes.plot(hist, f"-{col}")
    axes.grid(True)

    canvas = FigureCanvas(figure)
    return canvas

def Inf_Degrade(image):
    dmin=0
    dmax=255
    pattern = np.array([np.arange(image.shape[0])]).repeat(image.shape[1],0)/image.shape[0]
    pattern = np.flip(pattern)
    if len(image.shape)==2:
        pattern = np.transpose(pattern)
    else:
        pattern = [pattern, pattern, pattern]
        pattern = np.transpose(pattern)

    return np.uint8(np.clip(pattern*image, dmin, dmax-1))

def R_Degrade(image):
    dmin=0
    dmax=255
    pattern = np.transpose(np.array([np.arange(image.shape[1])]).repeat(image.shape[0],0)/image.shape[1])
    pattern = np.flip(pattern)
    if len(image.shape)!=2:
        pattern=np.transpose(np.array([pattern,pattern,pattern]))
    while True:
        try:
            return np.uint8(np.clip(pattern*image, dmin, dmax-1))
            break
        except:
            return np.uint8(np.clip(np.transpose(pattern)*image, dmin, dmax-1))

class Dialogo(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.resize(300, 300)
        dir2=os.path.dirname(os.path.abspath(__file__))
        directory2=dir2+"\Dialogo_Guardar.ui"
        uic.loadUi(directory2,self)
        #uic.loadUi('Dialogo_Guardar.ui',self)
        self.setWindowTitle("Guardar Imagen")

class ejemplo(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        dir=os.path.dirname(os.path.abspath(__file__))
        directory=dir+"\gui.ui"
        self.ex = BrowseFile() 
        uic.loadUi(directory,self)
        #uic.loadUi('gui.ui',self)
        self.img = None
        self.max_size = 10
        self.buffer = []
        
        self.a = 1
        self.b = 0
        self.OpenImageButton.clicked.connect(self.Open_Image)

        self.GrayScaleButton.clicked.connect(self.Convert2Gray)

        self.Equalize_Button.clicked.connect(self.Equalize)

        self.ComboBoxFiltro.addItem("Average")
        self.ComboBoxFiltro.addItem("Gaussian")
        self.ComboBoxFiltro.addItem("Sobel")
        self.comboBoxKernel.addItem("5x5")
        self.comboBoxKernel.addItem("10x10")
        self.comboBoxKernel.addItem("20x20")

        self.Apply_Filter_Button.clicked.connect(self.Filter)
        self.Apply_Edition_Button.clicked.connect(self.ApplyChanges)
        self.BrilloSlider.valueChanged.connect(self.Cambiar_Brillo) 
        self.BrilloSlider.setMinimum(-50)
        self.BrilloSlider.setMaximum(50)
        self.BrilloSlider.setSingleStep(2)
        

        self.ContrastSlider.valueChanged.connect(self.Cambiar_Contraste) 
        self.ContrastSlider.setMinimum(10)
        self.ContrastSlider.setMaximum(35)
        self.ContrastSlider.setSingleStep(5)
        
        self.GammSlider.valueChanged.connect(self.Cambiar_Gamma) 
        self.GammSlider.setMinimum(5)
        self.GammSlider.setMaximum(30)
        self.GammSlider.setSingleStep(5)

        self.NegativoButton.clicked.connect(self.negative)

        self.DegragadoVButton.clicked.connect(self.VDegrade)
        self.DegragadoHButton.clicked.connect(self.HDegrade)

        self.dialog=Dialogo()

        self.Save_Button.clicked.connect(self.Abrir_Guardar)
        self.dialog.Ok_Save_Button.clicked.connect(self.Guardar_Imagen)

        self.UndoButton.clicked.connect(self.Undo)

        self.Errores=QtWidgets.QErrorMessage(self)

    def Undo(self):
        if len(self.buffer)>0:
            self.img=self.buffer.pop()

        PIXEL_MAP=Cv_to_QPixmap(self.img)
        self.Processed_Image.setPixmap(PIXEL_MAP)
        #Propiedades
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()

        #histograma
        self.mostrar_histograma()


    def Abrir_Guardar(self):
        if self.ex.saveFileDialog():
            self.Guardar_Imagen()
        #self.dialog.Label_Guardar_Exitoso.clear()
        #self.dialog.Text.clear()
        #self.dialog.exec_()

    def Guardar_Imagen(self):

        while True:
            try:
                #self.dialog.etiqueta.setText("Dialogo abierto")
                #self.dialog.Input_Text.showMessage("Error","Error")
                dir=self.ex.returnSaveName()
                print(dir)
                editimage = self.img
                cv2.imwrite(dir, editimage)
                self.Errores.showMessage(f"El Archivo Se Ha Guardado Exitosamente En:{dir}","Operación Exitosa")
                break 
            except :
                self.Errores.showMessage("No se puede guardar la imagen","Error")
        self.Errores.close()

    
    def Open_Image(self):
        self.ex.openFileNameDialog()
        #Buscar y abrir imagen
        #while True:
        if self.ex.fileName=='':
            self.Errores.showMessage("No se puede abrir la imagen","Error")
        else:
            try:
                
                PIX=QtGui.QPixmap(f'{self.ex.fileName}')
                
                self.Original_Image.setPixmap(PIX)
                self.Original_Image.setAlignment(QtCore.Qt.AlignCenter)
                self.Original_Image.setScaledContents(True)
                self.Original_Image.setMinimumSize(1,1)
                self.Original_Image.show()

                #Leer la imagen para opencv
                self.img = cv2.imread(f'{self.ex.fileName}')
                self.temp = self.img
                self.add_buffer()
                self.imgrgb = self.img
                self.no_negative = self.img
                PIXEL_MAP=Cv_to_QPixmap(self.img)
                self.Processed_Image.setPixmap(PIXEL_MAP)
                #Propiedades
                self.Processed_Image.setScaledContents(True)
                self.Processed_Image.setMinimumSize(1,1)
                self.Processed_Image.show()
            
                self.Errores.close()
            except AttributeError:
                self.Errores.showMessage("No se puede abrir la imagen","Error")

            #Histograma
            self.mostrar_histograma()
            self.Errores.close()

            self.BrilloSlider.setValue(0)
            self.ContrastSlider.setValue(10)
            self.GammSlider.setValue(0)

        """
        pixmap01 = QtGui.QPixmap.fromImage(qImg)
        pixmap_image = QtGui.QPixmap(pixmap01)
        self.Original_Image.setAlignment(QtCore.Qt.AlignCenter)
        self.Original_Image.setScaledContents(True)
        self.Original_Image.setMinimumSize(1,1)
        self.Original_Image.show()
        """

    def Convert2Gray(self):
        
        self.add_buffer()
        try:
            self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        except:
            self.img=self.img
            self.Errores.showMessage("No se puede convertir imagen a escala de grises","Error")

        PIXEL_MAP=Cv_to_QPixmap(self.img)
        self.Processed_Image.setPixmap(PIXEL_MAP)
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()

        #Muestra el histograma
        self.mostrar_histograma()

    def VDegrade(self, state):
        self.add_buffer()
        self.img=Inf_Degrade(self.img)
        PIXEL_MAP=Cv_to_QPixmap(self.img)
        self.Processed_Image.setPixmap(PIXEL_MAP)
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()
        
        #Muestra el histograma
        self.mostrar_histograma()
        
    def HDegrade(self):
        self.add_buffer()
        self.img=R_Degrade(self.img)
        PIXEL_MAP=Cv_to_QPixmap(self.img)
        self.Processed_Image.setPixmap(PIXEL_MAP)
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()
        
        #Muestra el histograma
        self.mostrar_histograma()

    def negative(self):
        self.add_buffer()
        dmax=255
        dmin=0
        self.img = np.uint8(np.clip(-self.img+dmax, dmin, dmax-1))
        PIXEL_MAP=Cv_to_QPixmap(self.img)
        self.Processed_Image.setPixmap(PIXEL_MAP)
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()
        #Muestra el histograma
        self.mostrar_histograma()
        
    def Equalize(self):

        self.add_buffer()
        if len(self.img.shape)==2:
            imgEqualized = cv2.equalizeHist(self.img)
            
        else:
            #Se convierte de BGR a YUV
            imageyuv = cv2.cvtColor(self.img,cv2.COLOR_BGR2YUV)
            #Se aplica la ecualizacion en YUV
            imageyuv[:,:,0] = cv2.equalizeHist(imageyuv[:,:,0])
            #Se transforma a BGR otra vez
            imgEqualized = cv2.cvtColor(imageyuv, cv2.COLOR_YUV2BGR)
            self.imgrgb=imgEqualized
            
        self.img=imgEqualized
        #Muestra el histograma
        self.mostrar_histograma()
    
    def Filter(self):
        self.add_buffer()
        N=None
        if self.comboBoxKernel.currentText()=="5x5":
            N=5
        elif self.comboBoxKernel.currentText()=="10x10":
            N=10
        elif self.comboBoxKernel.currentText()=="20x20":
            N=20

        filtered_img=None

        if self.ComboBoxFiltro.currentText()=="Average":
            filtered_img=average_filter(self.img,N)
        elif self.ComboBoxFiltro.currentText()=="Sobel": 
            try:
                filtered_img=sobel_filter(self.img)
            except:
                self.Errores.showMessage("No se puede aplicar el filtro sobel","Error")
                filtered_img=self.img
        elif self.ComboBoxFiltro.currentText()=="Gaussian":
            filtered_img=gauss_filter(self.img,N,4)
        
        self.img=filtered_img
        self.Processed_Image.setPixmap(Cv_to_QPixmap(self.img))
        #Propiedades
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()

        #Muestra el histograma
        self.mostrar_histograma()

    def Cambiar_Brillo(self):
        self.a=self.ContrastSlider.value()/10
        self.b=self.BrilloSlider.value()
        
        self.temp=np.uint8(np.minimum(255, np.maximum(self.a*self.img+self.b, 0)))
        g=self.GammSlider.value()/10
        self.temp=gamma(self.temp,g)
        #Actualizar imagen
        self.Processed_Image.setPixmap(Cv_to_QPixmap(self.temp))
        #Propiedades
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()

        #Muestra el histograma
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene (scene)
        canvas = histogramer(self.temp)
        scene.addWidget(canvas)

    def Cambiar_Contraste(self):
        self.a=self.ContrastSlider.value()/10
        self.b=self.BrilloSlider.value()
        self.temp=np.uint8(np.minimum(255, np.maximum(self.a*self.img+self.b, 0)))
        g=self.GammSlider.value()/10
        self.temp=gamma(self.temp,g)
        #Actualizar imagen
        self.Processed_Image.setPixmap(Cv_to_QPixmap(self.temp))
        #Propiedades
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()

        #Muestra el histograma
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene (scene)
        canvas = histogramer(self.temp)
        scene.addWidget(canvas)
        
    def mostrar_histograma(self):
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene (scene)
        canvas = histogramer(self.img)
        scene.addWidget(canvas)

    def Cambiar_Gamma(self):
        self.temp=np.uint8(np.clip(self.a*self.img+self.b, 1.0, 254.0))
        g=self.GammSlider.value()/10
        self.temp=gamma(self.temp,g)

        #Actualizar imagen
        self.Processed_Image.setPixmap(Cv_to_QPixmap(self.temp))
        #Propiedades
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()

        #Muestra el histograma
        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene (scene)
        canvas = histogramer(self.temp)
        scene.addWidget(canvas)

    def ApplyChanges(self):
        self.img = self.temp
        self.add_buffer()
        self.GammSlider.setValue(10)
        self.ContrastSlider.setValue(10)
        self.BrilloSlider.setValue(0)
        self.Processed_Image.setPixmap(Cv_to_QPixmap(self.img))
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()
        self.mostrar_histograma()

    def add_buffer(self):
        self.buffer.append(self.img)
        self.buffer = self.buffer[0:self.max_size]

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    GUI = ejemplo()
    GUI.show()
    sys.exit(app.exec_())