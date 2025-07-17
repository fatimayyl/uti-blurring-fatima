import os
import sys
import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.BlurringFatima.src.models.PackageModel import PackageModel, CropTopOption, CropBottomOption
from components.BlurringFatima.src.utils.response import build_response_crop


class CropFatimaExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)

        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")
        self.crop_mode = self.request.get_config("CropMode")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop_image(self, img, mode):
        h, w = img.shape[:2]

        if isinstance(mode, CropTopOption):
            pixels = mode.config.value
            return img[pixels:, :]
        elif isinstance(mode, CropBottomOption):
            pixels = mode.config.value
            return img[:h - pixels, :]
        else:
            print("Unknown crop mode. Returning original image.")
            return img

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        cropped1 = self.crop_image(img1.value, self.crop_mode.value)
        cropped2 = self.crop_image(img2.value, self.crop_mode.value)

        print("Cropped1 shape:", cropped1.shape)
        print("Cropped2 shape:", cropped2.shape)

        img1_cropped = Image()
        img1_cropped.value = cropped1

        img2_cropped = Image()
        img2_cropped.value = cropped2

        self.imageOne = Image.set_frame(
            img=img1_cropped, package_uID=self.uID, redis_db=self.redis_db
        )
        self.imageTwo = Image.set_frame(
            img=img2_cropped, package_uID=self.uID, redis_db=self.redis_db
        )

        return build_response_crop(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
