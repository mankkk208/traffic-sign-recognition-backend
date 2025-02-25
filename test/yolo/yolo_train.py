# pylint: disable=no-member
from ultralytics import YOLO

# Định nghĩa đường dẫn model YOLO
#MODEL_PATH = "models/yolo/yolov8n_finetune/weights/last.pt" # Fine-tune Model từ checkpoint
MODEL_PATH = "models/yolo/yolo11s.pt" #fine-tune Model lần đầu

# Định nghĩa đường dẫn đến file cấu hình dataset
DATA_CONFIG_PATH = "data/yolo/via-trafficsign.yaml"
# Định nghĩa đường dẫn đến file hyperparameter (hyp)
#HYP_CONFIG_PATH = "data/yolo/hyp.yaml"  # Đường dẫn tới file hyp.yaml

# Huấn luyện YOLO
def train_yolo():
    # Load model YOLOv8
    model = YOLO(MODEL_PATH)

    # Fine-tuning model
    model.train(    
        data=DATA_CONFIG_PATH,  # Đường dẫn file cấu hình dataset
        epochs=30,              # Số epoch
        batch=16,               # Batch size
        imgsz=320,              # Kích thước ảnh đầu vào
        workers=4,              # Số luồng xử lý dữ liệu
        device="cuda",          # Sử dụng GPU nếu có
        project="models/yolo",  # Thư mục lưu model
        name="yolov11s_finetune",  # Tên folder chứa model đã train
        # Custom preprocessing function (added)
        augment=True,  # Enable augmentation
        #hyp=HYP_CONFIG_PATH,  # Thêm tham số hyp ở đây
        #cache=True      # Cache images to speed up training
    )

if __name__ == "__main__":
    train_yolo()
