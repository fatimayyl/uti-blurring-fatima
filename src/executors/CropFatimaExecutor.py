"""
    CropFatimaExecutor:
    Seçilen moda göre (CropTop veya CropBottom), görüntünün üstünden ya da altından kırpma işlemi yapar.
"""

import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.BlurringFatima.src.models.PackageModel import PackageModel
from components.BlurringFatima.src.utils.response import build_response_crop


class CropFatimaExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.crop_mode = self.request.get_param("CropMode")
        self.crop_top_pixels = self.request.get_param("CropTopPixels")
        self.crop_bottom_pixels = self.request.get_param("CropBottomPixels")
        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img, mode, pixels):
        height, width = img.shape[:2]
        print(f"Cropping mode: {mode}, pixels: {pixels}, image size: {img.shape}")
        if mode == "CropTop":
            return img[pixels:, :]
        elif mode == "CropBottom":
            return img[:height - pixels, :]
        else:
            return img  # mode hatalıysa işlem yapma

    def run(self):
        # Resimleri al
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        # Crop moduna göre kaç pixel kırpılacağını belirle
        if self.crop_mode == "CropTop":
            crop_pixels = self.crop_top_pixels.value if hasattr(self.crop_top_pixels, "value") else 50
        elif self.crop_mode == "CropBottom":
            crop_pixels = self.crop_bottom_pixels.value if hasattr(self.crop_bottom_pixels, "value") else 50
        else:
            print(f"[WARN] Geçersiz crop_mode: {self.crop_mode}")
            crop_pixels = 0

        crop_pixels = max(1, min(1000, int(crop_pixels)))

        # Görüntülere kırpma uygula
        img1.value = self.crop(img1.value, self.crop_mode, crop_pixels)
        img2.value = self.crop(img2.value, self.crop_mode, crop_pixels)

        # Çıktıyı Redis'e kaydet
        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        # Response dön
        return build_response_crop(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
