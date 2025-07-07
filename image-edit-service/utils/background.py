import os
from rembg import remove
from PIL import Image

# ✅ Use lightweight model
os.environ["U2NET_MODEL_NAME"] = "u2netp"

def remove_bg_add_new(input_path, output_path, bg_color=None, bg_image_path=None):
    input_img = Image.open(input_path).convert("RGBA")
    no_bg = remove(input_img)

    # Prepare background
    if bg_color:
        try:
            if isinstance(bg_color, str) and bg_color.startswith('#'):
                bg_color = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)
            elif isinstance(bg_color, str) and ',' in bg_color:
                rgb = tuple(map(int, bg_color.split(',')))
                bg_color = rgb + (255,) if len(rgb) == 3 else rgb
            elif isinstance(bg_color, tuple):
                bg_color = bg_color if len(bg_color) == 4 else bg_color + (255,)
            else:
                raise ValueError("Unsupported color format")

            background = Image.new("RGBA", no_bg.size, bg_color)
        except Exception as e:
            print(f"[Error] Invalid bg_color '{bg_color}':", e)
            background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
    elif bg_image_path:
        try:
            background = Image.open(bg_image_path).convert("RGBA").resize(no_bg.size)
        except Exception as e:
            print(f"[Error] Failed bg_image '{bg_image_path}':", e)
            background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
    else:
        background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))

    combined = Image.alpha_composite(background, no_bg.convert("RGBA"))
    combined.save(output_path)
