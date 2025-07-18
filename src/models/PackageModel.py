from pydantic import Field, validator
from typing import List, Optional, Union, Literal,Tuple
from sdks.novavision.src.base.model import Detection, Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImageOne(Output):
    name: Literal["outputImageOne"] = "outputImageOne"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class OutputImageTwo(Output):
    name: Literal["outputImageTwo"] = "outputImageTwo"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"


class Degree(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"

    class Config:
        title = "Angleee"



class CropTopPixels(Config):
    name: Literal["CropTopPixels"] = "CropTopPixels"
    value: int = Field(default=50, ge=1, le=1000)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["1 – 1000"] = "1 – 1000"

    class Config:
        title = "Top Crop Pixels"


class CropBottomPixels(Config):
    name: Literal["CropBottomPixels"] = "CropBottomPixels"
    value: int = Field(default=50, ge=1, le=1000)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["1 – 1000"] = "1 – 1000"

    class Config:
        title = "Bottom Crop Pixels"


class CropTopOption(Config):
    name: Literal["CropTop"] = "CropTop"
    value: Literal["CropTop"] = "CropTop"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    config: CropTopPixels = CropTopPixels()

    class Config:
        title = "Top Crop"


class CropBottomOption(Config):
    name: Literal["CropBottom"] = "CropBottom"
    value: Literal["CropBottom"] = "CropBottom"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    config: CropBottomPixels = CropBottomPixels()

    class Config:
        title = "Bottom Crop"


class CropMode(Config):
    name: Literal["CropMode"] = "CropMode"
    value: Union[CropTopOption, CropBottomOption]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Crop Type"


class ZoomInFactor(Config):
    name: Literal["ZoomInFactor"] = "ZoomInFactor"
    value: float = Field(default=1.2, ge=1.0, le=10.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["1.0 – 10.0"] = "1.0 – 10.0"
    class Config:
        title = "Zoom In Factor"


class ZoomOutFactor(Config):
    name: Literal["ZoomOutFactor"] = "ZoomOutFactor"
    value: float = Field(default=0.8, ge=0.1, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["0.1 – 1.0"] = "0.1 – 1.0"
    class Config:
        title = "Zoom Out Factor"



class ZoomInOption(Config):
    name: Literal["ZoomIn"] = "ZoomIn"
    value: Literal["ZoomIn"] = "ZoomIn"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    config: ZoomInFactor = ZoomInFactor()  # Bu dökümana uygun: "ZoomIn" seçilirse bu gösterilir

    class Config:
        title = "Zoom In"


class ZoomOutOption(Config):
    name: Literal["ZoomOut"] = "ZoomOut"
    value: Literal["ZoomOut"] = "ZoomOut"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"
    config: ZoomOutFactor = ZoomOutFactor()  # "ZoomOut" seçilirse bu gösterilir

    class Config:
        title = "Zoom Out"


class ZoomMode(Config):
    name: Literal["ZoomMode"] = "ZoomMode"
    value: Union[ZoomInOption, ZoomOutOption]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Zoom Type"




class GrayFatimaExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo


class GrayFatimaExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

class GrayFatimaExecutorRequest(Request):
    inputs: Optional[GrayFatimaExecutorInputs]
    configs: GrayFatimaExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class GrayFatimaExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

class GrayFatimaExecutorResponse(Response):
    outputs: GrayFatimaExecutorOutputs

class GrayFatimaExecutor(Config):
    name: Literal["GrayFatimaExecutor"] = "GrayFatimaExecutor"
    value: Union[GrayFatimaExecutorRequest, GrayFatimaExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Gray"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ZoomFatimaExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

class ZoomFatimaExecutorConfigs(Configs):
    zoomMode: ZoomMode

class ZoomFatimaExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo

class ZoomFatimaExecutorRequest(Request):
    inputs: Optional[ZoomFatimaExecutorInputs]
    configs: ZoomFatimaExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class ZoomFatimaExecutorResponse(Response):
    outputs: ZoomFatimaExecutorOutputs


class ZoomFatimaExecutor(Config):
    name: Literal["ZoomFatimaExecutor"] = "ZoomFatimaExecutor"
    value: Union[ZoomFatimaExecutorRequest, ZoomFatimaExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "ZoomFatima"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class CropFatimaExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo


class CropFatimaExecutorConfigs(Configs):
    cropMode: CropMode

class CropFatimaExecutorRequest(Request):
    inputs: Optional[CropFatimaExecutorInputs]
    configs: CropFatimaExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class CropFatimaExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

class CropFatimaExecutorResponse(Response):
    outputs: CropFatimaExecutorOutputs

class CropFatimaExecutor(Config):
    name: Literal["CropFatimaExecutor"] = "CropFatimaExecutor"
    value: Union[CropFatimaExecutorRequest, CropFatimaExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Crop"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class BlurringFatimaExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

class BlurringFatimaExecutorInputs(Inputs):
    inputImageOne: InputImageOne

class BlurringFatimaExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne

class BlurringFatimaExecutorRequest(Request):
    inputs: Optional[BlurringFatimaExecutorInputs]
    configs: BlurringFatimaExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class BlurringFatimaExecutorResponse(Response):
    outputs: BlurringFatimaExecutorOutputs


class BlurringFatimaExecutor(Config):
    name: Literal["BlurringFatimaExecutor"] = "BlurringFatimaExecutor"
    value: Union[BlurringFatimaExecutorRequest, BlurringFatimaExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "BlurringFatima"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class TransportExecutorInputs(Inputs):
    inputImageOne: InputImageOne


class TransportExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne



class TransportExecutorRequest(Request):
    inputs: Optional[TransportExecutorInputs]

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class TransportExecutorResponse(Response):
    outputs: TransportExecutorOutputs


class TransportExecutor(Config):
    name: Literal["TransportDetection"] = "TransportDetection"
    value: Union[TransportExecutorRequest, TransportExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Transport Detection"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[BlurringFatimaExecutor,TransportExecutor,ZoomFatimaExecutor,GrayFatimaExecutor,CropFatimaExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["BlurringFatima"] = "BlurringFatima"
