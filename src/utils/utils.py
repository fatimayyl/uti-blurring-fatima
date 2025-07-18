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
    models = {}

    weight_name = config.get("Weights", "yolo11m.pt")
    weight_path = f"/storage/{weight_name}"

    if not os.path.exists(weight_path):
        raise FileNotFoundError(f"Model dosyası bulunamadı: {weight_path}")

    config_device = config.get("ConfigDevice", "CPU")
    device = 'cuda' if (config_device == "GPU" and torch.cuda.is_available()) else 'cpu'

    logger.info(f"YOLO modeli {device.upper()} üzerinde çalışacak.")

    model = YOLO(weight_path)
    model.to(device)

    models["model"] = model
    models["device"] = device

    return models
