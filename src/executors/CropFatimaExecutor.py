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
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        crop_pixels = (
            self.crop_pixels.value
            if hasattr(self.crop_pixels, "value")
            else 50  # default value
        )

        cropped1 = self.crop(img1.value, self.crop_mode, crop_pixels)
        cropped2 = self.crop(img2.value, self.crop_mode, crop_pixels)

        print("Cropped1 shape:", cropped1.shape)
        print("Cropped2 shape:", cropped2.shape)

        # Image nesnesine sar
        img1_cropped = Image(value=cropped1)
        img2_cropped = Image(value=cropped2)

        # Redis'e kaydet
        self.imageOne = Image.set_frame(
            img=img1_cropped, package_uID=self.uID, redis_db=self.redis_db
        )
        self.imageTwo = Image.set_frame(
            img=img2_cropped, package_uID=self.uID, redis_db=self.redis_db
        )

        print("imageOne is None?", self.imageOne is None)
        print("imageTwo is None?", self.imageTwo is None)

        return build_response_crop(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
