# pylint: disable=no-member
import os
import cv2
import numpy as np
import albumentations as A
from PIL import Image

# Thư mục chứa ảnh gốc và nơi lưu ảnh augmented
#input_folder = "data/gemini/images"
input_folder = r"C:\Users\Lenovo\Desktop\Test\300\DiThang"
output_folder = r"C:\Users\Lenovo\Desktop\Test\300\augmented\DiThang"
os.makedirs(output_folder, exist_ok=True)

# Định nghĩa các phép biến đổi
transform = A.Compose([
    #A.HorizontalFlip(p=0.5),  # Lật ngang với xác suất 50%
    A.VerticalFlip(p=0.5),  # Lật dọc với xác suất 50%
    A.Rotate(limit=15, p=0.5),  # Xoay ±15 độ
    A.RandomBrightnessContrast(p=0.5),  # Điều chỉnh độ sáng & tương phản
    A.GaussNoise(p=0.3),  # Thêm nhiễu Gaussian
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=15, p=0.5),  # Dịch, scale, xoay
])

# Lặp qua tất cả ảnh
image_files = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".jpeg"))]

for idx, filename in enumerate(image_files):
    img_path = os.path.join(input_folder, filename)
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Đổi sang RGB

    for i in range(5):  # Tạo 5 ảnh augmented cho mỗi ảnh gốc
        augmented = transform(image=image)["image"]
        augmented = Image.fromarray(augmented)
        new_filename = f"{filename.split('.')[0]}_aug{i}.jpg"
        augmented.save(os.path.join(output_folder, new_filename))

    print(f"✅ Augmented: {filename} -> {5} ảnh mới")

print("\n🎉 Hoàn tất Data Augmentation!")
