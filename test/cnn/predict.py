# pylint: disable=no-member
import os
import sys
import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from src.config import DATA_DIR, MODEL_DIR, INPUT_SHAPE
from ultralytics import YOLO

CLASS_NAMES = [
    "Speed limit (20km/h)",
    "Speed limit (30km/h)",
    "Speed limit (50km/h)",
    "Speed limit (60km/h)",
    "Speed limit (70km/h)",
    "Speed limit (80km/h)",
    "End of speed limit (80km/h)",
    "Speed limit (100km/h)",
    "Speed limit (120km/h)",
    "No passing",
    "No passing for vehicles over 3.5 tons",
    "Right-of-way at the next intersection",
    "Priority road",
    "Yield",
    "Stop",
    "No vehicles",
    "Vehicles over 3.5 tons prohibited",
    "No entry", "General caution",
    "Dangerous curve to the left",
    "Dangerous curve to the right",
    "Double curve",
    "Bumpy road",
    "Slippery road",
    "Road narrows on the right",
    "Road work",
    "Traffic signals",
    "Pedestrians",
    "Children crossing",
    "Bicycles crossing",
    "Beware of ice/snow",
    "Wild animals crossing",
    "End of all speed and passing limits",
    "Turn right ahead",
    "Turn left ahead",
    "Ahead only",
    "Go straight or right",
    "Go straight or left",
    "Keep right",
    "Keep left",
    "Roundabout mandatory",
    "End of no passing",
    "End of no passing by vehicles over 3.5 tons"
]

class TrafficSignRecognizer:
    
    # Load model đã train
    def __init__(self):
        self.model = load_model(os.path.join(MODEL_DIR, 'best_model.h5'))
        
    def _load_class_names(self):
        class_df = pd.read_csv(os.path.join(DATA_DIR, 'class_names.csv'))
        return dict(zip(class_df['ClassId'], class_df['SignName']))  # Trả về dictionary {ClassId: SignName}
    
    def predict(self, image_path):
        # Tiền xử lý ảnh với image_path
        # Đọc ảnh bằng OpenCV (cv2.imread).
        img = cv2.imread(image_path)
        img = cv2.resize(img, INPUT_SHAPE[:2])
        img = img / 255.0  # Normalize
        img = np.expand_dims(img, axis=0)

        # Dự đoán nhãn bằng mô hình CNN
        pred = self.model.predict(img)
        class_id = np.argmax(pred)

        # Lấy tên biển báo từ class_id
        sign_name = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else "Unknown Sign"
        return sign_name

if __name__ == '__main__':
    recognizer = TrafficSignRecognizer()
    image_path = 'data/Test/00032.png'
    print(f'Predicted sign: {recognizer.predict(image_path)}')