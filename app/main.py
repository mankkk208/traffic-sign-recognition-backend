from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.CNN_router import cnn_router
from app.routers.YOLO_router import yolo_router
from app.routers.GEMINI_router import gemini_router
from app.routers.GPT_router import gpt_router
from app.routers.GCS_router import gcs_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các domain. Bạn có thể thay "*" bằng các domain cụ thể nếu cần.
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các headers
)

# Registering the routers for CNN and YOLO
app.include_router(cnn_router, prefix="/cnn")
app.include_router(yolo_router, prefix="/yolo")
app.include_router(gemini_router, prefix="/gemini")
app.include_router(gpt_router, prefix="/gpt")
app.include_router(gcs_router, prefix="/gcs")


@app.get("/")
async def root():
    return {"message": "Traffic Sign Recognition API is running!"}