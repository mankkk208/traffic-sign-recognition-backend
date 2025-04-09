# pylint: disable=no-member
import os
import io
import cv2
import numpy as np
from PIL import Image
import httpx
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.routers.yolo_detector import YOLODetector
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
CONFIDENCE_THRESHOLD = 0.8
GEMINI_PREDICT_URL = f"{BASE_URL}/gemini/predict/"

yolo_model_path = 'app/models/yolo/yolov11m_finetune230325/weights/best.pt'
yolo_detector = YOLODetector(model_path=yolo_model_path, conf_threshold=CONFIDENCE_THRESHOLD, nms_threshold=0.4)

yolo_router = APIRouter()

@yolo_router.post("/predict/")
async def predict_yolo(file: UploadFile = File(...)):
    try:
        file_contents = await file.read()
        file_buffer = io.BytesIO(file_contents)
        image = Image.open(file_buffer)
        image_np = np.array(image)

        # Kiểm tra định dạng ảnh (Grayscale hoặc RGBA) và chuyển về BGR
        if len(image_np.shape) == 2:
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        elif image_np.shape[-1] == 4:
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)
        else:
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # 👉 Dùng bản HSV cho prediction, giữ bản BGR để vẽ bbox và hiển thị
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        results = yolo_detector.model(image_hsv)
        detected_signs = []

        for result in results:
            for box in result.boxes.data.tolist():
                x1, y1, x2, y2, conf, class_id = box
                conf = float(conf)
                class_id = int(class_id)
                label = result.names[class_id]
                if conf >= CONFIDENCE_THRESHOLD:
                    detected_signs.append(f"{label} (Conf: {conf:.2f})")
                    # 🟢 Vẽ bbox lên ảnh gốc (BGR)
                    cv2.rectangle(image_bgr, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(image_bgr, f"ID {class_id}", (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if detected_signs:
            _, img_encoded = cv2.imencode(".jpg", image_bgr)
            img_base64 = base64.b64encode(img_encoded).decode("utf-8")
            return {
                "prediction": ", ".join(detected_signs),  # Text area sẽ hiển thị label
                "image_base64": img_base64                # Ảnh vẽ class ID trên ảnh gốc
            }

        # Không đủ độ tin cậy => Gửi sang Gemini
        file_buffer.seek(0)
        files = {"file": (file.filename, file_buffer, file.content_type)}
        async with httpx.AsyncClient() as http_client:
            gemini_response = await http_client.post(
                GEMINI_PREDICT_URL,
                files=files,
                timeout=30.0
            )
            return gemini_response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e