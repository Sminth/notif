""" auteur : sminth malan
    mail : emmanuelmalan225@gmail.com
    contact : 88364403
    nom du programme : notif.py
    : Ce programme a pour but d'afficher des messages biblique inspirante aleatoires chaque 30 minutes
      avec un system de tray icon pour stoper le programme """

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from spui import *
from PyQt5.QtGui import QPixmap, QImage
import base64,random,cita,time
from PyQt5.QtWidgets import QWidget
import sys
import threading
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

class syncWorker(QObject):
    """class en parallele avec le programme principal
       chaque 30 minute elle communique au programme principale le message
       a afficher grace au pyqtSignal
    """
    setMess = pyqtSignal(str)
    def __init__(self):
       super().__init__()
 
    @pyqtSlot()
    def loop(self):
       while True:
           time.sleep(1800)
           self.setMess.emit(random.choice(cita.croyons))
           
class MainWindow(QWidget):

    #Le programme commence ICI
    def __init__(self):
        
        super(MainWindow, self).__init__()
        MainWindow.setWindowIcon(self,QtGui.QIcon('Bible.png'))
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.im.setPixmap(QPixmap(QImage.fromData(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACmElEQVRYR8VXTW7TUBD+xjYSXZFukOIsSE9AskNJJMoJmq4r7OYEwAkabhBOkB/Emt4gVIojdpgbpIumEitX6gKB7UHPkauXxLHfc4F6Z3l+vvnmm/fGhAd+6IHzQwvA9cfOITMfAdQAcx1EdVEAM/tEFADsWyaPn57MfdXClABcT1qnzHSWJiwMzrwgoF91vXGRbS6AH59ajd8hDYmoURQo67tgxoij42rv62KX/04Agu44xmciVMokT32YERgGjquvZ1+y4mQCWPUa0/sk3vQlwqssEFsAVrQbU4XKL/ai2+5PPK6waQ4AOsoDnDARh83NdmwBuJq0fQI9L6p+L7rd3+/5gbAToMPI+FbkIzRRc72mbLcGIFE7jGFRIPHddmZrvstJh1X8CHGv6sxHqe1GkPYCoGcqgcoCAPPCdr2DLQC6wqMoPEj7qdqCNKllxs30sLpjYDluDUDGG5XqhY2sal3w4PiD7c7fJnHShMtJR8zpy/8CALiwndnhBgD1/t+XAXkaZAaUVHwnHulg0W6BNEWlAQD8zna8gQB0Ne70iXCm2j55jCUAei1gxvuaO+uXAcDg7zXHSy640iKUAehOEDJFqDmGQkiPLO5Fv+KADXOqvCuIsrPGsIyQdHou22YeRMJgOdHTQTkAfGk7XrLKrWlAvOhcRgBfWiZ3RQti0zxXuUFXCXMuo0TRitfxugjbIxC5RYzI6s9kIGFh+KLOpiW22id5AUuI8IaisFG4kCQg/sFKJgtPLix3KWXGeRETRbQDuCFCV2spTYMm+2FEI1WBbYIRPTeiqFtqLZeDraaD+qrbkpgQAvfl1WsXU0p/RjIjYYhTkNFgcCVlRlRKoAAc+5aF0V//NVPoc2kTLQZKZ8lx/AMXBmMwuXUwOAAAAABJRU5ErkJggg=='))))
        
        self.ui.text.setText(random.choice(cita.croyons))
        #self.ui.text.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        MainWindow.setGeometry(self,-15, 530, 473, 267)
        MainWindow.setWindowFlags(self,
                             QtCore.Qt.WindowStaysOnTopHint
                             | QtCore.Qt.FramelessWindowHint
                             | QtCore.Qt.Tool)
        MainWindow.setAttribute(self,QtCore.Qt.WA_TranslucentBackground)
        self.ui.close.clicked.connect(lambda : ui.close())
        
        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("appli notif : marcher la tête haute")
        self.tray_icon.setIcon(QtGui.QIcon('Bible.png'))#self.style().standardIcon(QStyle.SP_ComputerIcon))
        '''
            menu contextuel du tray icon
            show - show window
            hide - hide window
            exit - quitter l'application
        '''
        show_action = QAction("Afficher", self)
        quit_action = QAction("Quitter", self)
        hide_action = QAction("Fermer", self)
        show_action.triggered.connect(lambda : self.afficheNotif(random.choice(cita.croyons)))
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        #self.tray_icon.setToolTip("icon de l'appli notif")
        
        #utilisation de threading pour recevoir un signal(le message apres le temps ecoule) provenant de la class syncWorker
        self.worker = syncWorker()
        self.workerThread = QThread() #deplace le Worker object au Thread object
        self.workerThread.started.connect(self.worker.loop) #init worker loop
        self.worker.moveToThread(self.workerThread)
        self.worker.setMess.connect(self.afficheNotif)
        self.workerThread.start()
        self.tray_icon.show()

    #fonction qui affiche le message
    def afficheNotif(self,mess):
        #if self.isVisible
        self.ui.text.setText(mess)
        self.show()
        
    def closeEvent(self,event):
        self.hide()
        self.tray_icon.showMessage(
                "notif",
                "l'application s'execute en arriere plan dans un tray",
                QSystemTrayIcon.Information,
                2000
            )
        
        #sys.exit(app.exec_())
##    def mousePressEvent(self, event):
##        super(MainWindow, self).mousePressEvent(event)
##        w = self.childAt(event.pos())
##        print(w)
##        if not w:
##            return
##        if w == self.ui.close:  print("la")
##        elif w == self.ui.text: #and self.callback and callable(self.callback):


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('Bible.png'))
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
