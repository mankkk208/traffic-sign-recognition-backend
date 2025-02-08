import os

# Thư mục gốc
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Các paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# Model parameters
INPUT_SHAPE = (32, 32, 3)
NUM_CLASSES = 43
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.0001

# Define class names (if not loading from a CSV)
CLASS_NAMES = [
    "Giới hạn tốc độ (20km/h)",
    "Giới hạn tốc độ (30km/h)",
    "Giới hạn tốc độ (50km/h)",
    "Giới hạn tốc độ (60km/h)",
    "Giới hạn tốc độ (70km/h)",
    "Giới hạn tốc độ (80km/h)",
    "Hết giới hạn tốc độ (80km/h)",
    "Giới hạn tốc độ (100km/h)",
    "Giới hạn tốc độ (120km/h)",
    "Cấm vượt",
    "Cấm vượt đối với xe trên 3.5 tấn",
    "Quyền ưu tiên tại giao lộ tiếp theo",
    "Đường ưu tiên",
    "Nhường đường",
    "Dừng lại",
    "Cấm xe",
    "Cấm xe trên 3.5 tấn",
    "Cấm vào",
    "Cảnh báo chung",
    "Đường cong nguy hiểm bên trái",
    "Đường cong nguy hiểm bên phải",
    "Đường cong kép",
    "Đường gồ ghề",
    "Đường trơn",
    "Đường hẹp bên phải",
    "Công trường",
    "Tín hiệu giao thông",
    "Người đi bộ",
    "Trẻ em qua đường",
    "Xe đạp qua đường",
    "Cẩn thận băng/ tuyết",
    "Động vật hoang dã qua đường",
    "Hết tất cả giới hạn tốc độ và cấm vượt",
    "Rẽ phải phía trước",
    "Rẽ trái phía trước",
    "Chỉ đi thẳng",
    "Đi thẳng hoặc rẽ phải",
    "Đi thẳng hoặc rẽ trái",
    "Giữ bên phải",
    "Giữ bên trái",
    "Vòng xuyến bắt buộc",
    "Hết cấm vượt",
    "Hết cấm vượt đối với xe trên 3.5 tấn"
]