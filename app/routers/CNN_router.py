# # pylint: disable=no-member
# import numpy as np
# import os
# import sys
# import cv2
# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import JSONResponse
# from PIL import Image
# from io import BytesIO
# from tensorflow.keras.models import load_model
# from test.config import MODEL_DIR, INPUT_SHAPE, CLASS_NAMES

# # Load CNN model (ensure the model path is correct)
# model_path = os.path.join(MODEL_DIR, "cnn/best_model.h5")
# model = load_model(model_path)

# cnn_router = APIRouter()

# def preprocess_image(image: np.ndarray):
#     """
#     Preprocess the image before passing it into the model for prediction.
#     """
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
#     img = cv2.resize(image, (INPUT_SHAPE[1], INPUT_SHAPE[0]))  # Resize to the required shape
#     img = img / 255.0  # Normalize to [0, 1]
#     img = np.expand_dims(img, axis=0)  # Add batch dimension
#     return img

# @cnn_router.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     """
#     Receive an image file from the request, preprocess it, and predict using the CNN model.
#     """
#     try:
#         contents = await file.read()
#         image = Image.open(BytesIO(contents)).convert("RGB")  # Ensure RGB format
#         image_np = np.array(image)

#         preprocessed_image = preprocess_image(image_np)
        
#         prediction = model.predict(preprocessed_image)
#         class_id = np.argmax(prediction)
#         predicted_sign = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else "Unknown sign"
#         return JSONResponse(content={"Predicted sign": f"Tên biển báo: {predicted_sign}"})
#     except Exception as e:
#         return JSONResponse(status_code=400, content={"error": str(e)})
