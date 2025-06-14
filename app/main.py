from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.YOLO_router import yolo_router
from app.routers.GEMINI_router import gemini_router
from app.routers.GPT_router import gpt_router
from app.routers.GCS_router import gcs_router

app = FastAPI()

# Cấu hình CORS chi tiết hơn
origins = [
    "https://traffic-sign-recognition-app.web.app",
    "https://traffic-sign-recognition-9aaf9.web.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Registering the routers
app.include_router(yolo_router, prefix="/yolo")
app.include_router(gemini_router, prefix="/gemini")
app.include_router(gpt_router, prefix="/gpt")
app.include_router(gcs_router, prefix="/gcs")

@app.get("/")
async def root():
    return {"message": "Traffic Sign Recognition API is running!"}