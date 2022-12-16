import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
import glob
import serial
import time
import cv2

class detector:
    def __init__(self) -> None:
        pass
    

    def getHeatmap(self, img):
        heatmap_hsv = np.zeros((img.shape[0], img.shape[1], 3))
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                heatmap_hsv[x][y][0] = 170-(img[x][y]/255* 170)
                heatmap_hsv[x][y][1] = 255
                heatmap_hsv[x][y][2] = 255
        heatmap_hsv = heatmap_hsv.astype(np.uint8)
        # print(heatmap_hsv.shape)
        heatmap = cv2.cvtColor(heatmap_hsv, cv2.COLOR_HSV2BGR_FULL)
        return heatmap


    def calDiff(self, img, img_mask=None):
        # 平均値の算出
        px_sum = []
        img_t = img.transpose(2, 0, 1)
        px_sum.append(np.sum(img_t[0]))
        px_sum.append(np.sum(img_t[1]))
        px_sum.append(np.sum(img_t[2]))
        px_sum = np.array(px_sum)
        
        if img_mask == None:
            px_num = int(img.shape[0]*img.shape[1])  # マスクされてない画素の数
        else:
            px_num = int(np.count_nonzero(img_mask)/3)  # マスクされてない画素の数
        px_mean = px_sum/px_num
        # print(px_mean)

        # 平均値からのズレ行列の算出
        img_diff = np.zeros_like(img_t)
        for i in range(3):
            img_diff[i] = np.abs(img_t[i] - px_mean[i])
        img_diff = img_diff.transpose(1, 2, 0)

        if img_mask != None:
            img_diff = cv2.bitwise_and(img_diff, img_mask)

        return img_diff

    def fuseImg(self, img_inputs, w):
        # 重みがfloatの場合もあるのでfloatにして行列を定義
        img_fused = np.zeros(img_inputs[0].shape).astype(np.float32)
        img_inputs_float = img_inputs.astype(np.float32)

        # 枚数分ループ回して重み付和算
        for i in range(len(img_inputs_float)):
            img_fused += w[i] * img_inputs_float[i]

        # ガード処理
        # for i in range(img_fused.shape[0]):
        #     for j in range(img_fused.shape[1]):
        #         for k in range(img_fused.shape[2]):
        #             if img_fused[i][j][k] > 255:
        #                 img_fused[i][j][k] = 255

        # uint8に戻す
        img_fused = img_fused.astype(np.uint8)
        return img_fused

    def detect(self, imgs):
        # img = cv2.imread("./../test_assets/test.png")
        img = imgs[0]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(img.shape)

        # 検出範囲を表す配列[xs, xe, ys, ye]
        dr = np.array([680, 1340, 240, 850])

        img_range = cv2.rectangle(img,(dr[0], dr[2]), (dr[1], dr[3]),(0,255,0),3)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow('image',img_range)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 検出範囲のみトリミング
        img_trimed = img_gray[dr[2]:dr[3], dr[0]:dr[1]]

        ret2, img_otsu = cv2.threshold(img_trimed, 0, 255, cv2.THRESH_OTSU)
        kernel = np.ones((3,3),np.uint8)
        closing = cv2.morphologyEx(img_otsu, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        print(opening)
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(opening)

        nipper_label_idx = np.argmax(stats.T[cv2.CC_STAT_AREA])

        img_mask = np.zeros(labels.shape, dtype="uint8")
        for r in range(labels.shape[0]):
            for c in range(labels.shape[1]):
                if labels[r][c] != nipper_label_idx:
                    continue
                img_mask[r][c] = 255

        kernel = np.ones((8,8),np.uint8)
        img_mask = cv2.erode(img_mask, kernel,iterations = 1)
        img_mask = np.array([img_mask, img_mask, img_mask], dtype='uint8')
        img_mask = np.transpose(img_mask, (1, 2, 0))
        print(img_mask.shape)

        #     print(f"label {i}")
        #     print(f"* topleft: ({row[cv2.CC_STAT_LEFT]}, {row[cv2.CC_STAT_TOP]})")
        #     print(f"* size: ({row[cv2.CC_STAT_WIDTH]}, {row[cv2.CC_STAT_HEIGHT]})")
        #     print(f"* area: {row[cv2.CC_STAT_AREA]}")

        seg_size = 10
        scan_width = seg_size // 5
        anomaly_check_size = 1
        print('=== 検出条件 ===')
        print(f'セグメントサイズ：{seg_size}')
        print(f'走査幅：{scan_width}')
        print(f'傷レベル検索範囲：{anomaly_check_size}')
        print('================')

        # セグメントマップの作成
        seg_map = []
        for r in range(img_trimed.shape[0]//scan_width):
            tmp_seg_vec = []
            for c in range(img_trimed.shape[1]//scan_width):
                # 走査範囲の設定
                rs, cs = r * scan_width, c * scan_width
                re, ce = rs + seg_size, cs + seg_size

                # 境界処理
                if re > img_trimed.shape[0]: re = img_trimed.shape[0]-1
                if ce > img_trimed.shape[1]: ce = img_trimed.shape[1]-1

                # セグメント値の計算とリストへの追加
                seg = np.average(img_trimed[rs:re, cs:ce])
                tmp_seg_vec.append(seg)
            seg_map.append(tmp_seg_vec)
        seg_map = np.array(seg_map)
        print(seg_map.shape)


        # 傷レベルの計算
        anomaly_map = []
        anomaly_level_map = []
        for r in range(seg_map.shape[0]):
            tmp_anomaly_vec = []
            tmp_anomaly_level_vec = []
            for c in range(seg_map.shape[1]):
                # 走査範囲の設定
                rs, cs = r - anomaly_check_size, c - anomaly_check_size
                re, ce = r + anomaly_check_size, c + anomaly_check_size
                
                # 境界処理
                if rs < 0: rs = 0
                if cs < 0: cs = 0
                if re > seg_map.shape[0]: re = seg_map.shape[0]-1
                if ce > seg_map.shape[1]: ce = seg_map.shape[1]-1

                sub_seg = seg_map[rs:re, cs:ce]
                anomaly = sub_seg.max() - sub_seg.min()

                anomaly_level = [0, 0, 0]
                if anomaly > 15:
                    anomaly_level = [0, 0, 255]
                elif anomaly > 10:
                    anomaly_level = [0, 255, 255]
                
                tmp_anomaly_vec.append(anomaly)
                tmp_anomaly_level_vec.append(anomaly_level)
            anomaly_map.append(tmp_anomaly_vec)
            anomaly_level_map.append(tmp_anomaly_level_vec)
        anomaly_map = np.array(anomaly_map, dtype="uint8")
        anomaly_level_map = np.array(anomaly_level_map, dtype="uint8")


        anomaly_level_map = cv2.resize(anomaly_level_map, (anomaly_level_map.shape[1]*scan_width, anomaly_level_map.shape[0]*scan_width), interpolation = cv2.INTER_NEAREST) 
        # anomaly_level_map = cv2.bitwise_and(anomaly_level_map, img_mask)

        anomaly_level_map_paddinged = np.zeros(img.shape, dtype="uint8")
        for r in range(anomaly_level_map.shape[0]):
            for c in range(anomaly_level_map.shape[1]):
                anomaly_level_map_paddinged[r+dr[2]+1][c+dr[0]+1] = anomaly_level_map[r][c]

        print(anomaly_level_map_paddinged.shape)
        img_trimed
        img_overlayed = self.fuseImg(np.array([img, anomaly_level_map_paddinged]), np.array([0.5, 0.5]))

        # calDiff(img[dr[2]:dr[3], dr[0]:dr[1], :], img_mask)

        # 表示

        # 差分計算
        img_diff = self.calDiff(img[dr[2]:dr[3], dr[0]:dr[1], :])
        print(img_diff.shape)

        # グレースケール化
        img_diff_gray = cv2.cvtColor(img_diff, cv2.COLOR_BGR2GRAY)

        # ヒストグラム均等化
        img_diff_gray = cv2.equalizeHist(anomaly_map)

        heatnap = self.getHeatmap(img_diff_gray)

        plt.imshow(np.asarray(cv2.cvtColor(heatnap, cv2.COLOR_BGR2RGB)))
        plt.show()


