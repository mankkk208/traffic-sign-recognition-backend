# pylint: disable=no-member
import os
import base64
from fastapi import APIRouter, UploadFile, File, HTTPException
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part

# ===== 1. Cấu hình Google Cloud =====
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gen-lang-client-0788085518-6a37c52bd548.json"

PROJECT_ID = "681792955708"  # 🔹 Thay bằng ID của dự án
LOCATION = "us-central1"      # 🔹 Thay bằng location của model
ENDPOINT_ID = "7468486607738241024"  # 🔹 Thay bằng endpoint của model fine-tune

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

# ===== 4. Định nghĩa router =====
gemini_router = APIRouter()

# ===== 5. Cấu hình AI Chat =====
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

system_prompt = """
Bạn là AI chuyên nhận diện biển báo giao thông Việt Nam. Trong ảnh có thể có một hoặc nhiều biển báo giao thông Việt Nam. Hãy cho tôi biết tên của các biển báo này. Câu trả lời của bạn phải chính xác với tên chuẩn của biển báo giao thông Việt Nam.
Nếu không nhận diện được biển báo nào, hãy trả lời 'Không có biển báo'.
Câu trả lời theo format như sau: 
Biển báo 1 ..., Biển báo 2 ..., Biển báo 3 ..., ...
"""

@gemini_router.post("/predict/")
async def predict_gemini(file: UploadFile = File(...)):
    try:
        # ===== 6. Đọc ảnh từ file và mã hóa thành Base64 =====
        image_bytes = await file.read()

        # ===== 7. Gửi ảnh đến model để dự đoán =====
        chat = model.start_chat()
        response = chat.send_message([
            Part.from_text(system_prompt),
            Part.from_data(image_bytes, mime_type="image/jpeg"),
        ], generation_config=generation_config, safety_settings=safety_settings)

        # ===== 8. Kiểm tra kết quả và trả về =====
        if response.text:
            return {"predicted_sign": response.text}
        else:
            raise HTTPException(status_code=400, detail="Không có dự đoán nào được trả về từ Gemini AI")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
