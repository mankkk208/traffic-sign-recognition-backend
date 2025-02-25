# pylint: disable=no-member
import os
import pandas as pd
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from .config import DATA_DIR, INPUT_SHAPE

def load_data(csv_path):
    data = pd.read_csv(csv_path)
    images = []
    labels = []
    
    for idx, row in data.iterrows():
        # Update the path based on the new dataset structure
        img_path = os.path.join(DATA_DIR, 'cnn', row['Path'])
        img = cv2.imread(img_path)
        img = cv2.resize(img, INPUT_SHAPE[:2])
        img = img / 255.0  # Normalize pixel to [0, 1]
        images.append(img)
        labels.append(row['ClassId'])
    
    return np.array(images), np.array(labels)

def prepare_data():
    # Load training data (updated path)
    train_data_path = os.path.join(DATA_DIR, 'cnn', 'Train.csv')
    X, y = load_data(train_data_path)
    
    # Split into train/validation sets (80% train - 20% validation)
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Load test data (updated path)
    test_data_path = os.path.join(DATA_DIR, 'cnn', 'Test.csv')
    X_test, y_test = load_data(test_data_path)
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)
