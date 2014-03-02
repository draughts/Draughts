from PyQt4.QtCore import *
from PyQt4.QtGui import *

import MainApp.conf as config

import nxtWindow
import configWindow
import mainWindowUI as ui
import gui

class mainWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)
        self.thread = gui.Worker()
        self.connect(self.configButton,SIGNAL("clicked()"),self.configButton_click)
        self.connect(self.nxtControlButton, SIGNAL("clicked()"), self.nxtControlButton_click)
        self.connect(self, SIGNAL("text"), self.add_textHandler)
        self.connect(self, SIGNAL("image_update"), self.updateImageHadler)
        self.connect(self.makeMoveButton, SIGNAL("clicked()"), self.new_move)

    def use_thread(self, thr):
        self.thread = thr
        self.connect(self.calibrateCornersButton, SIGNAL("clicked()"), self.thread.calibrate_image)

    def new_move(self):
        #self.add_text("new")
        self.thread.new_move()

    def add_textHandler(self):
        self.movesList.append(self.textToAdd)

    def add_text(self,string):
        self.textToAdd = string
        self.emit(SIGNAL("text"),self.add_textHandler)

    def nxtControlButton_click(self):
        ui = nxtWindow.nxtWindow(self)
        ui.exec_()

    def configButton_click(self):
        ui = configWindow.configWindow(self)
        ui.lineEdit.setText(config.get('IP'))
        ui.spinBox.setValue(int(config.get('threshold')))
        if ui.exec_():
            config.set('IP', ui.lineEdit.text())
            #config.IP = ui.lineEdit.text()
            config.set('threshold', ui.spinBox.value())
            #config.threshold = ui.spinBox.value()

    def updateImage(self):
        self.emit(SIGNAL("image_update"), self.updateImageHadler)

    def updateImageHadler(self):
        myPixmap = QPixmap(QString.fromUtf8('tmp.jpg'))
        scene = QGraphicsScene()
        scene.addPixmap(myPixmap)
        self.image.setScene(scene)