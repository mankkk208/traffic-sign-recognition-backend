# pylint: disable=no-member
from ultralytics import YOLO
import cv2
import numpy as np

class YOLODetector:
    def __init__(self, model_path, conf_threshold=0.7, nms_threshold=0.4):
        # Load pre-trained YOLOv8 model
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold

    def predict(self, image_path):
        # Đọc và kiểm tra ảnh
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image {image_path} could not be loaded. Please check the file path or image format.")
        print(f"✅ Image loaded successfully: {image_path}, Shape: {image.shape}")

        # Resize ảnh cho phù hợp với yêu cầu của YOLO
        image_resized = cv2.resize(image, (320, 320))  
        #cv2.imwrite("resized_image.jpg", image_resized)  # Lưu ảnh đã resize
        
        # Dự đoán với YOLO
        results = self.model(image_resized)
        # Dự đoán với YOLO
        #results = self.model("resized_image.jpg")

        # Xử lý kết quả trả về
        predictions = []
        for result in results:
            for box in result.boxes.data.tolist():
                conf = box[4]
                if conf >= self.conf_threshold:
                    # Nếu độ tin cậy > threshold, thêm vào kết quả
                    class_id = int(box[5])  # class ID của biển báo
                    label = result.names[class_id]
                    predictions.append(label)
        print(f"Detected labels: {predictions}")
                    
        if not predictions:
                return ["No signs detected"]
        
        return predictions
            