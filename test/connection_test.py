import serial
import time

# 入力変数に対応した通信用電文を返す
def encodeSendData(led_list):
    # 通信電文数値に変換
    send_data_int = 33  # 32以下は制御文字のため
    for i, led_bit in enumerate(led_list):
        send_data_int += led_bit << i

    # ASCIIコードに対応した1文字を返す
    return chr(send_data_int)

if __name__ == '__main__':
    # 通信電文取得
    send_data_str = encodeSendData([0, 0, 0, 1])
    # print(send_data_str)

    while(1):
        ser = serial.Serial('/dev/ttyACM0', timeout=2)

        # データ送信
        ser.write(str.encode(send_data_str))

        line = ser.readline()  # 行終端'¥n'までリードする
        ser.close()

        time.sleep(1)
        print(line.decode('utf-8'))

