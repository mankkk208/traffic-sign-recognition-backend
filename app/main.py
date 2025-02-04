# pylint: disable=no-member
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from tensorflow.keras.models import load_model

# Import config
from src.config import MODEL_DIR, INPUT_SHAPE, CLASS_NAMES

# Load model đã được train
model_path = os.path.join(MODEL_DIR, "best_model.h5")
model = load_model(model_path)

app = FastAPI()

def preprocess_image(image: np.ndarray):
    """
    Tiền xử lý ảnh từ uploaded file trước khi đưa vào mô hình dự đoán.
    """
    # chỉnh kích thước ảnh về kích thước mà mô hình đã train
    img = cv2.resize(image, INPUT_SHAPE[:2])
    # chuẩn hóa ảnh về khoảng [0, 1]
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
        # mở ảnh với PIL.Image
        image = Image.open(BytesIO(contents))
        # đoạn code này sẽ đọc file ảnh từ request, sau đó chuyển ảnh sang dạng numpy array
        image_np = np.array(image)
        
        # chuyển từ ảnh màu RGBA sang RGB
        if image_np.ndim == 3 and image_np.shape[-1] == 4:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
        elif image_np.ndim == 2:
            # nếu ảnh đen trắng thì chuyển sang ảnh màu
            image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2RGB)

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
