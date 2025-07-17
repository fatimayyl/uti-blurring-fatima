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

        crop_mode_obj = self.request.get_param("CropMode")
        self.crop_mode = crop_mode_obj.get("value") if isinstance(crop_mode_obj, dict) else crop_mode_obj

        self.crop_top_pixels = crop_mode_obj.get("config", {}).get("CropTopPixels", {}).get("value") \
            if self.crop_mode == "CropTop" else None

        self.crop_bottom_pixels = crop_mode_obj.get("config", {}).get("CropBottomPixels", {}).get("value") \
            if self.crop_mode == "CropBottom" else None

        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img, crop_mode, top_px, bottom_px):
        height, width = img.shape[:2]
        if crop_mode == "CropTop" and top_px:
            print(f"Cropping TOP: {top_px}px")
            return img[int(top_px):, :]
        elif crop_mode == "CropBottom" and bottom_px:
            print(f"Cropping BOTTOM: {bottom_px}px")
            return img[:height - int(bottom_px), :]
        print("NO CROP applied")
        return img

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        top_px = (
            self.crop_top_pixels.value
            if self.crop_mode == "CropTop" and hasattr(self.crop_top_pixels, "value")
            else None
        )

        bottom_px = (
            self.crop_bottom_pixels.value
            if self.crop_mode == "CropBottom" and hasattr(self.crop_bottom_pixels, "value")
            else None
        )

        print("MODE:", self.crop_mode)
        print("TOP:", top_px)
        print("BOTTOM:", bottom_px)

        img1.value = self.crop(img1.value, self.crop_mode, top_px, bottom_px)
        img2.value = self.crop(img2.value, self.crop_mode, top_px, bottom_px)

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