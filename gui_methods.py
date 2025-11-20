# gui_methods.py
import cv2
from image_utils import replace_white
import os

def open_cam(gui_obj):
    """カメラ起動＋プレビュー開始"""
    gui_obj.camera = cv2.VideoCapture(0)
    if gui_obj.camera.isOpened():
        print("カメラ起動 OK")
        gui_obj.btn_cap.setEnabled(True)
        gui_obj.timer.start(30)
    else:
        print("カメラが見つかりません")

def capture(gui_obj):
    """カメラ撮影＋保存＋プレビュー停止"""
    if gui_obj.camera and gui_obj.camera.isOpened():
        ret, frame = gui_obj.camera.read()
        if ret:
            gui_obj.capture_img = frame
            gui_obj.show_img(frame)
            save_path = os.path.join(gui_obj.output_dir, "captured.png")
            cv2.imwrite(save_path, frame)
            print("撮影画像保存:", save_path)
            gui_obj.btn_merge.setEnabled(True)
            gui_obj.timer.stop()

def merge_img(gui_obj):
    """白部分置換して合成画像を表示＆保存"""
    if gui_obj.capture_img is None or gui_obj.overlay_img is None:
        return
    result = replace_white(gui_obj.overlay_img, gui_obj.capture_img)
    gui_obj.show_img(result)
    save_path = os.path.join(gui_obj.output_dir, "result.png")
    cv2.imwrite(save_path, result)
    print("合成画像保存:", save_path)
  