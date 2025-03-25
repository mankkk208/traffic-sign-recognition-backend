#pylint: disable=no-member
from ultralytics import YOLO
import cv2
import os

# Đường dẫn đến mô hình đã train xong
model_path = "app/models/yolo/yolov11m_finetune230325/weights/best.pt"

# Load mô hình YOLO
model = YOLO(model_path)

# Đường dẫn thư mục ảnh validation
val_img_dir = r"C:\Users\Lenovo\Desktop\Dataset\processed\I.423a"
output_dir = r"C:\Users\Lenovo\Desktop\817\Data\testrun2"

# Tạo thư mục output nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# Lấy danh sách file ảnh trong tập validation
image_files = [f for f in os.listdir(val_img_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

# Dự đoán trên từng ảnh và lưu kết quả
for img_name in image_files:
    img_path = os.path.join(val_img_dir, img_name)

    # Chạy dự đoán
    results = model(img_path, conf=0.25, iou=0.4)  # conf=0.25 là ngưỡng tin cậy

    # Đọc ảnh gốc để vẽ kết quả
    img = cv2.imread(img_path)

    # Vẽ bounding boxes lên ảnh
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Lấy toạ độ bounding box
            conf = box.conf[0].item()  # Độ tin cậy của dự đoán
            cls = int(box.cls[0].item())  # Lớp dự đoán
            label = f"{cls} ({conf:.2f})"

            # Vẽ khung chữ nhật và nhãn
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Lưu ảnh đã vẽ ra thư mục output
    output_path = os.path.join(output_dir, img_name)
    cv2.imwrite(output_path, img)

print(f"Kết quả dự đoán đã lưu vào thư mục: {output_dir}")