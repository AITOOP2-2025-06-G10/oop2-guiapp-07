import cv2
import numpy as np
import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

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
        self.overlay_img = cv2.imread("google.png")  # ← 白部分を置換したい画像
        self.camera = None

        # 既存の output_images フォルダを指定
        self.output_dir = os.path.join(os.getcwd(), "output_images")
        if not os.path.exists(self.output_dir):
            print("警告: output_images フォルダが存在しません！")
        else:
            print(f"保存先フォルダ: {self.output_dir}")

        # GUI部品
        self.btn_open = QPushButton("① カメラ起動")
        self.btn_cap = QPushButton("② 撮影")
        self.btn_merge = QPushButton("③ 合成")
        self.label = QLabel("ここに表示されます")

        self.btn_cap.setEnabled(False)
        self.btn_merge.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_cap)
        layout.addWidget(self.btn_merge)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # イベント接続
        self.btn_open.clicked.connect(self.open_cam)
        self.btn_cap.clicked.connect(self.capture)
        self.btn_merge.clicked.connect(self.merge_img)

    # ----------------------
    # ① カメラ起動
    # ----------------------
    def open_cam(self):
        self.camera = cv2.VideoCapture(0)
        if self.camera.isOpened():
            print("カメラ起動 OK")
            self.btn_cap.setEnabled(True)
        else:
            print("カメラが見つかりません")

    # ----------------------
    # ② 撮影 + 保存
    # ----------------------
    def capture(self):
        ret, frame = self.camera.read()
        if ret:
            self.capture_img = frame
            self.show_img(frame)
            self.save_capture(frame)
            print("撮影完了")
            self.btn_merge.setEnabled(True)

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
    # GUI表示処理
    # ----------------------
    def show_img(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)
        self.label.setPixmap(pix.scaled(400, 400, Qt.KeepAspectRatio))


# -------------------------------
#  main
# -------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
