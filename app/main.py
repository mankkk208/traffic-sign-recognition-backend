# pylint: disable=no-member
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model
from src.config import MODEL_DIR, INPUT_SHAPE, CLASS_NAMES

# Load model đã được train
model_path = os.path.join(MODEL_DIR, "best_model.h5")
model = load_model(model_path)

app = FastAPI()

def preprocess_image(image: np.ndarray):
    """
    Tiền xử lý ảnh từ uploaded file trước khi đưa vào mô hình dự đoán.
    """
    # Chuyển ảnh từ RGB sang BGR để đồng nhất với cách đọc của OpenCV
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # Chỉnh kích thước ảnh về INPUT_SHAPE (chiều cao, chiều rộng)
    img = cv2.resize(image, (INPUT_SHAPE[1], INPUT_SHAPE[0]))
    # Chuẩn hóa ảnh về khoảng [0, 1]
    img = img / 255.0
    # Add batch dimension: (height, width, channels) -> (1, height, width, channels)
    img = np.expand_dims(img, axis=0)
    return img

@app.post("/predict/")  
async def predict(file: UploadFile = File(...)):
    """
    Nhận file ảnh từ request, tiền xử lý ảnh và dự đoán bằng mô hình đã train.
    """
    try:
        contents = await file.read()
        # Mở ảnh với PIL và chuyển sang numpy array
        image = Image.open(BytesIO(contents)).convert("RGB")  # Đảm bảo ảnh luôn ở chế độ RGB
        image_np = np.array(image)

        # Preprocess the image
        preprocessed_image = preprocess_image(image_np)
        
        # Perform prediction
        prediction = model.predict(preprocessed_image)
        class_id = np.argmax(prediction)
        predicted_sign = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else "Unknown Sign"
        
        return JSONResponse(content={"Predicted sign": predicted_sign})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/")
async def root():
    return {"message": "Traffic Sign Recognition API is running!"}
