import os
import sys
import torch
from ultralytics import YOLO

# PYTHONPATH ayarları
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from sdks.novavision.src.base.model import BoundingBox
from sdks.novavision.src.helper.executor import Executor

from components.BlurringFatima.src.utils.utils import load_models
from components.BlurringFatima.src.utils.response import build_response
from components.BlurringFatima.src.models.PackageModel import PackageModel, Detection


class TransportDetection(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        # Giriş parametreleri
        self.image = self.request.get_param("inputImage")
        self.device = self.request.get_param("ConfigDevice")
        self.conf_thres = float(self.request.get_param("ConfidentThreshold"))
        self.iou_thres = float(self.request.get_param("IOUThreshold"))

        # Model ve cihaz
        self.weight = self.bootstrap.get("model")  # YOLO model objesi
        self.select_device = self.bootstrap.get("device")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        """
        YOLO modelini ve device'ı yükleyen fonksiyon.
        """
        model = load_models(config=config)  # utils.py içindeki load_models çağrısı
        return model

    def output_result(self, results, img_uid):
        """
        YOLO çıktısını Detection listesine dönüştürür.
        """
        detection_list = []
        for r in results:
            for box in r.boxes:
                bbox = BoundingBox(
                    left=float(box.xyxy[0][0]),
                    top=float(box.xyxy[0][1]),
                    width=float(box.xyxy[0][2] - box.xyxy[0][0]),
                    height=float(box.xyxy[0][3] - box.xyxy[0][1])
                )
                newdetect = Detection(
                    boundingBox=bbox,
                    confidence=float(box.conf[0]),
                    classLabel=self.weight.names[int(box.cls[0])],
                    classId=int(box.cls[0]),
                    imgUID=img_uid
                )
                detection_list.append(newdetect)
        return detection_list

    def transport_inference(self):
        """
        YOLO modelinde tahmin çalıştırır.
        """
        results = self.weight.predict(
            self.image.value,
            conf=self.conf_thres,
            iou=self.iou_thres,
            device=self.select_device,
            verbose=False
        )
        output_detection_list = self.output_result(results, self.image.uID)
        return output_detection_list

    def run(self):
        """
        Executor'un ana çalıştırma fonksiyonu.
        """
        self.image = Image.get_frame(img=self.image, redis_db=self.redis_db)
        self.detection = self.transport_inference()
        packageModel = build_response(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
