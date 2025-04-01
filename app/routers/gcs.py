from google.cloud import storage
import os
import io

# ===== 1. Cấu hình Google Cloud =====
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "app/gen-lang-client-0788085518-6a37c52bd548.json"

# Khởi tạo client GCS
def get_gcs_client():
    return storage.Client()

# Upload file lên GCS
def upload_to_gcs(bucket_name: str, file_stream: io.BytesIO, destination_blob_name: str) -> str:
    try:
        print(f"Starting upload of {destination_blob_name} to GCS...")
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload file từ stream thay vì file trên ổ đĩa
        blob.upload_from_file(file_stream, rewind=True)  # rewind=True đảm bảo bắt đầu đọc từ đầu file

        print(f"File {destination_blob_name} uploaded to GCS.")
        
        # Make file public (nếu cần)
        blob.make_public()
        gcs_url = blob.public_url
        print(f"File public URL: {gcs_url}")
        
        return gcs_url
    except Exception as e:
        print(f"Lỗi khi upload file lên GCS: {e}")
        return None
