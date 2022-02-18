import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton,QComboBox,QListView,QLabel,QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from nipper_inspector_ui import Ui_MainWindow
import numpy as np

import matplotlib.pyplot as plt

class NipperInspectorGui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(NipperInspectorGui, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def button_click_LED1(self):
        print("[info] LED1 clicked.")

    def button_click_LED2(self):
        print("[info] LED2 clicked.")

    def button_click_LED3(self):
        print("[info] LED3 clicked.")

    def button_click_LED4(self):
        print("[info] LED4 clicked.")

if __name__ == '__main__':
    argvs = sys.argv
    app = QApplication(argvs)
    nipper_inspector_gui = NipperInspectorGui()
    nipper_inspector_gui.show()
    sys.exit(app.exec_())
