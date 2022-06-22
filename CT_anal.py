# -*- coding: utf-8 -*-
import sys

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
from CT_anal_window import Ui_MainWindow



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
            self.ax.imshow(self.data.get_fdata()[self.spinBox.value(),::])
        elif self.radioButton_2.isChecked():
            self.ax.imshow(self.data.get_fdata()[:,self.spinBox.value(),:])
        elif self.radioButton_3.isChecked():
            self.ax.imshow(self.data.get_fdata()[:,:,self.spinBox.value()])

        #print(self.data.shape)
        self.canvas.draw()
    def selectFile(self):
        fileName = QFileDialog.getOpenFileName()[0]
        #print(fileName)
        self.lineEdit.setText(fileName)
        self.data = nib.load(fileName)
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
