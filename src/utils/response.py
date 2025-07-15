
from sdks.novavision.src.helper.package import PackageHelper
from components.BlurringFatima.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, BlurringFatimaExecutorOutputs, BlurringFatimaExecutorResponse, BlurringFatimaExecutor, OutputImageOne, OutputImageTwo
from components.BlurringFatima.src.models.PackageModel import ZoomFatimaExecutorOutputs, ZoomFatimaExecutorResponse, ZoomFatimaExecutor
from components.BlurringFatima.src.models.PackageModel import GrayFatimaExecutorOutputs, GrayFatimaExecutorResponse, GrayFatimaExecutor


def build_response(context):
    outputImageOne = OutputImageOne(value=context.image)
    blurringFatimaExecutorOutputs = BlurringFatimaExecutorOutputs(outputImageOne=outputImageOne)
    blurringFatimaExecutorResponse = BlurringFatimaExecutorResponse(outputs=blurringFatimaExecutorOutputs)
    blurringFatimaExecutor = BlurringFatimaExecutor(value=blurringFatimaExecutorResponse)
    configexecutor = ConfigExecutor(value=blurringFatimaExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_zoom(context):
    outputImageOne = OutputImageOne(value=context.imageOne)
    outputImageTwo = OutputImageTwo(value=context.imageTwo)
    zoomFatimaExecutorOutputs = ZoomFatimaExecutorOutputs(outputImageOne=outputImageOne, outputImageTwo=outputImageTwo)
    zoomFatimaExecutorResponse = ZoomFatimaExecutorResponse(outputs=zoomFatimaExecutorOutputs)
    zoomFatimaExecutor = ZoomFatimaExecutor(value=zoomFatimaExecutorResponse)
    configexecutor = ConfigExecutor(value=zoomFatimaExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel

def build_response_gray(context):
    outputImageOne = OutputImageOne(value=context.imageOne)
    outputImageTwo = OutputImageTwo(value=context.imageTwo)
    grayFatimaExecutorOutputs = GrayFatimaExecutorOutputs(outputImageOne=outputImageOne, outputImageTwo=outputImageTwo)
    grayFatimaExecutorResponse = GrayFatimaExecutorResponse(outputs=grayFatimaExecutorOutputs)
    grayFatimaExecutor = GrayFatimaExecutor(value=grayFatimaExecutorResponse)
    configexecutor = ConfigExecutor(value=grayFatimaExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
