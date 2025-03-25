import os
from PIL import Image, ExifTags, ImageFile

# Cho phép Pillow xử lý ảnh bị thiếu dữ liệu
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Thư mục chứa ảnh
folder_path = r"C:\Users\Lenovo\Desktop\817\BienBaoS4_3"
# folder_path = "data/gemini/images"

# Lấy danh sách file ảnh có định dạng hợp lệ
valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
image_files.sort()  # Sắp xếp thứ tự file

# Nhập số bắt đầu và kết thúc
start_num = int(input("Nhập số bắt đầu: "))  # Ví dụ: 1
end_num = start_num + len(image_files) - 1  # Tính toán số kết thúc tự động

# Kiểm tra nếu số file không đủ
if len(image_files) < (end_num - start_num + 1):
    print("⚠️ Số lượng file không đủ để đổi tên theo yêu cầu!")
    exit()

def correct_orientation(image):
    """ Kiểm tra và xoay ảnh nếu có thông tin Exif về Orientation """
    try:
        exif = image._getexif()
        if exif:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == "Orientation":
                    if value == 3:
                        return image.rotate(180, expand=True)
                    elif value == 6:
                        return image.rotate(270, expand=True)  # Xoay phải 90 độ
                    elif value == 8:
                        return image.rotate(90, expand=True)  # Xoay trái 90 độ
        return image
    except Exception:
        return image  # Nếu có lỗi, trả về ảnh gốc

# Đổi tên & chuyển đổi ảnh sang JPG
for idx, filename in enumerate(image_files, start=start_num):
    old_path = os.path.join(folder_path, filename)
    #new_name = f"{idx:05d}.jpg"  # Định dạng mới: 00001.jpg, 00002.jpg, ...
    new_name = f"test_{idx:05d}.jpg"
    new_path = os.path.join(folder_path, new_name)

    try:
        # Mở ảnh và xử lý xoay nếu cần
        with Image.open(old_path) as img:
            img = correct_orientation(img)
            rgb_img = img.convert("RGB")  # Chuyển về RGB để tránh lỗi
            rgb_img.save(new_path, "JPEG", quality=95)

        # Xóa file cũ sau khi lưu thành công
        if old_path != new_path:
            os.remove(old_path)
            print(f"✅ Chuyển & đổi tên: {filename} -> {new_name} (Đã xóa ảnh cũ)")

    except Exception as e:
        print(f"❌ Lỗi khi xử lý {filename}: {e}")

print("\n🎉 Hoàn tất chuyển đổi và đổi tên ảnh!")
