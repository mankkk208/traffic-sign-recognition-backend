import os
from collections import Counter

def remove_low_sample_labels(labels_dir, class_file, threshold=200):
    # Đọc danh sách class
    with open(class_file, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f.readlines()]

    class_counter = Counter()
    
    # Đếm số lần xuất hiện của từng class trong toàn bộ dataset
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

    # Xác định class nào có ít hơn threshold ảnh
    low_sample_classes = {class_id for class_id, count in class_counter.items() if count < threshold}

    # Duyệt lại từng file label để xóa các dòng thuộc class ít hơn 200 ảnh
    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(labels_dir, filename)
            
            # Đọc dữ liệu và lọc bỏ dòng không cần thiết
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            new_lines = [line for line in lines if int(line.split()[0]) not in low_sample_classes]

            # Nếu file bị xoá hết dữ liệu, xoá file đó luôn
            if not new_lines:
                os.remove(file_path)
                print(f"🗑️ Đã xóa file rỗng: {filename}")
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)

    print("\n✅ Đã xoá hết các dòng có biển báo ít hơn 200 ảnh.")

# Thay đổi đường dẫn tương ứng
labels_directory = r"C:\Users\Lenovo\Desktop\817\Data\train\labels"  # Đường dẫn đến thư mục chứa file labels
class_file_path = r"C:\Users\Lenovo\Desktop\817\Data\classes14.txt"  # Đường dẫn đến file class.txt

remove_low_sample_labels(labels_directory, class_file_path)
