#pylint: disable=no-member
import os
import cv2
import glob
import numpy as np
import albumentations as A

# Thư mục chứa ảnh và nhãn gốc
input_folder = r"C:\Users\Lenovo\Desktop\817\Data\train\images"
label_folder = r"C:\Users\Lenovo\Desktop\817\Data\train\labels"

# Thư mục lưu ảnh và nhãn augment
output_image_folder = r"C:\Users\Lenovo\Desktop\817\Data\augmented\train\images"
output_label_folder = r"C:\Users\Lenovo\Desktop\817\Data\augmented\train\labels"

os.makedirs(output_image_folder, exist_ok=True)
os.makedirs(output_label_folder, exist_ok=True)

# Khai báo danh sách augmentation
transform = A.Compose([
    A.HorizontalFlip(p=0.5),  
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.07, rotate_limit=10, p=0.8),  
    A.MotionBlur(blur_limit=(3, 7), p=0.5),  
    A.Perspective(scale=0.03, p=0.4),  
    A.GaussNoise(var_limit=(10.0, 40.0), p=0.6),  
    A.GaussianBlur(blur_limit=(3, 7), p=0.5),  
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.6),  
    A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=15, val_shift_limit=15, p=0.6),  
    A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.3),
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels'], min_visibility=0.2))

# Hàm đọc bounding box từ file YOLO
def read_yolo_label(label_path):
    boxes = []
    class_labels = []
    with open(label_path, "r") as file:
        for line in file.readlines():
            data = line.strip().split()
            class_id = int(data[0])
            bbox = list(map(float, data[1:]))  # (x_center, y_center, width, height)
            boxes.append(bbox)
            class_labels.append(class_id)
    return boxes, class_labels

# Duyệt qua từng ảnh trong thư mục
for image_path in glob.glob(os.path.join(input_folder, "*.jpg")):
    file_name = os.path.basename(image_path)
    label_path = os.path.join(label_folder, file_name.replace(".jpg", ".txt"))

    if not os.path.exists(label_path):
        continue  # Bỏ qua nếu không có file label

    # Đọc ảnh và nhãn
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    boxes, class_labels = read_yolo_label(label_path)

    # Tạo 10 phiên bản augment cho mỗi ảnh
    for i in range(10):
        augmented = transform(image=image, bboxes=boxes, class_labels=class_labels)
        aug_image = augmented["image"]
        aug_bboxes = augmented["bboxes"]
        aug_labels = augmented["class_labels"]

        # Nếu sau augment mà không còn bounding box hợp lệ -> bỏ qua
        if len(aug_bboxes) == 0:
            continue

        # Lưu ảnh augment
        aug_image_path = os.path.join(output_image_folder, f"aug_{i}_{file_name}")
        cv2.imwrite(aug_image_path, aug_image)

        # Lưu label mới
        aug_label_path = os.path.join(output_label_folder, f"aug_{i}_{file_name.replace('.jpg', '.txt')}")
        with open(aug_label_path, "w") as f:
            for class_id, bbox in zip(aug_labels, aug_bboxes):
                f.write(f"{class_id} {' '.join(map(str, bbox))}\n")

print("✅ Augment dữ liệu Train hoàn tất!")
