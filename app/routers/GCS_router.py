from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.routers.gcs import upload_to_gcs
import io
import os
from dotenv import load_dotenv
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/gen-lang-client-0788085518-6a37c52bd548.json"

load_dotenv()

# Bucket của bạn trên GCS
BUCKET_NAME = "traffic-sign-recognition-storage"

gcs_router = APIRouter()

@gcs_router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()  # Đọc dữ liệu file vào biến bytes
    file_stream = io.BytesIO(file_bytes)  # Chuyển đổi thành stream để upload

    gcs_url = upload_to_gcs(BUCKET_NAME, file_stream, file.filename)

    if gcs_url:
        return JSONResponse(content={"url": gcs_url})  # Đổi từ "public_url" thành "url" cho đồng nhất với JS
    else:
        print("Lỗi upload GCS")
        return JSONResponse(content={"message": "Lỗi upload GCS"}, status_code=500)
