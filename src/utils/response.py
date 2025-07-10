
from sdks.novavision.src.helper.package import PackageHelper
from components.BlurringFatima.src.models.PackageModel import (PackageModel, PackageConfigs, ConfigExecutor, BlurringFatimaExecutorOutputs, BlurringFatimaExecutorResponse, BlurringFatimaExecutor, OutputImage)


def build_response(context):
    outputImage = OutputImage(value=context.image)
    blurringFatimaExecutorOutputs = BlurringFatimaExecutorOutputs(outputImage=outputImage)
    blurringFatimaExecutorResponse = BlurringFatimaExecutorResponse(outputs=blurringFatimaExecutorOutputs)
    blurringFatimaExecutor = BlurringFatimaExecutor(value=blurringFatimaExecutorResponse)
    configexecutor = ConfigExecutor(value=blurringFatimaExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
