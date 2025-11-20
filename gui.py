# gui.py
import os
import cv2
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer
from gui_methods import open_cam, capture, merge_img

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("合成アプリ")

        # 状態
        self.capture_img = None
        self.camera = None
        self.timer = QTimer()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        overlay_path = os.path.join(BASE_DIR, "google.png")
        import cv2
        self.overlay_img = cv2.imread(overlay_path)
        if self.overlay_img is None:
            raise FileNotFoundError(f"{overlay_path} が見つかりません！")

        self.output_dir = os.path.join(BASE_DIR, "output_images")
        if not os.path.exists(self.output_dir):
            print("警告: output_images フォルダが存在しません！")

        # GUI
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

        # イベント接続（lambdaでselfを渡す）
        self.btn_open.clicked.connect(lambda: open_cam(self))
        self.btn_cap.clicked.connect(lambda: capture(self))
        self.btn_merge.clicked.connect(lambda: merge_img(self))

        # タイマーでプレビュー更新
        self.timer.timeout.connect(self.update_frame)

    def update_frame(self):
        import cv2
        if self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                self.show_img(frame)

    def show_img(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pix = QPixmap.fromImage(qimg)
        self.label.setPixmap(pix.scaled(400, 400, Qt.KeepAspectRatio))
