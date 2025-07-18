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
    """
    YOLO modelini yükler ve config parametrelerine göre hazırlar.
    """
    models = {}

    # MODEL_PATH kontrolü
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model dosyası bulunamadı: {MODEL_PATH}")

    # Cihaz seçimi (GPU varsa onu kullan)
    config_device = application.get_param(config=config, name="ConfigDevice", default="CPU")
    device = 'cuda' if (config_device == "GPU" and torch.cuda.is_available()) else 'cpu'
    logger.info(f"YOLO modeli {device.upper()} üzerinde çalışacak.")

    # YOLO modelini yükle
    model = YOLO(MODEL_PATH)
    model.to(device)

    models["model"] = model
    models["device"] = device

    return models
