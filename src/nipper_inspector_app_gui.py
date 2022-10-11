import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton,QComboBox,QListView,QLabel,QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from nipper_inspector_ui import Ui_MainWindow
import numpy as np

import datetime
import glob
import serial
import time
import cv2

import threading

import matplotlib.pyplot as plt

led_list = [0, 0, 0, 0, 0, 0, 0, 0]
frame = None

class NipperInspectorGui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(NipperInspectorGui, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def button_click_LED1(self):
        if led_list[0] == 0:
            led_list[0] = 1
        else:
            led_list[0] = 0
        print("[info] LED1 clicked.")

    def button_click_LED2(self):
        if led_list[1] == 0:
            led_list[1] = 1
        else:
            led_list[1] = 0
        print("[info] LED2 clicked.")

    def button_click_LED3(self):
        if led_list[2] == 0:
            led_list[2] = 1
        else:
            led_list[2] = 0
        print("[info] LED3 clicked.")

    def button_click_LED4(self):
        if led_list[3] == 0:
            led_list[3] = 1
        else:
            led_list[3] = 0
        print("[info] LED4 clicked.")

    def button_click_LED5(self):
        if led_list[4] == 0:
            led_list[4] = 1
        else:
            led_list[4] = 0
        print("[info] LED5 clicked.")

    def button_click_LED6(self):
        if led_list[5] == 0:
            led_list[5] = 1
        else:
            led_list[5] = 0
        print("[info] LED6 clicked.")

    def button_click_LED7(self):
        if led_list[6] == 0:
            led_list[6] = 1
        else:
            led_list[6] = 0
        print("[info] LED7 clicked.")

    def button_click_LED8(self):
        if led_list[7] == 0:
            led_list[7] = 1
        else:
            led_list[7] = 0
        print("[info] LED8 clicked.")

    def button_click_FlowCapture(self):
        global led_list
        project_folder_path = os.path.dirname(os.path.abspath(__file__))
        save_folder_path = os.path.join(project_folder_path, "img", datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

        # led_list = [0, 0, 0, 0]
        # time.sleep(3)
        # led_list = [0, 0, 0, 1]
        # time.sleep(3)
        # led_list = [0, 0, 1, 0]
        # time.sleep(3)
        # led_list = [0, 1, 0, 0]
        # time.sleep(3)
        # led_list = [1, 0, 0, 0]
        # time.sleep(2)
        for i in range(2**len(led_list)):
            for j in range(len(led_list)):
                led_list[j] = (i >> j) & 1
            time.sleep(5)
            # saveImg(frame, save_folder_path)

        led_list = [0, 0, 0, 0, 0, 0, 0, 0]

# 入力変数に対応した通信用電文を返す
def getSendData(led_list):
    print(led_list)

    # 通信電文数値に変換
    send_num_int = 0
    for i, led_bit in enumerate(led_list):
        send_num_int += led_bit << i

    return send_num_int


def communiacateMbed():
    while(1):
        ser = serial.Serial('COM6', timeout=2)

        send_num = getSendData(led_list)
        send_byte = send_num.to_bytes(1, 'little')

        print("---")
        print(send_byte)
        print(send_byte.hex())
        print("---")

        ser.write(send_byte)

        line = ser.readline()  # 行終端'¥n'までリードする
        ser.close()

        # time.sleep(0.01)
        # print(led_list)
        # print(line.decode('utf-8'))


def saveImg(frame, save_folder_path):
    os.makedirs(save_folder_path, exist_ok=True)
    file_num = len(glob.glob(os.path.join(save_folder_path, '*')))
    save_filename = "{:0>4}.png".format(file_num)

    cv2.imwrite(os.path.join(save_folder_path, save_filename),frame)

def camera():
    print("a")
#     # VideoCaptureのインスタンスを作成する。
#     # 引数でカメラを選べれる。
#     cap = cv2.VideoCapture(0)

#     # 画像の保存先フォルダ名の生成
#     project_folder_path = os.path.dirname(os.path.abspath(__file__))
#     save_folder_path = os.path.join(project_folder_path, "img", datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

#     while True:
#         # VideoCaptureから1フレーム読み込む
#         global frame
#         ret, frame = cap.read()

#         # スクリーンショットを撮りたい関係で1/4サイズに縮小
#         frame = cv2.resize(frame, (int(frame.shape[1]/1), int(frame.shape[0]/1)))
#         # 加工なし画像を表示する
#         cv2.imshow('Raw Frame', frame)

#         # キー入力を1ms待って、k が27（ESC）だったらBreakする
#         k = cv2.waitKey(1)
#         if k == 115:
#             saveImg(frame, save_folder_path)
#         if k == 27:
#             break

#     # キャプチャをリリースして、ウィンドウをすべて閉じる
#     cap.release()
#     cv2.destroyAllWindows()


if __name__ == '__main__':
    argvs = sys.argv
    app = QApplication(argvs)

    thread_communicate = threading.Thread(target=communiacateMbed)
    thread_communicate.start()

    thread_camera = threading.Thread(target=camera)
    thread_camera.start()

    nipper_inspector_gui = NipperInspectorGui()
    nipper_inspector_gui.show()
    sys.exit(app.exec_())
