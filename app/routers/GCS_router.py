from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from src.gcs import upload_to_gcs, delete_from_gcs
import os

gcs_router = APIRouter()

# Bucket của bạn trên GCS
BUCKET_NAME = "traffic-sign-recognition-storage"

@gcs_router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Lưu tạm file trên server
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Upload file lên GCS
    gcs_url = upload_to_gcs(BUCKET_NAME, file_location, file.filename)

    # Xóa file tạm thời trên server
    os.remove(file_location)

    # Trả về URL của ảnh đã upload
    return JSONResponse(content={"url": gcs_url}, status_code=200)

@gcs_router.delete("/delete/{file_name}")
async def delete_file(file_name: str):
    # Xóa file trên GCS
    delete_from_gcs(BUCKET_NAME, file_name)
    return {"message": f"File {file_name} deleted successfully from GCS."}
