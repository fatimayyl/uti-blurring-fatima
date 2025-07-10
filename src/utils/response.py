
from sdks.novavision.src.helper.package import PackageHelper
from components.BlurringFatima.src.models.PackageModel import (PackageModel, PackageConfigs, ConfigExecutor, BlurringFatimaExecutorOutputs, BlurringFatimaExecutorResponse, BlurringFatimaExecutor, OutputImage)
from components.ZoomFatima.src.models.PackageModel import (PackageModel, PackageConfigs, ConfigExecutor, ZoomFatimaExecutorOutputs, ZoomFatimaExecutorResponse, ZoomFatimaExecutor, OutputImage)


def build_response_blurring(context):
    outputImage = OutputImage(value=context.image)
    blurringFatimaExecutorOutputs = BlurringFatimaExecutorOutputs(outputImage=outputImage)
    blurringFatimaExecutorResponse = BlurringFatimaExecutorResponse(outputs=blurringFatimaExecutorOutputs)
    blurringFatimaExecutor = BlurringFatimaExecutor(value=blurringFatimaExecutorResponse)
    configexecutor = ConfigExecutor(value=blurringFatimaExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_zoom(context):
    outputImage = OutputImage(value=context.image)
    zoomFatimaExecutorOutputs = ZoomFatimaExecutorOutputs(outputImage=outputImage)
    zoomFatimaExecutorResponse = ZoomFatimaExecutorResponse(outputs=zoomFatimaExecutorOutputs)
    zoomFatimaExecutor = ZoomFatimaExecutor(value=zoomFatimaExecutorResponse)
    configexecutor = ConfigExecutor(value=zoomFatimaExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
