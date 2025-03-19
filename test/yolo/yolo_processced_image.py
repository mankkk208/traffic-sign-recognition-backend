# pylint: disable=no-member
import cv2
import numpy as np
import os
from glob import glob

# Đường dẫn thư mục
IMAGE_DIR = r"C:\Users\Lenovo\Desktop\817\Data\augmented\val\images"
SAVE_DIR = r"C:\Users\Lenovo\Desktop\817\Data\processed\images\val"

# Tạo thư mục lưu ảnh đã tiền xử lý
os.makedirs(SAVE_DIR, exist_ok=True)

def preprocess_image(image_path):
    """Tiền xử lý ảnh: Chuyển RGB -> HSV"""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Đọc ảnh gốc

    # Xử lý ảnh RGBA hoặc grayscale nếu cần
    if image is None:
        print(f"Không thể đọc ảnh: {image_path}")
        return None
    if len(image.shape) == 2:  # Grayscale -> BGR
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[-1] == 4:  # RGBA -> BGR
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Chuyển đổi từ BGR sang HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    return hsv_image

# Lặp qua toàn bộ ảnh và xử lý
image_paths = glob(os.path.join(IMAGE_DIR, "*.jpg"))  # Lấy danh sách ảnh
for img_path in image_paths:
    processed_img = preprocess_image(img_path)
    if processed_img is not None:
        filename = os.path.basename(img_path)
        cv2.imwrite(os.path.join(SAVE_DIR, filename), processed_img)  # Lưu ảnh đã xử lý

print(f"Xử lý hoàn tất! Ảnh HSV được lưu tại {SAVE_DIR}")
