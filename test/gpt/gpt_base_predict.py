from openai import OpenAI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.config import GPT_API_KEY
client = OpenAI(api_key=GPT_API_KEY)

# Đường dẫn URL của ảnh đã được tải lên
image_url = "https://proauto.vn/wp-content/uploads/2024/06/cac-loai-bien-bao-giao-thong-bien-bao-cam-re-phai.png"

# Define the system prompt
system_prompt = "Bạn là AI nhận diện biển báo giao thông Việt Nam. Hãy dự đoán tên các biển báo trong ảnh, trong ảnh có thể có một hoặc nhiều biển báo. Chỉ cần nói ra tên biển báo ví dụ như sau: Tên biển báo 1: ... Tên biển báo 2: ..."

# Send the image to the model with system prompt
response = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",  # Hoặc model phù hợp khác
    messages=[
        {
            "role": "system",
            "content": system_prompt  # Cung cấp prompt hệ thống
        },
        {
            "role": "user",
            "content": "Cho tôi biết tên các biển báo giao thông Việt Nam trong ảnh"
        },
        {
            "role": "user",
            "content": f"image_url:{image_url}"  # Gửi URL của ảnh
        }
    ]
)

# Output the response from GPT-4
print(response.choices[0].message.content)
