import os
import tensorflow as tf
from tensorflow.keras import layers, models
from .data_loader import prepare_data
from .config import *

def build_model():
    model = models.Sequential([
        # Convolutional Layer: Trích xuất đặc trưng từ ảnh.
        # Pooling Layer: Giảm độ phức tạp của ảnh.
        layers.Conv2D(32, (3,3), activation='relu', input_shape=INPUT_SHAPE),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),
        layers.Conv2D(128, (3,3), activation='relu'),
        # Flatten & Dense Layers: Biến ma trận thành vector & phân loại.
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        # Softmax: Tính xác suất cho từng loại biển báo.
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    # Dùng Adam optimizer để tối ưu hàm loss.
    model.compile(optimizer=tf.keras.optimizers.Adam(LEARNING_RATE),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def train():
    # Load data
    (X_train, y_train), (X_val, y_val), _ = prepare_data()
    
    # Build model
    model = build_model()
    model.summary()
    
    # Callbacks
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(MODEL_DIR, 'best_model.h5'),
            save_best_only=True,
            monitor='val_accuracy'
        ),
        tf.keras.callbacks.EarlyStopping(
            patience=5,
            restore_best_weights=True
        )
    ]
    
    # Training
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks
    )
    
    #Output: Mô hình CNN được lưu vào models/best_model.h5.
    return model

if __name__ == '__main__':
    train()