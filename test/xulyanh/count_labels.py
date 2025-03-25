import os
from collections import Counter

def count_class_occurrences(labels_dir, class_file):
    # Đọc danh sách class
    with open(class_file, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f.readlines()]
    
    class_counter = Counter()
    
    # Duyệt qua tất cả các file trong thư mục labels
    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):  # Chỉ đọc các file .txt
            file_path = os.path.join(labels_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    class_id = int(line.split()[0])  # Lấy ID của class
                    if class_id < len(classes):  # Kiểm tra nếu class_id hợp lệ
                        class_counter[class_id] += 1
                    else:
                        print(f"Warning: Class ID {class_id} in {filename} is out of range.")
    
    # Hiển thị kết quả
    for class_id, count in class_counter.items():
        print(f"{classes[class_id]}: {count}")
    
    return class_counter

# Thay đổi đường dẫn tương ứng
labels_directory = r"C:\Users\Lenovo\Desktop\817\Data\train\labels"  # Đường dẫn đến thư mục chứa file labels
class_file_path = r"C:\Users\Lenovo\Desktop\817\Data\classes.txt"  # Đường dẫn đến file class.txt

result = count_class_occurrences(labels_directory, class_file_path)
