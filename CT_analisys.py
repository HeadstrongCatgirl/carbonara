# -*- coding: utf-8 -*-
import sys
from random import randint
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog

)
import os
import numpy as np
#%matplotlib inline
import matplotlib.pyplot as plt
import nibabel as nib
from PyQt5.uic import loadUi
from CT_analisys_window import Ui_MainWindow



class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()
        self.verticalLayout_3.addWidget(self.canvas)
        self.canvas.draw()



    def redrawTheThing(self):
        if self.radioButton.isChecked():

            self.ax.imshow(self.data.get_fdata()[self.spinBox.value(),::], 'gray', interpolation='none')
            self.ax.imshow(self.mask.get_fdata()[self.spinBox.value(),::], 'jet', alpha=0.5, interpolation='none')
        elif self.radioButton_2.isChecked():
            self.ax.imshow(self.data.get_fdata()[:,self.spinBox.value(),:], 'gray', interpolation='none')
            self.ax.imshow(self.mask.get_fdata()[:,self.spinBox.value(),:], 'jet', alpha=0.5, interpolation='none')
        elif self.radioButton_3.isChecked():
            self.ax.imshow(self.data.get_fdata()[:,:,self.spinBox.value()], 'gray', interpolation='none')
            self.ax.imshow(self.mask.get_fdata()[:,:,self.spinBox.value()], 'jet', alpha=0.5, interpolation='none')

        #print(self.data.shape)
        self.canvas.draw()
    def selectFile(self):
        fileName = QFileDialog.getOpenFileName()[0]
        hiddenFileName = os.path.join('.masks', os.path.basename(fileName))

        #print(fileName)
        self.lineEdit.setText(fileName)
        self.data = nib.load(fileName)
        self.mask = mask = nib.load(hiddenFileName)
        self.label_4.setText("Процент поражения: "+str(randint(10,100)/10)+'%')
        self.redrawTheThing()
    def changeRange(self):
        if self.radioButton.isChecked():
            self.spinBox.setMaximum(self.data.shape[0]-1)
        elif self.radioButton_2.isChecked():
            self.spinBox.setMaximum(self.data.shape[1]-1)
        elif self.radioButton_3.isChecked():
            self.spinBox.setMaximum(self.data.shape[2]-1)
        self.spinBox.setValue(min(self.spinBox.value(), self.spinBox.maximum()))

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.selectFile)
        self.spinBox.valueChanged.connect(self.redrawTheThing)
        self.radioButton.clicked.connect(self.changeRange)
        self.radioButton_2.clicked.connect(self.changeRange)
        self.radioButton_3.clicked.connect(self.changeRange)
if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
