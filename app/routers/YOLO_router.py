# pylint: disable=no-member
import os
import io
import torch
import cv2
import numpy as np
from PIL import Image

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from src.yolo.yolo_detector import YOLODetector

from src.config import MODEL_DIR

CONFIDENCE_THRESHOLD = 0.8
GCS_UPLOAD_URL = "http://localhost:8000/gcs/upload/"
GPT_PREDICT_URL = "http://localhost:8000/gpt/predict/"

# Load YOLO model
yolo_model_path = os.path.join(MODEL_DIR, 'yolo/yolov11s_finetune/weights/best.pt')
yolo_detector = YOLODetector(model_path=yolo_model_path, conf_threshold=CONFIDENCE_THRESHOLD, nms_threshold=0.4)

yolo_router = APIRouter()

@yolo_router.post("/predict/")
async def predict_yolo(file: UploadFile = File(...)):
    """
    Nhận ảnh từ request, xử lý và dự đoán bằng mô hình YOLOv8.
    """
    try:
        # Đọc ảnh từ file tải lên
        contents = await file.read()
        image_data = io.BytesIO(contents)
        image = Image.open(image_data)

        # Chuyển đổi từ PIL.Image sang numpy array (OpenCV có thể xử lý numpy array)
        image = np.array(image)

        # Đảm bảo ảnh có 3 kênh (RGB)
        if image.shape[-1] == 4:  # Nếu ảnh có 4 kênh (RGBA)
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        elif image.shape[-1] == 1:  # Nếu ảnh là grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # Đảm bảo ảnh có kích thước phù hợp cho YOLO
        image = cv2.resize(image, (320, 320))
        #image = image / 255.0  # Chuẩn hóa giá trị pixel về [0, 1]
        
        print(f"📸 Image received: {file.filename}")

        # Dự đoán với YOLO: Truyền ảnh dưới dạng numpy ndarray vào model
        results = yolo_detector.model(image)

        detected_signs = []
        for result in results:
            for box in result.boxes.data.tolist():
                conf = box[4]
                if conf >= yolo_detector.conf_threshold:
                    class_id = int(box[5])  # class ID của biển báo
                    label = result.names[class_id]
                    detected_signs.append(f"Tên biển báo: {label}, Confidence: {conf:.2f}")
                    print(f"Detected sign: {label} with Confidence: {conf:.2f}")
        
        # Kiểm tra nếu không có dự đoán nào
        if not detected_signs:
            return JSONResponse(content={"message": "Không nhận diện được biển báo"}, status_code=200)
 
        return JSONResponse(content={"Detected signs from YOLO": detected_signs})

    except Exception as e:
        print("❌ Lỗi trong API:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
