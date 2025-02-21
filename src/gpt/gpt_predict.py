from openai import OpenAI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.config import GPT_API_KEY
client = OpenAI(api_key=GPT_API_KEY)

# Đường dẫn URL của ảnh đã được tải lên
image_url = "https://storage.googleapis.com/traffic-sign-recognition-storage/y-nghia-cua-bien-bao-cam-re-phai.png"

# Prompt cho hệ thống và người dùng
system_prompt = "Bạn là AI nhận diện biển báo giao thông Việt Nam. Hãy dự đoán tên các biển báo trong ảnh, trong ảnh có thể có một hoặc nhiều biển báo. Chỉ cần nói ra tên biển báo ví dụ như sau: Tên biển báo 1: ... Tên biển báo 2: ... Nếu bạn không nhận diện được biển báo hãy trả lời 'Không nhận diện được biển báo'."
user_prompt = "Cho tôi biết tên các biển báo giao thông Việt Nam trong ảnh."

# Gửi request để dự đoán tên biển báo trong ảnh
response = client.chat.completions.create(
    model="ft:gpt-4o-2024-08-06:has::B2BLb0gS",  # muốn dùng model-finetune thì chỉ cần thay tên model, ví dụ model="ft:gpt-4o-mini:my-org:custom_suffix:id"
    messages=[
        {
            "role": "system",
            "content": system_prompt  # Cung cấp prompt hệ thống
        },
        {
            "role": "user",
            "content": user_prompt # Gửi prompt của người dùng
        },
        {
            "role": "user",
            "content": f"image_url:{image_url}"  # Gửi URL của ảnh
        }
    ]
)

# In kết quả dự đoán
print(response.choices[0].message.content)
