# pylint: disable=no-member
import os
import io
import cv2
import numpy as np
from PIL import Image
import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.routers.yolo_detector import YOLODetector

CONFIDENCE_THRESHOLD = 0.8
GPT_PREDICT_URL = "http://localhost:8000/gpt/predict/"
GEMINI_PREDICT_URL = "http://localhost:8000/gemini/predict/"

# Load YOLO model
yolo_model_path = 'app/models/yolo/yolov11m_finetune230325/weights/best.pt'
yolo_detector = YOLODetector(model_path=yolo_model_path, conf_threshold=CONFIDENCE_THRESHOLD, nms_threshold=0.4)

yolo_router = APIRouter()

@yolo_router.post("/predict/")
async def predict_yolo(file: UploadFile = File(...)):
    try:
        # Đọc và xử lý ảnh
        file_contents = await file.read()
        file_buffer = io.BytesIO(file_contents)
        image = Image.open(file_buffer)
        image_np = np.array(image)
        
        if image_np is None:
            raise HTTPException(status_code=400, detail="Không thể đọc ảnh")
        if len(image_np.shape) == 2:  # Grayscale -> BGR
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        elif image_np.shape[-1] == 4:  # RGBA -> BGR
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
        
        # Chuyển đổi từ BGR sang HSV
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
        
        # Resize ảnh
        image_np = cv2.resize(image_np, (640, 640))
        
        # Dự đoán với YOLO
        results = yolo_detector.model(image_np)
        detected_signs = []
        for result in results:
            for box in result.boxes.data.tolist():
                conf = box[4]
                class_id = int(box[5])
                label = result.names[class_id]
                if conf >= CONFIDENCE_THRESHOLD:
                    detected_signs.append(f"{label} (Conf: {conf:.2f})")
        
        # Nếu có kết quả từ YOLO với độ tin cậy cao
        if detected_signs:
            return JSONResponse(content={"prediction": ", ".join(detected_signs)})
        
        # Nếu không có kết quả hoặc độ tin cậy thấp, chuyển sang Gemini
        file_buffer.seek(0)
        files = {"file": (file.filename, file_buffer, file.content_type)}
        async with httpx.AsyncClient() as http_client:
            gemini_response = await http_client.post(
                GEMINI_PREDICT_URL,
                files=files,
                timeout=30.0
            )
            print(gemini_response.json())
            return gemini_response.json()

        # # Nếu không có kết quả hoặc độ tin cậy thấp, chuyển sang GPT
        # file_buffer.seek(0)
        # files = {"file": (file.filename, file_buffer, file.content_type)}
        # async with httpx.AsyncClient() as http_client:
        #     gpt_response = await http_client.post(
        #         GPT_PREDICT_URL,
        #         files=files,
        #         timeout=30.0
        #     )
        #     print(gpt_response.json())
        #     return gpt_response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
