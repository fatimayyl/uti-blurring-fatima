import os
import sys
import torch

sys.path.append('/opt/project/capsules/Yolov5/src/lib/yolov5')

from sdks.novavision.src.base.download import Download
from sdks.novavision.src.base.logger import LoggerManager
from sdks.novavision.src.base.application import Application
from capsules.Yolov5.src.lib.yolov5.models.common import DetectMultiBackend
from capsules.Yolov5.src.lib.yolov5.utils.torch_utils import select_device

# Logger ve Application instance
logger = LoggerManager()
application = Application()

# Transport model için Google Drive URL'si
# (Buraya kendi weight dosyanın drive linkini koy)
weight_url = "https://drive.google.com/file/d/TRANSPORT_MODEL_ID/view?usp=sharing"


def download_weights(url: str, weight_name: str) -> str:
    """
    Model ağırlıklarını (weights) Google Drive'dan indirir.
    /storage/{weight_name} yoluna kaydeder.
    """
    weight_path = f"/storage/{weight_name}"

    if not os.path.exists(weight_path):
        logger.info(f"TransportDetection - Model ({weight_name}) indiriliyor...")
        if Download.download_from_drive(url, weight_path) is None:
            logger.error(f"TransportDetection - Model ({weight_name}) indirilemedi!")
        else:
            logger.info(f"TransportDetection - Model ({weight_name}) başarıyla indirildi.")

    return weight_path


def load_models(config: dict):
    """
    TransportDetection için modeli yükler ve gerekli ayarları yapar.
    """
    models = {}

    # Weight parametresini al
    weight = application.get_param(config=config, name="Weights")
    weight_path = download_weights(url=weight_url, weight_name=weight)

    # Cihaz seçimi (GPU varsa ve seçildiyse kullan)
    config_device = application.get_param(config=config, name="ConfigDevice")
    device = select_device('cuda:0' if config_device == "GPU" and torch.cuda.is_available() else 'cpu')

    # Modeli yükle
    if config_device == "GPU" and torch.cuda.is_available():
        if application.get_param(config=config, name="Half"):
            model = DetectMultiBackend(weight_path, device=device, fp16=True)
        else:
            model = DetectMultiBackend(weight_path, device=device, fp16=False)
    else:
        model = DetectMultiBackend(weight_path, device=device, fp16=False)

    models["model"] = model
    models["device"] = device
    return models
