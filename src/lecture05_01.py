import numpy as np
import cv2
import os
from my_module.K24011.lecture05_camera_image_capture import MyVideoCapture  # ← 学籍番号に合わせる

def lecture05_01():
    
    # カメラキャプチャ実行
    app = MyVideoCapture()
    app.run()

    # 画像をローカル変数に保存
    google_img: cv2.Mat = cv2.imread('images/google.png')
    capture_img: cv2.Mat = app.get_img()  # カメラ画像取得

    # 画像サイズを取得
    g_height, g_width, g_channel = google_img.shape
    c_height, c_width, c_channel = capture_img.shape
    print("Google画像サイズ:", google_img.shape)
    print("カメラ画像サイズ:", capture_img.shape)

    # 白い部分をカメラ画像で置き換える処理
    for y in range(g_height):
        for x in range(g_width):
            b, g, r = google_img[y, x]
            # もし白色(255,255,255)だったら置き換える
            if (b, g, r) == (255, 255, 255):
                google_img[y, x] = capture_img[y % c_height, x % c_width]

    # 書き込み・保存処理
    output_dir = os.path.join(os.getcwd(), "output_images")  # 実行ディレクトリ基準
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "lecture05_01_k24011-07.png")

    cv2.imwrite(output_path, google_img)
    print(f"保存完了！：{output_path}")

