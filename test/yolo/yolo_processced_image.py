# pylint: disable=no-member
import cv2
import numpy as np
import os
from PIL import Image
from glob import glob

# Thư mục ảnh gốc
#IMAGE_DIR = "images/train"
#SAVE_DIR = "data/yolo/images/train"
IMAGE_DIR = "images"
SAVE_DIR = "data/yolo/images/val"

# Tạo thư mục lưu ảnh đã tiền xử lý
os.makedirs(SAVE_DIR, exist_ok=True)

def preprocess_image(image_path):
    """Tiền xử lý ảnh giống với API"""
    image = Image.open(image_path)  # Mở ảnh bằng PIL
    image = np.array(image)  # Chuyển thành numpy array

    # Đảm bảo ảnh có 3 kênh (RGB)
    if image.shape[-1] == 4:  # Nếu ảnh có 4 kênh (RGBA)
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif image.shape[-1] == 1:  # Nếu ảnh là grayscale
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    normalized_image = (image / 255.0) * 255  # Chuẩn hóa giống API (để giữ định dạng uint8)

    return normalized_image.astype(np.uint8)  # Chuyển về kiểu uint8 để lưu

# Lặp qua toàn bộ ảnh và xử lý
image_paths = glob(os.path.join(IMAGE_DIR, "*.jpg"))  # Lấy danh sách ảnh
for img_path in image_paths:
    processed_img = preprocess_image(img_path)
    filename = os.path.basename(img_path)
    cv2.imwrite(os.path.join(SAVE_DIR, filename), processed_img)  # Lưu ảnh đã xử lý
