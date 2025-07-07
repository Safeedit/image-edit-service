from rembg import remove, new_session
from PIL import Image

def remove_bg_add_new(input_path, output_path, bg_color=None, bg_image_path=None):
    try:
        print("Opening input image...")
        input_img = Image.open(input_path).convert("RGBA")
        print(f"Input image size: {input_img.size}")
        # Resize if too large (e.g., max 512x512)
        max_size = (512, 512)
        if input_img.width > 512 or input_img.height > 512:
            input_img.thumbnail(max_size, Image.Resampling.LANCZOS)
            print(f"Resized image to: {input_img.size}")
        print("Creating rembg session...")
        session = new_session("u2netp")
        print("Calling rembg.remove...")
        no_bg_img = remove(input_img, session=session)
        print("rembg.remove finished.")
        if isinstance(no_bg_img, bytes):
            from io import BytesIO
            no_bg = Image.open(BytesIO(no_bg_img)).convert("RGBA")
        elif isinstance(no_bg_img, Image.Image):
            no_bg = no_bg_img.convert("RGBA")
        else:
            raise ValueError("Unexpected output from rembg.remove")

        if bg_color:
            background = Image.new("RGBA", no_bg.size, bg_color)
        elif bg_image_path:
            bg_img = Image.open(bg_image_path).convert("RGBA")
            background = bg_img.resize(no_bg.size)
        else:
            background = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))  # Default white

        combined = Image.alpha_composite(background, no_bg)
        combined.save(output_path)
        print(f"Saved output to {output_path}")
    except Exception as e:
        print(f"Error in remove_bg_add_new: {e}")
        raise
