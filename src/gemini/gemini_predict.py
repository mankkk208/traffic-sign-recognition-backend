# pylint: disable=no-member
import os
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

# ===== 1. Cấu hình Google Cloud =====
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Lenovo\Desktop\gen-lang-client-0788085518-6a37c52bd548.json"

PROJECT_ID = "681792955708"  # 🔹 ID của dự án
LOCATION = "us-central1"      # 🔹 Location của model
ENDPOINT_ID = "7017585685280325632"  # 🔹 Endpoint của model fine-tune

# ===== 2. Khởi tạo Vertex AI =====
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    api_endpoint=f"{LOCATION}-aiplatform.googleapis.com"
)

# ===== 3. Khởi tạo model đã fine-tune =====
model = GenerativeModel(
    f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}"
)

# ===== 4. Cấu hình AI Chat =====
chat = model.start_chat()

# Cấu hình cho output
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Cấu hình safety (tắt chặn nội dung)
safety_settings = [
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=SafetySetting.HarmBlockThreshold.OFF),
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=SafetySetting.HarmBlockThreshold.OFF),
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=SafetySetting.HarmBlockThreshold.OFF),
    SafetySetting(category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=SafetySetting.HarmBlockThreshold.OFF),
]

# ===== 5. Đọc ảnh và mã hóa thành Base64 =====
image_path = "data/gemini/images/00018.jpg"  # 🔹 Thay đường dẫn ảnh nếu cần
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")  # Encode ảnh thành Base64

# ===== 6. Gửi yêu cầu nhận diện biển báo =====
response = chat.send_message([
    Part.from_text("Bạn là AI nhận diện biển báo giao thông Việt Nam. Hãy dự đoán tên các biển báo trong ảnh, trong ảnh có thể có một hoặc nhiều biển báo. Chỉ cần nói ra tên biển báo"),
    Part.from_data(image_bytes, mime_type="image/jpeg"),
], generation_config=generation_config, safety_settings=safety_settings)

# ===== 7. In kết quả dự đoán =====
print(response.text)
