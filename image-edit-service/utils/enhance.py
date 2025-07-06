import cv2

def enhance_image(input_path, output_path):
    img = cv2.imread(input_path)
    enhanced = cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)
    cv2.imwrite(output_path, enhanced)
