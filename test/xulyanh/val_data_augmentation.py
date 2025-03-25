#pylint: disable=no-member
import os
import cv2
import glob
import numpy as np
import albumentations as A

# Thư mục chứa ảnh và nhãn validation gốc
val_input_folder = r"C:\Users\Lenovo\Desktop\817\Data\val\images"
val_label_folder = r"C:\Users\Lenovo\Desktop\817\Data\val\labels"

# Thư mục lưu ảnh và nhãn augment
output_val_image_folder = r"C:\Users\Lenovo\Desktop\817\Data\augmented\val\images"
output_val_label_folder = r"C:\Users\Lenovo\Desktop\817\Data\augmented\val\labels"

os.makedirs(output_val_image_folder, exist_ok=True)
os.makedirs(output_val_label_folder, exist_ok=True)

# Khai báo augmentation nhẹ
val_transform = A.Compose([
    A.GaussianBlur(blur_limit=(3, 5), p=0.3),
    A.GaussNoise(var_limit=(5.0, 15.0), p=0.2),
    A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.1, p=0.3),
    A.HueSaturationValue(hue_shift_limit=5, sat_shift_limit=10, val_shift_limit=10, p=0.3)
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

# Duyệt qua từng ảnh trong thư mục validation
for image_path in glob.glob(os.path.join(val_input_folder, "*.jpg")):
    file_name = os.path.basename(image_path)
    label_path = os.path.join(val_label_folder, file_name.replace(".jpg", ".txt"))

    if not os.path.exists(label_path):
        continue  # Bỏ qua nếu không có file label

    # Copy ảnh gốc vào thư mục mới
    original_image_path = os.path.join(output_val_image_folder, file_name)
    original_label_path = os.path.join(output_val_label_folder, file_name.replace(".jpg", ".txt"))
    
    cv2.imwrite(original_image_path, cv2.imread(image_path))
    os.system(f'copy "{label_path}" "{original_label_path}"')  # Copy nhãn

    # Đọc ảnh và nhãn
    image = cv2.imread(image_path)
    boxes, class_labels = read_yolo_label(label_path)

    # Tạo 2 phiên bản augment cho mỗi ảnh val
    for i in range(2):
        augmented = val_transform(image=image, bboxes=boxes, class_labels=class_labels)
        aug_image = augmented["image"]
        aug_bboxes = augmented["bboxes"]
        aug_labels = augmented["class_labels"]

        # Nếu sau augment mà không còn bounding box hợp lệ -> bỏ qua
        if len(aug_bboxes) == 0:
            continue

        # Lưu ảnh augment
        aug_image_path = os.path.join(output_val_image_folder, f"val_aug_{i}_{file_name}")
        cv2.imwrite(aug_image_path, aug_image)

        # Lưu label mới
        aug_label_path = os.path.join(output_val_label_folder, f"val_aug_{i}_{file_name.replace('.jpg', '.txt')}")
        with open(aug_label_path, "w") as f:
            for class_id, bbox in zip(aug_labels, aug_bboxes):
                f.write(f"{class_id} {' '.join(map(str, bbox))}\n")

print("✅ Augment dữ liệu validation hoàn tất!")
