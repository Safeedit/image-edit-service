import cv2
import os

def enhance_image(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    img = cv2.imread(input_path)

    if img is None:
        raise ValueError("Failed to read image. Make sure the file is a valid image format.")

    enhanced = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)

    success = cv2.imwrite(output_path, enhanced)
    if not success:
        raise IOError(f"Failed to save enhanced image to: {output_path}")
