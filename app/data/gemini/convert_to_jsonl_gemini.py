import os
import json

# Đường dẫn thư mục chứa ảnh và nhãn
image_folder = "app/data/gemini/ChatData/images800"
label_folder = "app/data/gemini/ChatData/labels"

# Đường dẫn file JSONL đầu ra
jsonl_file = "app/data/gemini/train_data_800.jsonl"

# Tạo thư mục nếu chưa tồn tại
os.makedirs(os.path.dirname(jsonl_file), exist_ok=True)

# Bucket URI trên Google Cloud Storage
BUCKET_URI = "gs://traffic_recognition/images800/"

# Hàm tạo đường dẫn fileUri cho ảnh trên GCS
def get_gcs_uri(filename):
    return f"{BUCKET_URI}{filename}"

# Tạo file JSONL
with open(jsonl_file, "w", encoding="utf-8") as f_jsonl:
    for filename in os.listdir(image_folder):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(image_folder, filename)
            label_path = os.path.join(label_folder, filename.replace(".jpg", ".txt").replace(".png", ".txt"))

            # Kiểm tra file nhãn
            if os.path.exists(label_path):
                with open(label_path, "r", encoding="utf-8") as f:
                    label_text = f.read().strip()
            else:
                label_text = "Không có nhãn"

            # Tạo entry theo đúng format yêu cầu của Vertex AI
            jsonl_entry = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "fileData": {
                                    "mimeType": "image/jpeg" if filename.endswith(".jpg") else "image/png",
                                    "fileUri": get_gcs_uri(filename)
                                }
                            },
                            {
                                "text": "Bạn là AI chuyên nhận diện biển báo giao thông Việt Nam. Trong ảnh có thể có một hoặc nhiều biển báo giao thông Việt Nam. Hãy cho tôi biết tên của các biển báo này. Câu trả lời của bạn phải chính xác với tên chuẩn của biển báo giao thông Việt Nam. Nếu không nhận diện được biển báo nào, hãy trả lời 'Không có biển báo'. Câu trả lời theo format như sau: Biển báo 1 ..., Biển báo 2 ..., Biển báo 3 ..."
                            }
                        ]
                    },
                    {
                        "role": "model",
                        "parts": [
                            {
                                "text": label_text
                            }
                        ]
                    }
                ]
            }
            f_jsonl.write(json.dumps(jsonl_entry, ensure_ascii=False) + "\n")

print("✅ Dataset JSONL đã tạo thành công:", jsonl_file)
