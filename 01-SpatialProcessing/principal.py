import sys
from browsefile import BrowseFile
from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets, QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
from imageio import imread
import cv2

def Cv_to_QPixmap(image):
    if len(image.shape)==2:
        height, width = image.shape
        qImg = QtGui.QImage( image.data, width, height, width, QtGui.QImage.Format_Grayscale8)
    else: 
        height, width, channel = image.shape
        bytesPerLine = 3*width
        qImg = QtGui.QImage( image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888).rgbSwapped()
    PIX2 = QtGui.QPixmap(qImg)
    return PIX2

class ejemplo(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(r"C:\Users\Eduardo\Documents\universidad\VsionArtificial\Vision_Artificial-master\gui.ui",self)
        #self.label = self.findChild(QtWidgets.QLabel, 'lbl_image_1') #  Busca el boton llamado pushButton
        #self.show()
        self.img = None
        self.imgrgb = None
        self.OpenImageButton.clicked.connect(self.Open_Image)
        self.Gray_Checkbox.stateChanged.connect(self.checkBoxChangedAction)

    def Open_Image(self):
        print('Se presionó el boton pushButton')
        self.ex = BrowseFile()
        
        #Buscar y abrir imagen
        PIX=QtGui.QPixmap(f'{self.ex.fileName}')
        self.Original_Image.setPixmap(PIX)
        self.Original_Image.setAlignment(QtCore.Qt.AlignCenter)
        self.Original_Image.setScaledContents(True)
        self.Original_Image.setMinimumSize(1,1)
        self.Original_Image.show()

        #Leer la imagen para opencv
        self.img = cv2.imread(f'{self.ex.fileName}')
        PIXEL_MAP=Cv_to_QPixmap(self.img)
        self.Processed_Image.setPixmap(PIXEL_MAP)
        self.Processed_Image.setScaledContents(True)
        self.Processed_Image.setMinimumSize(1,1)
        self.Processed_Image.show()

        """
        pixmap01 = QtGui.QPixmap.fromImage(qImg)
        pixmap_image = QtGui.QPixmap(pixmap01)
        self.Original_Image.setAlignment(QtCore.Qt.AlignCenter)
        self.Original_Image.setScaledContents(True)
        self.Original_Image.setMinimumSize(1,1)
        self.Original_Image.show()
        """

    def checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.imgrgb = self.img
            self.img=cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            PIXEL_MAP=Cv_to_QPixmap(self.img)
            self.Processed_Image.setPixmap(PIXEL_MAP)
            self.Processed_Image.setScaledContents(True)
            self.Processed_Image.setMinimumSize(1,1)
            self.Processed_Image.show()
        else:
            self.img = self.imgrgb
            PIXEL_MAP=Cv_to_QPixmap(self.img)
            self.Processed_Image.setPixmap(PIXEL_MAP)
            self.Processed_Image.setScaledContents(True)
            self.Processed_Image.setMinimumSize(1,1)
            self.Processed_Image.show()



    
        



     

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    GUI = ejemplo()
    GUI.show()
    sys.exit(app.exec_())