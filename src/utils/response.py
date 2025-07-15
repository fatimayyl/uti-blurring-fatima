
from sdks.novavision.src.helper.package import PackageHelper
from components.BlurringFatima.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, BlurringFatimaExecutorOutputs, BlurringFatimaExecutorResponse, BlurringFatimaExecutor, OutputImageOne, OutputImageTwo
from components.BlurringFatima.src.models.PackageModel import ZoomFatimaExecutorOutputs, ZoomFatimaExecutorResponse, ZoomFatimaExecutor



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
    outputImageOne = OutputImageOne(value=context.image)
    outputImageTwo = OutputImageTwo(value=context.image)
    zoomFatimaExecutorOutputs = ZoomFatimaExecutorOutputs(outputImageOne=outputImageOne, outputImageTwo=outputImageTwo)
    zoomFatimaExecutorResponse = ZoomFatimaExecutorResponse(outputs=zoomFatimaExecutorOutputs)
    zoomFatimaExecutor = ZoomFatimaExecutor(value=zoomFatimaExecutorResponse)
    configexecutor = ConfigExecutor(value=zoomFatimaExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
