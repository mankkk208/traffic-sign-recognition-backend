# pylint: disable=no-member
import os
import json
import google.generativeai as genai
from typing import List, Dict, Any
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Lenovo\Desktop\gen-lang-client-0788085518-6a37c52bd548.json"

# Cấu hình API key
GOOGLE_API_KEY = "AIzaSyDqUFWRlnWrNZVrAT56GHmnYcBnICVe-xE"
genai.configure(api_key=GOOGLE_API_KEY)

def read_jsonl(file_path: str) -> List[Dict[str, Any]]:
    """Đọc file JSONL và trả về danh sách các dictionary."""
    data = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line.strip()))
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File không tìm thấy: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ Lỗi giải mã JSON: {e}")
    return data

# Đọc dữ liệu từ file JSONL
jsonl_file = "data/gemini/train_data.jsonl"
raw_data = read_jsonl(jsonl_file)

# Kiểm tra dữ liệu và chuẩn bị cho huấn luyện
training_data = []
for item in raw_data:
    # Trực tiếp lấy text_input và output từ JSONL
    if "text_input" in item and "output" in item:
        training_data.append({
            "text_input": item["text_input"],  # Câu hỏi của người dùng
            "output": item["output"]           # Đáp án từ mô hình (label)
        })

# Kiểm tra nếu dữ liệu huấn luyện không trống
if not training_data:
    raise ValueError("❌ Dữ liệu huấn luyện không được để trống.")

# 🚀 Khởi tạo quá trình fine-tune (nếu API hỗ trợ)
try:
    tuning_job = genai.create_tuned_model(
        source_model="models/gemini-1.5-flash-001-tuning",  # Chọn mô hình gốc
        training_data=training_data,  # Dữ liệu huấn luyện
        id="traffic-sign-tuned-model-7",  # ID mô hình fine-tune phải hợp lệ (chỉ sử dụng chữ thường, số và dấu gạch ngang)
        display_name="Traffic Sign Fine-Tuned Model",  # Tên hiển thị
        epoch_count=5,  # Số epoch
        batch_size=4,  # Kích thước batch
        learning_rate=0.001,  # Tốc độ học
    )
    
    # Đợi cho đến khi quá trình fine-tuning hoàn tất và nhận thông tin về mô hình
    tuning_job_result = tuning_job.result(timeout=72000)  # Thêm timeout để tránh lâu quá thời gian mặc định
    
    # In thông tin về mô hình đã được fine-tune
    print("✅ Fine-tuning completed... Model ID:", tuning_job_result)

except TimeoutError as e:
    print(f"❌ Lỗi timeout: {e}")
except Exception as e:
    print(f"❌ Lỗi không xác định: {e}")