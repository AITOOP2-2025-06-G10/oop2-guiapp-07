# image_utils.py
import numpy as np

def replace_white(overlay_img, camera_img):
    """overlay_img の白を camera_img で置き換える"""
    h, w, _ = overlay_img.shape
    ch, cw, _ = camera_img.shape
    result = overlay_img.copy()

    for y in range(h):
        for x in range(w):
            b, g, r = result[y, x]
            if (b, g, r) == (255, 255, 255):
                result[y, x] = camera_img[y % ch, x % cw]
    return result
