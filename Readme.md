# Traffic Sign Recognition

## Description
This project is designed to recognize traffic signs using machine learning techniques. It aims to improve road safety by providing real-time recognition of traffic signs for drivers.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/mankkk208/Traffic-Sign-Recognition
   ```
2. Download datasets 
   Dataset for cnn model can be downloaded from https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign?resource=download
   Extract the archive to the `data\cnn` directory.
   
   Dataset for cnn model can be downloaded from https://github.com/makerhanoi/via-datasets/releases/download/v1.0/via-trafficsign-20210321.zip
   or https://www.kaggle.com/datasets/lvnduy/street-traffic-signs-in-vietnam-coco
   Extract the archive to the `data\yolo` directory.
4. Navigate to the project directory:
   ```bash
   cd traffic_sign_recognition
   ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
First you need to run the `train.py` and `yolo_train.py` to train and create our models.
To run the traffic sign recognition model, execute the following command:
```bash
fastapi dev
```
