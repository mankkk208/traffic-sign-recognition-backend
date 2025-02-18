# Traffic Sign Recognition

## Description
This project is designed to recognize traffic signs using machine learning techniques. It aims to improve road safety by providing real-time recognition of traffic signs for drivers.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/mankkk208/Traffic-Sign-Recognition
   ```
2. Download datasets 
   Dataset for yolo model can be downloaded from https://github.com/makerhanoi/via-datasets/releases/download/v1.0/via-trafficsign-20210321.zip
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
First you need to run the `yolo_train.py` to train and create our models.
To run the traffic sign recognition model, execute the following command:
```bash
fastapi dev
```

## Set up môi trường làm việc Google Cloud
```bash
gcloud auth application-default login
gcloud config set project [PROJECT_ID]
```

## Tải dữ liệu lên Google Cloud Storage (GCS)
1. Upload file train_data.jsonl và dataset lên GCS để Vertex AI có thể fine-tune model.
   Chạy lệnh sau để tạo bucket trên GCS (nếu chưa có):
   ```bash
   gsutil mb -p [PROJECT_ID] -c STANDARD -l us-central1 gs://your-bucket-name/
   ```
   Tải file json lên GCS:
   ```bash
   gsutil cp data/gemini/train_data.jsonl gs://your-bucket-name/train_data.jsonl
   ```
   Tải dataset lên GCS
   ```bash
   gsutil cp data/gemini/path-to-dataset gs://your-bucket-name/train_data.jsonl
   ```
2. Cấp quyền và huấn luyện model
   Truy cập vào https://console.cloud.google.com/
   Chọn IAM & ADMIN ở Dashboard
   cấp các quyền sau cho service account: `AI Platform Admin`, `Service Account Token Creator`, `Storage Admin`, `Vertex AI Administrator`, `Vertex AI User`

   Truy cập vào https://console.cloud.google.com/vertex-ai/
   Chọn Tuning ở Dashboard, chọn Create tuned model, trong phần advance sẽ có chọn service account
   Trong Tuning dataset chọn `Existing file on Cloud Storage` và browse đến file train_data.jsonl. Start tuning
   Sau khi tune xong có thể xem model ở Model Registry, ấn vào tên model để deploy model.