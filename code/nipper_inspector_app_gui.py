import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton,QComboBox,QListView,QLabel,QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from nipper_inspector_ui import Ui_MainWindow
import numpy as np

import serial
import time

import threading

import matplotlib.pyplot as plt

led_list = [0, 0, 0, 0]

class NipperInspectorGui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(NipperInspectorGui, self).__init__(parent)
        self.setupUi(self)
        led_list = [0, 0, 0, 0]

    @pyqtSlot()
    def button_click_LED1(self):
        led_list[0] = 1
        print("[info] LED1 clicked.")

    def button_click_LED2(self):
        led_list[1] = 1
        print("[info] LED2 clicked.")

    def button_click_LED3(self):
        led_list[2] = 1
        print("[info] LED3 clicked.")

    def button_click_LED4(self):
        led_list[3] = 1
        print("[info] LED4 clicked.")


# 入力変数に対応した通信用電文を返す
def encodeSendData(led_list):
    # 通信電文数値に変換
    send_data_int = 33  # 32以下は制御文字のため
    for i, led_bit in enumerate(led_list):
        send_data_int += led_bit << i

    # ASCIIコードに対応した1文字を返す
    return chr(send_data_int)


def communiacateMbed():
    while(1):
        ser = serial.Serial('/dev/ttyACM0', timeout=2)

        # データ送信
        send_data_str = encodeSendData(led_list)
        ser.write(str.encode(send_data_str))

        line = ser.readline()  # 行終端'¥n'までリードする
        ser.close()

        time.sleep(0.1)
        print(led_list)
        print(line.decode('utf-8'))



if __name__ == '__main__':
    argvs = sys.argv
    app = QApplication(argvs)

    thread_communicate = threading.Thread(target=communiacateMbed)
    thread_communicate.start()

    nipper_inspector_gui = NipperInspectorGui()
    nipper_inspector_gui.show()
    sys.exit(app.exec_())
