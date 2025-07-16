"""
    It is one of the preprocessing components in which the image is cropped from center.
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

        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

        # Sabit crop boyutları (örnek olarak 200x200)
        self.crop_width = 200
        self.crop_height = 200

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    @staticmethod
    def crop(img, crop_width, crop_height):
        height, width = img.shape[:2]
        x1 = max(0, (width - crop_width) // 2)
        y1 = max(0, (height - crop_height) // 2)
        x2 = x1 + crop_width
        y2 = y1 + crop_height
        return img[y1:y2, x1:x2]

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img1.value = self.crop(img1.value, self.crop_width, self.crop_height)
        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)

        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)
        img2.value = self.crop(img2.value, self.crop_width, self.crop_height)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        return build_response_crop(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
