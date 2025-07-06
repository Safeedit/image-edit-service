import os
from rembg import remove
from PIL import Image
from io import BytesIO

def remove_bg_add_new(input_path, output_path, bg_color=None, bg_image_path=None):
    # ✅ Set lightweight model to avoid Render memory limit
    os.environ["U2NET_MODEL_NAME"] = "u2netp"

    # Read image as bytes for rembg
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    # Remove background using lightweight model
    output_bytes = remove(input_bytes)

    # Convert output bytes to PIL Image
    no_bg = Image.open(BytesIO(output_bytes)).convert("RGBA")

    # Prepare background
    try:
        if bg_color:
            if isinstance(bg_color, str) and bg_color.startswith('#') and len(bg_color) == 7:
                bg_color = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)
            elif isinstance(bg_color, str) and ',' in bg_color:
                rgb = tuple(map(int, bg_color.split(',')))
                bg_color = rgb + (255,) if len(rgb) == 3 else rgb
            elif isinstance(bg_color, tuple):
                bg_color = bg_color if len(bg_color) == 4 else bg_color + (255,)
            else:
                raise ValueError("Unsupported color format")

            background = Image.new("RGBA", no_bg.size, bg_color)
        elif bg_image_path:
            background = Image.open(bg_image_path).convert("RGBA").resize(no_bg.size)
        else:
            background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
    except Exception as e:
        print(f"[Error] Background setup failed:", e)
        background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))

    # Combine background + transparent image
    result = Image.alpha_composite(background, no_bg)

    # Save final image
    result.save(output_path)
