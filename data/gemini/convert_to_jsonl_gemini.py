# import os
# import json

# # Đường dẫn thư mục chứa ảnh và nhãn
# image_folder = "data/gemini/images"
# label_folder = "data/gemini/labels"

# # Đường dẫn file JSONL đầu ra
# jsonl_file = "data/gemini/train_data.jsonl"

# # Bucket URI trên Google Cloud Storage
# BUCKET_URI = "gs://traffic_recognition/images/"

# # Hàm tạo đường dẫn fileUri cho ảnh trên GCS
# def get_gcs_uri(filename):
#     return f"{BUCKET_URI}{filename}"

# # Tạo file JSONL
# with open(jsonl_file, "w", encoding="utf-8") as f_jsonl:
#     for filename in os.listdir(image_folder):
#         if filename.endswith(('.jpg', '.png')):
#             image_path = os.path.join(image_folder, filename)
#             label_path = os.path.join(label_folder, filename.replace(".jpg", ".txt").replace(".png", ".txt"))

#             # Kiểm tra file nhãn
#             if os.path.exists(label_path):
#                 with open(label_path, "r", encoding="utf-8") as f:
#                     label_text = f.read().strip()
#             else:
#                 label_text = "Không có nhãn"

#             # Tạo entry theo đúng format yêu cầu của Vertex AI
#             jsonl_entry = {
#                 "contents": [
#                     {
#                         "role": "user",
#                         "parts": [
#                             {
#                                 "fileData": {
#                                     "mimeType": "image/jpeg" if filename.endswith(".jpg") else "image/png",
#                                     "fileUri": get_gcs_uri(filename)
#                                 }
#                             },
#                             {
#                                 "text": "Đây là một biển báo giao thông. Hãy cho tôi biết tên của biển báo này."
#                             }
#                         ]
#                     },
#                     {
#                         "role": "model",
#                         "parts": [
#                             {
#                                 "text": label_text
#                             }
#                         ]
#                     }
#                 ]
#             }
#             f_jsonl.write(json.dumps(jsonl_entry, ensure_ascii=False) + "\n")

# print("✅ Dataset JSONL đã tạo thành công:", jsonl_file)

import os
import json
from typing import List, Dict, Any

# Đường dẫn thư mục chứa ảnh và nhãn
image_folder = "data/gemini/images"
label_folder = "data/gemini/labels"

# Đường dẫn file JSONL đầu ra
jsonl_file = "data/gemini/train_data.jsonl"

# Hàm tạo entry cho mỗi ảnh và nhãn
def create_json_entry(image_filename: str, label_filename: str) -> Dict[str, Any]:
    # Đọc nhãn từ file
    label_path = os.path.join(label_folder, label_filename)
    with open(label_path, "r", encoding="utf-8") as label_file:
        label_text = label_file.read().strip()
    
    # Tạo entry cho file ảnh
    json_entry = {
        "text_input": "Đây là một biển báo giao thông. Hãy cho tôi biết tên của biển báo này.",
        "output": label_text
    }
    
    return json_entry

# Tạo file JSONL từ ảnh và nhãn
with open(jsonl_file, "w", encoding="utf-8") as f_jsonl:
    for image_filename in os.listdir(image_folder):
        if image_filename.endswith(('.jpg', '.png')):  # Kiểm tra định dạng ảnh
            label_filename = image_filename.replace(".jpg", ".txt").replace(".png", ".txt")
            
            # Nếu file nhãn tồn tại, tạo entry cho JSONL
            if os.path.exists(os.path.join(label_folder, label_filename)):
                json_entry = create_json_entry(image_filename, label_filename)
                # Viết entry vào file JSONL
                f_jsonl.write(json.dumps(json_entry, ensure_ascii=False) + "\n")

print("✅ Dataset JSONL đã tạo thành công:", jsonl_file)
