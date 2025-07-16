"""
    It is one of the preprocessing components in which the image is rotated.
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
        self.request.model = PackageModel(**(self.request.data))
        self.rotation_degree = self.request.get_param("Degree")
        self.keep_side = self.request.get_param("KeepSide")
        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img):
        if isinstance(self.crop_type, str) and self.crop_type.lower() == "cropboxsize":
            return img[50:50 + self.crop_box_size, 50:50 + self.crop_box_size]
        elif isinstance(self.crop_type, str) and self.crop_type.lower() == "cropratio":
            h, w = img.shape[:2]
            new_h = int(h * self.crop_ratio)
            new_w = int(w * self.crop_ratio)
            start_y = (h - new_h) // 2
            start_x = (w - new_w) // 2
            return img[start_y:start_y + new_h, start_x:start_x + new_w]
        else:
            return img  # Geçersiz durumda orijinal döndür

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img1.value = self.crop(img1.value)
        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)

        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)
        img2.value = self.crop(img2.value)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        self.imageOne = self.imageOne
        self.imageTwo = self.imageTwo
        return build_response_crop(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
