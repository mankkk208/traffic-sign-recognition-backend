from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import httpx
from openai import OpenAI
import io
import os
import time
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()
# Lấy OpenAI API Key
GPT_API_KEY = os.getenv("GPT_API_KEY")
BASE_URL = os.getenv("BASE_URL")

# Khởi tạo router và OpenAI client
gpt_router = APIRouter()
client = OpenAI(api_key=GPT_API_KEY)
GCS_UPLOAD_URL = f"{BASE_URL}/gcs/upload/"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/gen-lang-client-0788085518-6a37c52bd548.json"

# System prompt
system_prompt = """
Bạn là AI nhận diện biển báo giao thông Việt Nam. Hãy dự đoán tên các biển báo trong ảnh.
Chỉ cần nói ra tên biển báo như sau:
Tên biển báo 1: ...
Tên biển báo 2: ...
Nếu bạn không nhận diện được biển báo, hãy trả lời 'Không nhận diện được biển báo'.
"""

user_prompt = "Cho tôi biết tên các biển báo giao thông Việt Nam trong ảnh."

@gpt_router.post("/predict/")
async def predict_gpt(file: UploadFile = File(...)):
    try:
        # Thêm timestamp vào tên file
        timestamp = int(time.time())
        file_name = f"{timestamp}_{file.filename}"
        
        # Đọc file vào RAM thay vì lưu trên ổ đĩa
        file_stream = io.BytesIO(await file.read())
        
        # Upload ảnh lên GCS với file stream
        files = {"file": (file_name, file_stream, file.content_type)}
        async with httpx.AsyncClient() as http_client:
            gcs_response = await http_client.post(
                GCS_UPLOAD_URL,
                files=files,
                timeout=30.0
            )
            
            if gcs_response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to upload image to GCS")
            
            image_url = gcs_response.json()["url"]

        # Gửi URL đến GPT để dự đoán
        response = client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:has::B2BLb0gS",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
                {"role": "user", "content": f"image_url:{image_url}"}
            ]
        )

        prediction_text = response.choices[0].message.content
        print(f"Prediction: {prediction_text}")
        return JSONResponse(content={"prediction": prediction_text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
