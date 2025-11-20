import cv2
import numpy as np
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer

# -------------------------------
# 白部分を置き換える関数
# -------------------------------
def replace_white(overlay_img, camera_img):
    h, w, _ = overlay_img.shape
    ch, cw, _ = camera_img.shape

    result = overlay_img.copy()

    for y in range(h):
        for x in range(w):
            b, g, r = result[y, x]
            if (b, g, r) == (255, 255, 255):
                result[y, x] = camera_img[y % ch, x % cw]

    return result

# -------------------------------
# GUI 本体
# -------------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("合成アプリ")

        # 状態変数
        self.capture_img = None
        self.camera = None
        self.timer = QTimer()  # プレビュー用タイマー

        # main.py のあるフォルダを基準
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # google.png 読み込み
        overlay_path = os.path.join(BASE_DIR, "google.png")
        self.overlay_img = cv2.imread(overlay_path)
        if self.overlay_img is None:
            raise FileNotFoundError(f"{overlay_path} が見つかりません！")

        # output_images フォルダ指定
        self.output_dir = os.path.join(BASE_DIR, "output_images")
        if not os.path.exists(self.output_dir):
            print("警告: output_images フォルダが存在しません！")

        # GUI 部品
        self.btn_open = QPushButton("① カメラ起動")
        self.btn_cap = QPushButton("② 撮影")
        self.btn_merge = QPushButton("③ 合成")
        self.label = QLabel("ここに画像が表示されます")

        self.btn_cap.setEnabled(False)
        self.btn_merge.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_cap)
        layout.addWidget(self.btn_merge)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # ボタンイベント
        self.btn_open.clicked.connect(self.open_cam)
        self.btn_cap.clicked.connect(self.capture)
        self.btn_merge.clicked.connect(self.merge_img)

        # タイマーイベント
        self.timer.timeout.connect(self.update_frame)

    # ----------------------
    # ① カメラ起動
    # ----------------------
    def open_cam(self):
        self.camera = cv2.VideoCapture(0)
        if self.camera.isOpened():
            print("カメラ起動 OK")
            self.btn_cap.setEnabled(True)
            self.timer.start(30)  # 30ms間隔でプレビュー更新
        else:
            print("カメラが見つかりません")

    # ----------------------
    # タイマーで呼ばれるプレビュー更新
    # ----------------------
    def update_frame(self):
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                self.show_img(frame)

    # ----------------------
    # ② 撮影 + 保存
    # ----------------------
    def capture(self):
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                self.capture_img = frame
                self.show_img(frame)
                self.save_capture(frame)
                print("撮影完了")
                self.btn_merge.setEnabled(True)
                self.timer.stop()  # 撮影後はプレビュー停止

    def save_capture(self, img):
        path = os.path.join(self.output_dir, "captured.png")
        cv2.imwrite(path, img)
        print("撮影画像保存:", path)

    # ----------------------
    # ③ 合成 + 保存
    # ----------------------
    def merge_img(self):
        if self.capture_img is None:
            return

        result = replace_white(self.overlay_img, self.capture_img)
        self.show_img(result)
        self.save_result(result)
        print("合成完了")

    def save_result(self, img):
        path = os.path.join(self.output_dir, "result.png")
        cv2.imwrite(path, img)
        print("合成画像保存:", path)

    # ----------------------
    # GUI 表示
    # ----------------------
    def show_img(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)
        self.label.setPixmap(pix.scaled(400, 400, Qt.KeepAspectRatio))


# -------------------------------
# main
# -------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
