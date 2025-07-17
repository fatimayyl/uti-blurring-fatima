"""
    It is one of the preprocessing components in which the image is cropped.
    Crops from top or bottom by a given pixel amount.
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
        h, w = img.shape[:2]
        if mode == "CropTop":
            return img[pixels:, :]
        elif mode == "CropBottom":
            return img[:h - pixels, :]
        return img

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        if self.crop_mode == "CropTop":
            crop_pixels = self.crop_top_pixels.value if hasattr(self.crop_top_pixels, "value") else 50
        else:
            crop_pixels = self.crop_bottom_pixels.value if hasattr(self.crop_bottom_pixels, "value") else 50

        crop_pixels = max(1, min(1000, int(crop_pixels)))

        img1.value = self.crop(img1.value, self.crop_mode, crop_pixels)
        img2.value = self.crop(img2.value, self.crop_mode, crop_pixels)

        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        return build_response_crop(context=self)

if __name__ == "__main__":
    Executor(sys.argv[1]).run()
