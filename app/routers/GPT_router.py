from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from src.config import GPT_API_KEY
from fastapi.responses import JSONResponse
# Khởi tạo router cho GPT
gpt_router = APIRouter()

# Client OpenAI
client = OpenAI(api_key=GPT_API_KEY)

# System prompt
system_prompt = """
Bạn là AI nhận diện biển báo giao thông Việt Nam. Hãy dự đoán tên các biển báo trong ảnh.
Chỉ cần nói ra tên biển báo như sau:
Tên biển báo 1: ...
Tên biển báo 2: ...
Nếu bạn không nhận diện được biển báo, hãy trả lời 'Không nhận diện được biển báo'.
"""

user_prompt = "Cho tôi biết tên các biển báo giao thông Việt Nam trong ảnh."

# Định nghĩa request body bằng Pydantic
class ImageRequest(BaseModel):
    image_url: str  # Yêu cầu image_url phải là một chuỗi

@gpt_router.post("/predict/")
def predict_gpt(request: ImageRequest):
    try:
        response = client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:has::B2BLb0gS",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
                {"role": "user", "content": f"image_url:{request.image_url}"}
            ]
        )
        prediction_text = response.choices[0].message.content
        print(f"prediction: {prediction_text}")
        # Trả về JSON hợp lệ
        return JSONResponse(content={"prediction": prediction_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
