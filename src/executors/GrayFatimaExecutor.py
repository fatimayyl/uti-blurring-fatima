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
from components.BlurringFatima.src.utils.response import build_response_gray
from components.BlurringFatima.src.models.PackageModel import PackageModel


class GrayFatimaExecutor(Component):
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

    def gray(self,img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img1.value = self.gray(img1.value)
        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)

        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)
        img2.value = self.gray(img2.value)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        self.image_one = self.imageOne
        self.image_two = self.imageTwo
        return build_response_gray(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
