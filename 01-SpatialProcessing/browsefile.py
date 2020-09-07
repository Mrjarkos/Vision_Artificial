"""import sys
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class BrowseFile(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.fileName = ''
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.fileName = fileName
            print(fileName)
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
"""
import sys
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

class BrowseFile(QWidget):

<<<<<<< HEAD
=======
    
>>>>>>> 43fcc3497b88d486765914f94eb3225d44d48d26
    fileName= ''
    def __init__(self):
        super().__init__()
        self.title = 'File Browser'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
<<<<<<< HEAD
        self.fileName = ''
        self.saveName = ''
=======
>>>>>>> 43fcc3497b88d486765914f94eb3225d44d48d26
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
<<<<<<< HEAD
        #self.openFileNameDialog()
=======
        self.openFileNameDialog()
>>>>>>> 43fcc3497b88d486765914f94eb3225d44d48d26
    
    def openFileNameDialog(self):
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Images (*.png *.xpm *.jpg)")
<<<<<<< HEAD
        if fileName:
            self.fileName = fileName
            return True
        return False
        
=======
        self.fileName = fileName
        

>>>>>>> 43fcc3497b88d486765914f94eb3225d44d48d26
    def returnFileName(self):
        return self.fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
<<<<<<< HEAD
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Images (*.png *.xpm *.jpg)")
        if fileName:
            self.saveName = fileName
            return True
        return False

    def returnSaveName(self):
        return self.saveName
=======
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
>>>>>>> 43fcc3497b88d486765914f94eb3225d44d48d26
