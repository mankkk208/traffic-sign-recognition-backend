# pylint: disable=no-member
import os
import io
import cv2
import numpy as np
from PIL import Image
import asyncio
import httpx

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
    try:
        # Đọc file ảnh một lần duy nhất và tạo buffer
        file_contents = await file.read()
        file_buffer = io.BytesIO(file_contents)
        image = Image.open(file_buffer)
        image_np = np.array(image)
        
        # Chuyển ảnh về định dạng phù hợp
        if image_np.shape[-1] == 4:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        elif len(image_np.shape) == 2:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        image_np = cv2.resize(image_np, (320, 320))
        
        # Dự đoán với YOLO
        results = yolo_detector.model(image_np)
        detected_signs = []
        for result in results:
            for box in result.boxes.data.tolist():
                conf = box[4]
                class_id = int(box[5])
                label = result.names[class_id]
                if conf >= yolo_detector.conf_threshold:
                    detected_signs.append(f"{label} (Conf: {conf:.2f})")
        
        # Nếu có kết quả từ YOLO, trả về ngay
        if detected_signs:
            return JSONResponse(content={"Detected signs from YOLO": detected_signs})
        
        # Nếu không có kết quả, upload ảnh lên GCS
        file_buffer.seek(0)  # Reset buffer để gửi đi
        files = {"file": (file.filename, file_buffer, file.content_type)}
        print(f"Gửi ảnh {file.filename} lên GCS...")
        
        gcs_url = None
        # Thử tải ảnh lên GCS 3 lần
        MAX_RETRIES = 3
        async with httpx.AsyncClient() as client:
            for attempt in range(MAX_RETRIES):
                try:
                    print(f"Thử gửi ảnh lên GCS lần {attempt+1}")
                    gcs_response = await client.post(GCS_UPLOAD_URL, files=files, timeout=10.0)
                    if gcs_response.status_code == 200:
                        json_resp = gcs_response.json()
                        gcs_url = json_resp.get("url", "")
                        if gcs_url:
                            print(f"Gửi ảnh thành công: {gcs_url}")
                            break
                    else:
                        print(f"GCS response status: {gcs_response.status_code}")
                except Exception as e:
                    print(f"GCS API lỗi ở lần thử {attempt+1}: {e}")
                    await asyncio.sleep(2)  # Chờ 2 giây trước khi thử lại
            
            if not gcs_url:
                return JSONResponse(
                    content={"error": "Lỗi khi upload ảnh lên GCS sau nhiều lần thử"},
                    status_code=500
                )
            
            # Gửi URL ảnh đến GPT để dự đoán
            print(f"Gửi URL tới OpenAI: {gcs_url}")
            gpt_response = await client.post(
                GPT_PREDICT_URL,
                json={"image_url": gcs_url},
                timeout=30.0
            )
            gpt_result = gpt_response.json()
            print(f"GPT Response: {gpt_result}")
            return gpt_result

            #return JSONResponse(content=gpt_response.json())

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
