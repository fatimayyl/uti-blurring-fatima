import os
import torch
from ultralytics import YOLO
from sdks.novavision.src.base.logger import LoggerManager
from sdks.novavision.src.base.application import Application

logger = LoggerManager()
application = Application()

# Model yolunu sabit tanımlıyoruz
MODEL_PATH = "/storage/yolo11m.pt"

def load_models(config: dict):

    if os.path.isfile(MODEL_PATH):
        model = YOLO(MODEL_PATH)
        print("Model başarıyla yüklendi.")
    else:
        raise FileNotFoundError(f"Model dosyası bulunamadı: {MODEL_PATH}")

    return model
