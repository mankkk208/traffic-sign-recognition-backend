from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from src.gcs import upload_to_gcs, delete_from_gcs
import os


# Bucket của bạn trên GCS
BUCKET_NAME = "traffic-sign-recognition-storage"

gcs_router = APIRouter()

@gcs_router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    gcs_url = upload_to_gcs(BUCKET_NAME, file_location, file.filename)
    os.remove(file_location)
    
    return JSONResponse(content={"url": gcs_url})

@gcs_router.delete("/delete/{file_name}")
async def delete_file(file_name: str):
    delete_from_gcs(BUCKET_NAME, file_name)
    return {"message": f"File {file_name} deleted from GCS."}
