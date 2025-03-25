import os
import shutil
from collections import defaultdict

def get_class_counts(labels_dir):
    """ Đếm số lần xuất hiện của mỗi class trong dataset """
    class_counter = defaultdict(set)  # Lưu danh sách file chứa từng class

    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(labels_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    class_id = int(line.split()[0])  # Lấy ID class
                    class_counter[class_id].add(filename)  # Thêm ảnh chứa class này

    return {cls: len(files) for cls, files in class_counter.items()}, class_counter

def balance_dataset(labels_dir, images_dir, val_dir, class_file, threshold=200):
    """ Chuyển ảnh dư vào val nhưng vẫn giữ tối thiểu 200 ảnh/class """
    # Đọc danh sách class
    with open(class_file, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f.readlines()]
    
    # Đếm số lượng ảnh/class trước khi di chuyển
    class_counts, class_files = get_class_counts(labels_dir)

    # Tạo thư mục val nếu chưa có
    os.makedirs(os.path.join(val_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(val_dir, "labels"), exist_ok=True)

    # Danh sách ảnh có thể di chuyển
    removable_images = set()

    # Duyệt qua từng class để tìm ảnh dư
    for class_id, files in class_files.items():
        if class_counts[class_id] > threshold:
            extra_files = list(files)[threshold:]  # Ảnh dư thừa
            removable_images.update(extra_files)  # Đánh dấu ảnh có thể di chuyển

    # Duyệt qua từng ảnh, chỉ di chuyển nếu **tất cả class trong ảnh** đều có > 200 ảnh
    for image_file in removable_images:
        label_path = os.path.join(labels_dir, image_file)
        image_path = os.path.join(images_dir, image_file.replace(".txt", ".jpg"))

        # Kiểm tra nếu xóa ảnh này thì có làm class nào < 200 không
        with open(label_path, "r", encoding="utf-8") as f:
            classes_in_image = {int(line.split()[0]) for line in f}

        # Kiểm tra nếu mọi class trong ảnh đều dư > 200 thì mới di chuyển
        if all(class_counts[class_id] > threshold for class_id in classes_in_image):
            # Di chuyển label
            shutil.move(label_path, os.path.join(val_dir, "labels", image_file))
            # Di chuyển ảnh nếu tồn tại
            if os.path.exists(image_path):
                shutil.move(image_path, os.path.join(val_dir, "images", image_file.replace(".txt", ".jpg")))
            
            # Giảm số lượng ảnh/class sau khi di chuyển
            for class_id in classes_in_image:
                class_counts[class_id] -= 1

    print("\n✅ Hoàn thành! Tất cả class đều có ít nhất 200 ảnh.")

# Đường dẫn thư mục
labels_directory = r"C:\Users\Lenovo\Desktop\817\Data\train\labels"  
images_directory = r"C:\Users\Lenovo\Desktop\817\Data\train\images"  
val_directory = r"C:\Users\Lenovo\Desktop\817\Data\val"  
class_file_path = r"C:\Users\Lenovo\Desktop\817\Data\classes14.txt"  

balance_dataset(labels_directory, images_directory, val_directory, class_file_path)
