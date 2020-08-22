from PyQt5 import QtWidgets, uic
from browsefile import BrowseFile
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('test.ui', self)
        self.show()


        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton') #  Busca el boton llamado pushButton
        self.lbl = self.findChild(QtWidgets.QLabel, 'label') #  Busca la etiqueta de Texto
        self.button.clicked.connect(self.botonpresionado) # así es como se crea un evento, uno le pasa el nombre de la función

        self.show()

    def botonpresionado(self):
        print('Se presionó el boton pushButton')
        app = QtWidgets.QDialog()
        ex = BrowseFile()
        self.lbl.setText("Hola Mundo")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()