import numpy as np
from tensorflow.keras.models import load_model
import os
import sys
from src.data_loader import prepare_data
from src.config import MODEL_DIR

# Load model best_model.h5.
# # Đánh giá trên tập test.
def evaluate():
    # Load test data
    _, _, (X_test, y_test) = prepare_data()
    
    # Load model
    model = load_model(os.path.join(MODEL_DIR, 'best_model.h5'))
    
    # Evaluate
    loss, acc = model.evaluate(X_test, y_test)
    print(f'Test accuracy: {acc*100:.2f}%')

if __name__ == '__main__':
    evaluate()