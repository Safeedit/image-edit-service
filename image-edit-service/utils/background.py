from rembg import remove
from PIL import Image

def remove_bg_add_new(input_path, output_path, bg_color=None, bg_image_path=None):
    # Load and convert input to RGBA
    input_img = Image.open(input_path).convert("RGBA")
    
    # Remove background
    no_bg = remove(input_img)

    # Create background based on parameters
    background = None

    if bg_color:
        try:
            # Convert hex (#rrggbb) to RGBA
            if isinstance(bg_color, str) and bg_color.startswith('#') and len(bg_color) == 7:
                bg_color = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) + (255,)
            # Convert comma-separated RGB (e.g., "255,255,255") to RGBA
            elif isinstance(bg_color, str) and ',' in bg_color:
                rgb = tuple(map(int, bg_color.split(',')))
                bg_color = rgb + (255,) if len(rgb) == 3 else rgb
            # If it's already a tuple, ensure it has alpha
            elif isinstance(bg_color, tuple):
                bg_color = bg_color if len(bg_color) == 4 else bg_color + (255,)
            else:
                raise ValueError("Unsupported color format")
            
            background = Image.new("RGBA", no_bg.size, bg_color)
        except Exception as e:
            print(f"[Error] Failed to parse background color '{bg_color}':", e)
            background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))  # Fallback to white

    elif bg_image_path:
        try:
            background = Image.open(bg_image_path).convert("RGBA").resize(no_bg.size)
        except Exception as e:
            print(f"[Error] Failed to load background image '{bg_image_path}':", e)
            background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))  # Fallback

    else:
        background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))  # Default white

    # Composite the no-bg image onto the background
    combined = Image.alpha_composite(background, no_bg.convert("RGBA"))

    # Save as PNG
    combined.save(output_path)
