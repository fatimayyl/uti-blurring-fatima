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
        self.crop_pixels = self.request.get_param("CropPixels")
        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def crop(self, img, mode, pixels):
        print(f"Cropping mode: {mode}, pixels: {pixels}, image size: {img.shape}")

        h, w = img.shape[:2]
        p = int(pixels)

        if mode == "CropTop":
            return img[p:, :]
        elif mode == "CropBottom":
            return img[:h - p, :]
        elif mode == "CropLeft":
            return img[:, p:]
        elif mode == "CropRight":
            return img[:, :w - p]
        else:
            print("Unknown crop mode, returning original image.")
            return img

    def run(self):
        print("crop_mode:", self.crop_mode)
        print("crop_pixels (raw):", self.crop_pixels)
        print("imageOne param:", self.imageOne)
        print("imageTwo param:", self.imageTwo)

        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        # crop_pixels güvenli dönüşümü
        if hasattr(self.crop_pixels, "value"):
            try:
                crop_pixels = int(self.crop_pixels.value)
            except Exception as e:
                print("Error converting crop_pixels.value to int:", e)
                crop_pixels = 50
        else:
            try:
                crop_pixels = int(self.crop_pixels)
            except Exception as e:
                print("Error converting crop_pixels to int:", e)
                crop_pixels = 50

        cropped1 = self.crop(img1.value, self.crop_mode, crop_pixels)
        cropped2 = self.crop(img2.value, self.crop_mode, crop_pixels)

        print("Cropped1 shape:", cropped1.shape)
        print("Cropped2 shape:", cropped2.shape)

        img1_cropped = Image()
        img1_cropped.value = cropped1

        img2_cropped = Image()
        img2_cropped.value = cropped2

        self.imageOne = Image.set_frame(
            img=img1_cropped, package_uID=self.uID, redis_db=self.redis_db
        )
        print("Set frame imageOne:", self.imageOne)

        self.imageTwo = Image.set_frame(
            img=img2_cropped, package_uID=self.uID, redis_db=self.redis_db
        )
        print("Set frame imageTwo:", self.imageTwo)

        print("imageOne is None?", self.imageOne is None)
        print("imageTwo is None?", self.imageTwo is None)

        return build_response_crop(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
