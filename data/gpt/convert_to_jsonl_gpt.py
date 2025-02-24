import os
import json

# Prompt cho hệ thống và người dùng
system_prompt = "Bạn là AI nhận diện biển báo giao thông Việt Nam. Hãy dự đoán tên các biển báo trong ảnh, trong ảnh có thể có một hoặc nhiều biển báo. Chỉ cần nói ra tên biển báo ví dụ như sau: Tên biển báo 1: ... Tên biển báo 2: ... Nếu bạn không nhận diện được biển báo hãy trả lời 'Không nhận diện được biển báo'."
user_prompt = "Cho tôi biết tên các biển báo giao thông Việt Nam trong ảnh."

def prepare_jsonl(image_links_file, labels_folder, output_file):
    # Đọc link ảnh và tên tệp từ file txt
    with open(image_links_file, 'r', encoding='utf-8') as f:
        image_links = [line.strip().split() for line in f.readlines()]
        
    # Mở file JSONL để ghi dữ liệu huấn luyện với bộ mã hóa UTF-8
    with open(output_file, 'w', encoding='utf-8') as jsonl_file:
        for image_name, image_link in image_links:
            # Tạo đường dẫn đến file label tương ứng
            label_file_path = os.path.join(labels_folder, image_name.replace('.jpg', '.txt')
                                        .replace('.png', '.txt')
                                        .replace('.webp', '.txt'))

            # Kiểm tra nếu có file label tương ứng
            if os.path.exists(label_file_path):
                with open(label_file_path, 'r', encoding='utf-8') as label_file:
                    label = label_file.read().strip()  # Đọc nội dung nhãn từ file và loại bỏ khoảng trắng
            else:
                label = "Không có nhãn"  # Nếu không có nhãn, đánh dấu là "Không có nhãn"

            # Tạo ví dụ huấn luyện cho mỗi ảnh
            training_example = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "user", "content": [
                        {"type": "image_url", "image_url": {"url": image_link, "detail": "low"}}
                    ]},
                    {"role": "assistant", "content": label}  # Nhãn biển báo
                ]
            }

            # Ghi dữ liệu vào file JSONL
            jsonl_file.write(json.dumps(training_example, ensure_ascii=False) + "\n")

    print(f"Đã tạo file {output_file} từ dataset.")

# Gọi hàm với đường dẫn phù hợp
prepare_jsonl('data/gpt/images300_link.txt', 'data/gpt/labels_300', 'data/gpt/training_data300.jsonl')
