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

        # Config üzerinden crop tipi ve piksel değeri alınıyor
        self.crop_type = self.request.model.configs.cropMode.value
        self.crop_pixels = self.request.model.configs.cropMode.config.value

        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def crop(img, crop_type, crop_pixels):
        height, width = img.shape[:2]
        if crop_type == "CropTop":
            return img[crop_pixels:, :]
        elif crop_type == "CropBottom":
            return img[:height - crop_pixels, :]
        return img  # default: no crop

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img1.value = self.crop(img1.value, self.crop_type, self.crop_pixels)
        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)

        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)
        img2.value = self.crop(img2.value, self.crop_type, self.crop_pixels)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        return build_response_crop(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
