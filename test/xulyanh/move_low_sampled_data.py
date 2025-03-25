import os
import shutil
from collections import defaultdict

def move_low_sample_files(labels_dir, images_dir, class_file, dest_dir, threshold=200):
    # Đọc danh sách class từ file classes.txt
    with open(class_file, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f.readlines()]
    
    class_counter = defaultdict(int)  # Đếm số lần mỗi class xuất hiện
    file_class_map = defaultdict(set)  # Map file -> các class trong file

    # Đếm số lượng biển báo trong dataset
    for label_file in os.listdir(labels_dir):
        if label_file.endswith(".txt"):
            label_path = os.path.join(labels_dir, label_file)
            with open(label_path, "r", encoding="utf-8") as f:
                for line in f:
                    class_id = int(line.split()[0])  # Lấy ID của class
                    if class_id < len(classes):  # Kiểm tra ID hợp lệ
                        class_counter[class_id] += 1
                        file_class_map[label_file].add(class_id)  # Gán class_id cho file này

    # Xác định class nào có ít hơn threshold ảnh
    low_sample_classes = {class_id for class_id, count in class_counter.items() if count < threshold}

    # Tạo thư mục đích nếu chưa tồn tại
    os.makedirs(os.path.join(dest_dir, "labels"), exist_ok=True)
    os.makedirs(os.path.join(dest_dir, "images"), exist_ok=True)

    # Duyệt qua từng file label để kiểm tra có nên di chuyển không
    for label_file, class_ids in file_class_map.items():
        # Nếu file này chứa bất kỳ class nào có >= 200 ảnh thì bỏ qua (KHÔNG DI CHUYỂN)
        if any(class_id not in low_sample_classes for class_id in class_ids):
            continue  # Bỏ qua file này, giữ nguyên vị trí cũ

        label_path = os.path.join(labels_dir, label_file)
        image_file = label_file.replace(".txt", ".jpg")  # Giả định ảnh là .jpg
        image_path = os.path.join(images_dir, image_file)

        print(f"Moving file '{label_file}' with classes {[classes[c] for c in class_ids]}...")

        # Di chuyển file label
        if os.path.exists(label_path):
            shutil.move(label_path, os.path.join(dest_dir, "labels", label_file))
        # Di chuyển file ảnh nếu tồn tại
        if os.path.exists(image_path):
            shutil.move(image_path, os.path.join(dest_dir, "images", image_file))

    print("✅ Done! Only files with low-sample data have been moved.")

# Cấu hình đường dẫn
labels_directory = r"C:\Users\Lenovo\Desktop\817\Data\train\labels"
images_directory = r"C:\Users\Lenovo\Desktop\817\Data\train\images"
class_file_path = r"C:\Users\Lenovo\Desktop\817\Data\classes14.txt"
destination_directory = r"C:\Users\Lenovo\Desktop\817\Data\few_samples"

move_low_sample_files(labels_directory, images_directory, class_file_path, destination_directory)
