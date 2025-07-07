from rembg import remove
from PIL import Image
import numpy as np
import cv2

def remove_bg_add_new(input_path, output_path, bg_color=None, bg_image_path=None):
    input_image = Image.open(input_path).convert("RGBA")
    no_bg = remove(input_image)

    if bg_image_path:
        bg = Image.open(bg_image_path).resize(no_bg.size).convert("RGBA")
        final = Image.alpha_composite(bg, no_bg)
    elif bg_color:
        bg = Image.new("RGBA", no_bg.size, bg_color)
        final = Image.alpha_composite(bg, no_bg)
    else:
        final = no_bg

    final.convert("RGBA").save(output_path)
