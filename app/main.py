from fastapi import FastAPI
from app.routers.CNN_router import cnn_router
from app.routers.YOLO_router import yolo_router

app = FastAPI()

# Registering the routers for CNN and YOLO
app.include_router(cnn_router, prefix="/cnn")
app.include_router(yolo_router, prefix="/yolo")

@app.get("/")
async def root():
    return {"message": "Traffic Sign Recognition API is running!"}