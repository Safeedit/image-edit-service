import cv2
import os

def enhance_image(input_path, output_path, max_dim=2048):
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Read the image
    img = cv2.imread(input_path)

    if img is None:
        raise ValueError("Failed to read image. Make sure the file is a valid image format.")

    # ✅ Optional: Resize large images to avoid memory overload
    height, width = img.shape[:2]
    if max(height, width) > max_dim:
        scale = max_dim / max(height, width)
        img = cv2.resize(img, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)

    # Apply enhancement
    enhanced = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)

    # Save enhanced image
    success = cv2.imwrite(output_path, enhanced)
    if not success:
        raise IOError(f"Failed to save enhanced image to: {output_path}")
