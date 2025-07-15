"""
    It is one of the preprocessing components in which the image is zoomed.
    Zooms into the center of the image by a zoom factor.
        zoom_factor > 1 → Zoom in
        zoom_factor < 1 → Zoom out
"""

import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.BlurringFatima.src.models.PackageModel import PackageModel
from components.BlurringFatima.src.utils.response import build_response_zoom



class ZoomFatimaExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**self.request.data)


        self.zoom_mode = self.request.get_param("ZoomMode")
        self.zoom_in_factor = self.request.get_param("ZoomInFactor")
        self.zoom_out_factor = self.request.get_param("ZoomOutFactor")
        self.imageOne = self.request.get_param("inputImageOne")
        self.imageTwo = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def zoom(self, img, zoom_factor):
        """
        Zooms into the center of the image by a zoom factor.
        zoom_factor > 1 → Zoom in
        zoom_factor < 1 → Zoom out
        """

        height, width = img.shape[:2]

        new_width = max(1, int(width / zoom_factor))
        new_height = max(1, int(height / zoom_factor))

        x1 = (width - new_width) // 2
        y1 = (height - new_height) // 2
        x2 = x1 + new_width
        y2 = y1 + new_height

        cropped = img[y1:y2, x1:x2]
        zoomed = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LINEAR)

        return zoomed

    def run(self):
        img1 = Image.get_frame(img=self.imageOne, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.imageTwo, redis_db=self.redis_db)

        if self.zoom_mode.value == "ZoomIn":
            zoom_factor = self.zoom_in_factor.value
        else:
            zoom_factor = self.zoom_out_factor.value

        img1.value = self.zoom(img1.value, zoom_factor=zoom_factor)
        img2.value = self.zoom(img2.value, zoom_factor=zoom_factor)

        self.imageOne = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.imageTwo = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)

        packageModel = build_response_zoom(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
