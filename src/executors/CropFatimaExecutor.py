"""
    It is one of the preprocessing components in which the image is cropped from top or bottom.
"""

import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.BlurringFatima.src.models.PackageModel import PackageModel


class CropFatimaExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        # Crop config verilerini al
        crop_mode_obj = self.request.get_param("CropMode")

        if isinstance(crop_mode_obj, str):
            self.crop_mode = crop_mode_obj
            self.crop_top_pixels = self.request.get_param("CropTopPixels")
            self.crop_bottom_pixels = self.request.get_param("CropBottomPixels")

        elif isinstance(crop_mode_obj, dict):
            self.crop_mode = crop_mode_obj.get("value")
            config = crop_mode_obj.get("config", {})
            self.crop_top_pixels = config.get("CropTopPixels", {}).get("value") if self.crop_mode == "CropTop" else None
            self.crop_bottom_pixels = config.get("CropBottomPixels", {}).get("value") if self.crop_mode == "CropBottom" else None

        else:
            self.crop_mode = None
            self.crop_top_pixels = None
            self.crop_bottom_pixels = None

        # Giriş görüntüleri
        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img, crop_mode, top_px, bottom_px):
        height, width = img.shape[:2]
        if crop_mode == "CropTop" and top_px:
            print(f"🟡 Cropping from top: {top_px}px")
            return img[int(top_px):, :]
        elif crop_mode == "CropBottom" and bottom_px:
            print(f"🟡 Cropping from bottom: {bottom_px}px")
            return img[:height - int(bottom_px), :]
        print("⚠️ No crop applied")
        return img

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        print("🔧 CROP MODE:", self.crop_mode)
        print("🔧 TOP PIXELS:", self.crop_top_pixels)
        print("🔧 BOTTOM PIXELS:", self.crop_bottom_pixels)

        img1.value = self.crop(img1.value, self.crop_mode, self.crop_top_pixels, self.crop_bottom_pixels)
        img2.value = self.crop(img2.value, self.crop_mode, self.crop_top_pixels, self.crop_bottom_pixels)

        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        return {
            "outputs": {
                "outputImageOne": self.imageOne,
                "outputImageTwo": self.imageTwo
            }
        }


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
