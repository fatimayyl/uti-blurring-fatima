import os
import sys
import torch
from ultralytics import YOLO

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from sdks.novavision.src.helper.executor import Executor

# from components.BlurringFatima.src.utils.utils import load_models
from components.BlurringFatima.src.utils.response import build_response_transport
from components.BlurringFatima.src.models.PackageModel import PackageModel


class TransportDetection(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.image = self.request.get_param("inputImage")

        # self.weight = self.bootstrap["model"]

    """
    @staticmethod
    def bootstrap(config: dict) -> dict:
        model = load_models(config=config)  # utils.py içindeki load_models çağrısı
        return {"model": model}

    """

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        """
        Executor'un ana çalıştırma fonksiyonu.
        """
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response_transport(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
