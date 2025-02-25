from openai import OpenAI
import time
from src.config import GPT_API_KEY
client = OpenAI(api_key=GPT_API_KEY)

def check_fine_tuning_status(job_id):
    # Lấy trạng thái của fine-tuning job
    job_status = client.fine_tuning.jobs.retrieve(job_id)
    print(f"Fine-tuning job status: {job_status.status}")  # Accessing status with dot notation

    # Đợi job hoàn thành rồi lấy mô hình fine-tuned
    while job_status.status not in ['succeeded', 'failed']:  # Accessing status with dot notation
        print("Đang chờ job hoàn thành...")
        time.sleep(10)  # Kiểm tra lại sau 10 giây
        job_status = client.fine_tuning.jobs.retrieve(job_id)
    
    if job_status.status == 'succeeded':  # Accessing status with dot notation
        fine_tuned_model = job_status.fine_tuned_model  # Accessing fine_tuned_model with dot notation
        print(f"Mô hình fine-tuned đã sẵn sàng: {fine_tuned_model}")
    else:
        error_message = job_status.error # Lấy thông điệp lỗi từ trường 'error'
        print(f"Fine-tuning job thất bại. Lý do: {error_message}")

if __name__ == "__main__":
    job_id = "ftjob-9I4JVLwo2KlvLsQH6xBehm53"  # Thay thế bằng ID job của bạn
    check_fine_tuning_status(job_id)
