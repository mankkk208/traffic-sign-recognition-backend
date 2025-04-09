# pylint: disable=no-member
from ultralytics import YOLO
import cv2
import os

# =================== CẤU HÌNH ===================
model_path = "app/models/yolo/yolov11m_finetune230325/weights/best.pt"
input_dir = r"C:\Users\Lenovo\Desktop\817\Data\val\val"
output_dir = r"C:\Users\Lenovo\Desktop\817\Data\testrun4"
os.makedirs(output_dir, exist_ok=True)

# =================== TIỀN XỬ LÝ ẢNH ===================
def preprocess_image(image_path):
    """Tiền xử lý ảnh: Chuyển BGR -> HSV (nếu cần)"""
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Không thể đọc ảnh: {image_path}")
        return None

    if len(image.shape) == 2:  # Grayscale
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[-1] == 4:  # RGBA
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return hsv_image

# =================== LOAD MODEL ===================
model = YOLO(model_path)

# =================== CHẠY DỰ ĐOÁN ===================
image_files = [f for f in os.listdir(input_dir) if f.endswith((".jpg", ".png", ".jpeg"))]

for img_name in image_files:
    img_path = os.path.join(input_dir, img_name)

    # Preprocess ảnh đầu vào (HSV)
    input_img = preprocess_image(img_path)
    if input_img is None:
        continue

    # Dự đoán với ảnh đã tiền xử lý
    results = model(input_img, conf=0.25, iou=0.4)

    # Đọc lại ảnh gốc (BGR) để vẽ kết quả
    original_img = cv2.imread(img_path)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = f"{cls} ({conf:.2f})"

            cv2.rectangle(original_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Tính y cho text sao cho không bị mất label
            text_y = y1 - 10 if y1 - 10 > 10 else y1 + 20
            cv2.putText(original_img, label, (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)   

    # Lưu ảnh kết quả
    output_path = os.path.join(output_dir, img_name)
    cv2.imwrite(output_path, original_img)

print(f"Kết quả dự đoán đã lưu vào: {output_dir}")