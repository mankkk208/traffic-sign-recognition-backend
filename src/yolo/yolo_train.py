from ultralytics import YOLO

# Định nghĩa đường dẫn đến file cấu hình dataset
DATA_CONFIG_PATH = "data/yolo/via-trafficsign.yaml"

# Định nghĩa đường dẫn model YOLO
#MODEL_PATH = "models/yolo/yolov8n.pt"  # Fine-tune Model pretrained lần đầu
MODEL_PATH = "models/yolo/yolov8n_finetune/weights/last.pt"
# Huấn luyện YOLO
def train_yolo():
    # Load model YOLOv8
    model = YOLO(MODEL_PATH)

    # Fine-tuning model
    model.train(
        data=DATA_CONFIG_PATH,  # Đường dẫn file cấu hình dataset
        epochs=30,              # Số epoch
        batch=16,               # Batch size
        imgsz=224,              # Kích thước ảnh đầu vào
        workers=4,              # Số luồng xử lý dữ liệu
        #amp=False,
        device="cuda",          # Sử dụng GPU nếu có
        project="models/yolo",  # Thư mục lưu model
        name="yolov8n_finetune"  # Tên folder chứa model đã train
    )

if __name__ == "__main__":
    train_yolo()
