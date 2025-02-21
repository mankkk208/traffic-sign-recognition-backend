from google.cloud import storage
import os

# ===== 1. Cấu hình Google Cloud =====
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Lenovo\Desktop\gen-lang-client-0788085518-6a37c52bd548.json"

# Khởi tạo client GCS
def get_gcs_client():
    return storage.Client()

# Upload file lên GCS
def upload_to_gcs(bucket_name: str, source_file_name: str, destination_blob_name: str) -> str:
    try:
        print(f"Starting upload of {source_file_name} to GCS...")
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload file
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name}.")
        
        # Make file public (optional, only necessary if you need a public URL)
        blob.make_public()  # Chỉ làm tệp công khai nếu cần
        gcs_url = blob.public_url
        print(f"File public URL: {gcs_url}")
        
        return gcs_url
    except Exception as e:
        print(f"Lỗi khi upload file lên GCS: {e}")
        return None

# Xóa file từ GCS
def delete_from_gcs(bucket_name: str, blob_name: str) -> bool:
    """Xóa file khỏi Google Cloud Storage."""
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Kiểm tra file có tồn tại không
        if not blob.exists():
            print(f"⚠️ File {blob_name} không tồn tại trên GCS.")
            return False

        # Xóa file
        blob.delete()
        print(f"✅ File {blob_name} deleted from GCS.")
        return True

    except Exception as e:
        print(f"❌ Lỗi khi xóa file trên GCS: {e}")
        return False
