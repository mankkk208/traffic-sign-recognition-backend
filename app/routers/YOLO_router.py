# pylint: disable=no-member
import os
import sys
import cv2

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from src.yolo.yolo_detector import YOLODetector
from src.config import MODEL_DIR

# Load YOLO model
yolo_model_path = os.path.join(MODEL_DIR, 'yolo/yolov8n_finetune/weights/best.pt')
yolo_detector = YOLODetector(model_path=yolo_model_path, conf_threshold=0.05, nms_threshold=0.3)
#yolo_detector = YOLODetector(model_path=yolo_model_path, conf_threshold=0.5, nms_threshold=0.4)

yolo_router = APIRouter()   

@yolo_router.post("/predict/yolo/")
async def predict_yolo(file: UploadFile = File(...)):
    """
    Receive an image file from the request, preprocess it, and predict using YOLOv8 model.
    """
    try:
        # lưu ảnh nhận được vào file tạm thời
        contents = await file.read()
        temp_path = "temp_uploaded_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        print(f"📸 Image received: {file.filename}, saved as {temp_path}")
        # Dự đoán với YOLO
        detected_signs = yolo_detector.predict(temp_path)

        # Xóa file ảnh tạm sau khi dự đoán
        os.remove(temp_path)

        # Kiểm tra nếu không có dự đoán nào
        if "No signs detected" in detected_signs:
            return JSONResponse(content={"Detected signs from YOLO": detected_signs}, status_code=200)

        return JSONResponse(content={"Detected signs from YOLO": detected_signs})

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})