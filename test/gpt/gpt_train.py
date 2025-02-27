import os
import sys

from openai import OpenAI

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')))

client = OpenAI(api_key="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")

# Upload file dữ liệu huấn luyện (training data)
file_path = "app/data/gpt/training_data300.jsonl"

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
    integrations=[
        {
            "type": "wandb",
            "wandb": {
                "project": "OpenAI",
                "tags": ["openai"]
            }
        }
    ]
)

print(f"Fine-tuning job created: {fine_tune_job.id}")
