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
from components.BlurringFatima.src.utils.response import build_response_crop
from components.BlurringFatima.src.models.PackageModel import PackageModel


class CropFatimaExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        # Config parametreleri doğrudan alınır (Zoom ile uyumlu)
        self.crop_mode = self.request.get_param("CropMode")  # "CropTop" veya "CropBottom"
        self.crop_top_pixels = self.request.get_param("CropTopPixels")
        self.crop_bottom_pixels = self.request.get_param("CropBottomPixels")

        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img, crop_mode, top_px, bottom_px):
        height, width = img.shape[:2]
        if crop_mode == "CropTop" and top_px is not None:
            return img[int(top_px):, :]
        elif crop_mode == "CropBottom" and bottom_px is not None:
            return img[:height - int(bottom_px), :]
        return img  # hiçbir kırpma yapılmaz

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        img1.value = self.crop(img1.value, self.crop_mode, self.crop_top_pixels, self.crop_bottom_pixels)
        img2.value = self.crop(img2.value, self.crop_mode, self.crop_top_pixels, self.crop_bottom_pixels)

        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        return build_response_crop(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
