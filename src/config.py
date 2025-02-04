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
    "Speed limit (20km/h)", "Speed limit (30km/h)", "Speed limit (50km/h)",
    "Speed limit (60km/h)", "Speed limit (70km/h)", "Speed limit (80km/h)",
    "End of speed limit (80km/h)", "Speed limit (100km/h)", "Speed limit (120km/h)",
    "No passing", "No passing for vehicles over 3.5 tons", "Right-of-way at the next intersection",
    "Priority road", "Yield", "Stop", "No vehicles",
    "Vehicles over 3.5 tons prohibited", "No entry", "General caution",
    "Dangerous curve to the left", "Dangerous curve to the right", "Double curve",
    "Bumpy road", "Slippery road", "Road narrows on the right", "Road work",
    "Traffic signals", "Pedestrians", "Children crossing", "Bicycles crossing",
    "Beware of ice/snow", "Wild animals crossing", "End of all speed and passing limits",
    "Turn right ahead", "Turn left ahead", "Ahead only", "Go straight or right",
    "Go straight or left", "Keep right", "Keep left", "Roundabout mandatory",
    "End of no passing", "End of no passing by vehicles over 3.5 tons"
]