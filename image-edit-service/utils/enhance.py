import cv2

def enhance_image(input_path, output_path):
    try:
        print(f"Reading image from {input_path}...")
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Could not read image from {input_path}")
        print(f"Original image shape: {img.shape}")
        # Convert to LAB color space for better contrast enhancement
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        # Apply CLAHE to L-channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        # Optionally apply detail enhancement
        enhanced = cv2.detailEnhance(enhanced, sigma_s=10, sigma_r=0.15)
        cv2.imwrite(output_path, enhanced)
        print(f"Enhanced image saved to {output_path}")
    except Exception as e:
        print(f"Error in enhance_image: {e}")
        raise
