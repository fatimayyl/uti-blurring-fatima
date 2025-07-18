import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
sys.path.append('/opt/project/capsules/Yolov5/src/lib/yolov5')

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.capsule import Capsule
from sdks.novavision.src.base.model import BoundingBox
from sdks.novavision.src.helper.executor import Executor
from components.Yolov5.src.classes.yolov5_detect import Yolov5Detect
from components.BlurringFatima.src.utils.utils import load_models
from components.BlurringFatima.src.utils.response import build_response
from components.BlurringFatima.src.models.PackageModel import PackageModel, Detection


class TransportDetection(Capsule):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image = self.request.get_param("inputImage")
        self.device = self.request.get_param("ConfigDevice")
        self.select_device = bootstrap["device"]
        self.conf_thres = self.request.get_param("ConfidentThreshold")
        self.iou_thres = self.request.get_param("IOUThreshold")
        self.weight = self.bootstrap.get("model")  # Airplane-Car-Bike model weights
        self.select_device = self.bootstrap.get("device")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        model = load_models(config=config)  # Transport detection model loader
        return model

    def output_result(self, output, names, img_uid):
        output = output[0].cpu().numpy()
        detection_list = []
        for i in range(0, len(output)):
            bbox = BoundingBox(
                left=output[i][0],
                top=output[i][1],
                width=output[i][2] - output[i][0],
                height=output[i][3] - output[i][1]
            )
            newdetect = Detection(
                boundingBox=bbox,
                confidence=output[i][4],
                classLabel=names[int(output[i][5])],  # airplane, car, bicycle
                classId=int(output[i][5]),
                imgUID=img_uid
            )
            detection_list.append(newdetect)
        return detection_list

    def transport_inference(self):
        output, names, im = Yolov5Detect(
            model=self.weight,
            source=self.image.value,
            device=str(self.select_device),
            conf_thres=float(self.conf_thres),
            iou_thres=float(self.iou_thres)
        ).run()
        output_detection_list = self.output_result(output, names, self.image.uID)
        return output_detection_list

    def run(self):
        self.image = Image.get_frame(img=self.image, redis_db=self.redis_db)
        self.detection = self.transport_inference()
        packageModel = build_response(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()
