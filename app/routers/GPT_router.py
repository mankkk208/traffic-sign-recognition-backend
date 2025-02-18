from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI

# Khởi tạo router cho GPT
gpt_router = APIRouter()

# Client OpenAI
client = OpenAI(api_key="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")

# Request model
class ImageRequest(BaseModel):
    image_url: str

# Prompt hệ thống
SYSTEM_PROMPT = """
Bạn là AI nhận diện biển báo giao thông Việt Nam. Hãy dự đoán tên các biển báo trong ảnh.
Trong ảnh có thể có một hoặc nhiều biển báo.
Chỉ cần nói ra tên biển báo như sau:
Tên biển báo 1: ...
Tên biển báo 2: ...
Nếu bạn không nhận diện được biển báo, hãy trả lời 'Không nhận diện được biển báo'.
"""
USER_PROMPT = "Cho tôi biết tên các biển báo giao thông Việt Nam trong ảnh."
@gpt_router.post("/predict")
def predict_gpt(request: ImageRequest):
    try:
        response = client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:has::B2BLb0gS",  # Đổi model nếu cần
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT},
                {"role": "user", "content": f"image_url:{request.image_url}"}
            ]
        )
        return {"prediction": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
