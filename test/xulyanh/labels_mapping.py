import os

# Định nghĩa mapping class từ [0-13] về [1-5]
class_mapping = {
    0: 0,  # Cấm đi ngược chiều
    1: 1,  # Phải đi vòng sang bên phải
    2: 2,  # Cấm đỗ xe
    3: 3,  # Cấm dừng xe và đỗ xe
    6: 4   # Vị trí người đi bộ sang ngang
}

def convert_labels(labels_dir):
    """ Chuyển đổi các file labels theo class_mapping và loại bỏ class không mong muốn """
    for label_file in os.listdir(labels_dir):
        if label_file.endswith(".txt"):
            label_path = os.path.join(labels_dir, label_file)
            
            # Đọc file và xử lý từng dòng
            new_lines = []
            with open(label_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    class_id = int(parts[0])
                    
                    # Chỉ giữ lại các class mong muốn
                    if class_id in class_mapping:
                        parts[0] = str(class_mapping[class_id])  # Chuyển ID class
                        new_lines.append(" ".join(parts))

            # Nếu file có nội dung hợp lệ sau khi chuyển đổi, ghi đè lại file
            if new_lines:
                with open(label_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines) + "\n")
            else:
                # Nếu file không có class hợp lệ nào -> Xóa file label
                os.remove(label_path)
                print(f"🗑️ Đã xóa file {label_file} vì không chứa class hợp lệ.")

    print("\n✅ Hoàn thành! Tất cả file labels đã được cập nhật.")

# Đường dẫn thư mục chứa file labels
labels_directory = r"C:\Users\Lenovo\Desktop\817\Data\val\labels"

convert_labels(labels_directory)
