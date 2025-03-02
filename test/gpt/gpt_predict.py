from openai import OpenAI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
client = OpenAI(api_key="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")

# Đường dẫn URL của ảnh đã được tải lên
image_url = "https://drive.google.com/file/uc?id=1VRACZDi1w6WPLLHJGvKgR-cftgFbN_2U"

# Prompt cho hệ thống và người dùng
system_prompt = """You are tasked with evaluating the image of product displays in a supermarket, they normaly under the same big beverage brand sold in Vietnam. 
    
    Scan every product wwith direction: rack top to down, from left to right for each rack:
    1. Identify every single product with name, size and there position in the actual display. 
    2. Provide detailed information about the product's position in the image. 
       - Include the **Rack (shelf number)**, **Row (horizontal layer)**, and **Slot (specific position within the row)** .
   
    Your output should be structured and include a table-like summary for better clarity, with the following columns:
    - Product Name with Size, either can, bottle or package
    - Actual Position (Rack, Row, Slot)(kệ, hàng, chỗ)
    Remember response in Vietnamese"""
user_prompt = "Cho tôi thông tin chi tiết về các loại đồ uống trong ảnh"

# Gửi request để dự đoán tên biển báo trong ảnh
response = client.chat.completions.create(
    model="ft:gpt-4o-2024-08-06:has::B6f3Jrit",  # muốn dùng model-finetune thì chỉ cần thay tên model, ví dụ model="ft:gpt-4o-mini:my-org:custom_suffix:id"
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
