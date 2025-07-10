from pydantic import Field, validator
from typing import List, Optional, Union, Literal,Tuple
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputBlurring(Input):
    name: Literal["inputBlurring"] = "inputBlurring"
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
        title = "Blurring"

class InputZoom(Input):
    name: Literal["InputZoom"] = "InputZoom"
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
        title = "Zoom"


class OutputBlurring(Output):
    name: Literal["outputBlurring"] = "outputBlurring"
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
        title = "Blurring"

class OutputZoom(Output):
    name: Literal["outputZoom"] = "outputZoom"
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
        title = "Zoom"


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


class ZoomFatimaExecutorInputs(Inputs):
    inputImage: InputZoom

class BlurringFatimaExecutorInputs(Inputs):
    inputImage: InputBlurring




class ZoomFatimaExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

class BlurringFatimaExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox





class ZoomFatimaExecutorRequest(Request):
    inputs: Optional[ZoomFatimaExecutorInputs]
    configs: ZoomFatimaExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class BlurringFatimaExecutorRequest(Request):
    inputs: Optional[BlurringFatimaExecutorInputs]
    configs: BlurringFatimaExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }



class ZoomFatimaExecutorOutputs(Outputs):
    outputImage: OutputZoom


class BlurringFatimaExecutorOutputs(Outputs):
    outputImage: OutputBlurring





class ZoomFatimaExecutorResponse(Response):
    outputs: ZoomFatimaExecutorOutputs


class BlurringFatimaExecutorResponse(Response):
    outputs: BlurringFatimaExecutorOutputs



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


class BlurringFatimaExecutor(Config):
    name: Literal["BlurringFatimaExecutor"] = "BlurringFatimaExecutor"
    value: Union[BlurringFatimaExecutorRequest, BlurringFatimaExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }




class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[BlurringFatimaExecutor,ZoomFatimaExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Type"


class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["BlurringFatima"] = "BlurringFatima"
