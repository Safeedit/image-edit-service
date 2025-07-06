from rembg import remove
from PIL import Image

def remove_bg_add_new(input_path, output_path, bg_color=None, bg_image_path=None):
    input_img = Image.open(input_path)
    no_bg = remove(input_img)

    if bg_color:
        background = Image.new("RGBA", no_bg.size, bg_color)
    elif bg_image_path:
        background = Image.open(bg_image_path).resize(no_bg.size)
    else:
        background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))  # Default white

    combined = Image.alpha_composite(background.convert("RGBA"), no_bg.convert("RGBA"))
    combined.save(output_path)
