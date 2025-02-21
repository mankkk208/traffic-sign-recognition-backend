from openai import OpenAI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.config import GPT_API_KEY
client = OpenAI(api_key=GPT_API_KEY)

# Upload file dữ liệu huấn luyện (training data)
file_path = "data/gpt/training_data300.jsonl"

# truy câp vào Files API
files = client.files

with open(file_path, 'rb') as f:  # Open file in binary mode
    file = client.files.create(
        file=f,
        purpose='fine-tune'
    )

# Get the file ID from the FileObject
file_id = file.id  # Accessing the id attribute directly

# Tạo fine-tuning job with the file ID
fine_tune_job = client.fine_tuning.jobs.create(
    training_file=file_id,  # Use the file ID here
    model="gpt-4o-2024-08-06",  # Ensure this is the correct model ID
)

print(f"Fine-tuning job created: {fine_tune_job.id}")
