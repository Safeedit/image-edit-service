from rembg import remove
from PIL import Image

def remove_bg_add_new(input_path, output_path, bg_color=None, bg_image_path=None):
    input_img = Image.open(input_path).convert("RGBA")  # Ensure RGBA for transparency
    no_bg = remove(input_img)

    if bg_color:
        # Ensure valid hex or RGB input
        if isinstance(bg_color, str) and bg_color.startswith('#'):
            bg_color = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)  # convert #RRGGBB to (R, G, B, A)
        elif isinstance(bg_color, str) and ',' in bg_color:
            bg_color = tuple(map(int, bg_color.split(','))) + (255,)
        elif isinstance(bg_color, tuple):
            bg_color = bg_color + (255,)  # if tuple and no alpha, add alpha
        background = Image.new("RGBA", no_bg.size, bg_color)
    
    elif bg_image_path:
        background = Image.open(bg_image_path).convert("RGBA").resize(no_bg.size)
    
    else:
        background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))  # Default white

    combined = Image.alpha_composite(background, no_bg.convert("RGBA"))
    combined.save(output_path)
