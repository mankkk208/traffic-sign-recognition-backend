import os

class_location = r"C:\Users\Lenovo\Desktop\Test\class.txt"


# Đọc danh sách class từ file class.txt
with open(class_location, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

def convert_label_file(label_path, output_path):
    """Chuyển đổi file label YOLO thành file mô tả biển báo"""
    with open(label_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    labels = []
    for line in lines:
        class_id = int(line.split()[0])  # Lấy ID của biển báo
        labels.append(class_names[class_id])
    
    description = f"Trong ảnh có biển báo: {', '.join(labels)}"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(description)

def process_folder(label_folder, output_folder):
    """Xử lý tất cả các file labels trong folder"""
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(label_folder):
        if filename.endswith(".txt"):
            label_path = os.path.join(label_folder, filename)
            output_path = os.path.join(output_folder, filename)
            convert_label_file(label_path, output_path)

# Thay đổi đường dẫn cho phù hợp
label_folder = r"C:\Users\Lenovo\Desktop\Test\val"   # Thư mục chứa file labels cũ
output_folder = r"C:\Users\Lenovo\Desktop\Test\chat_labels"  # Thư mục chứa file labels mới
process_folder(label_folder, output_folder)
