
import cv2
import os
import numpy as np

def merge_img(self):
        if self.capture_img is None:
            return

        result = replace_white(self.overlay_img, self.capture_img)
        self.show_img(result)
        self.save_result(result)
        print("合成完了")

        return result

def save_result(self, img):
    path = os.path.join(self.output_dir, "result.png")
    cv2.imwrite(path, img)
    print("合成画像保存:", path)

    return result, path