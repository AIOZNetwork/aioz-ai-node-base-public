import os
import io
import shutil
import tempfile
from . import utils
from pathlib import Path
from typing import Literal, List, Union
from pydantic import BaseModel, ConfigDict, AnyUrl


class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        protected_namespaces=())

    @property
    def type_name(self):
        return self.type


class FileObject(CustomBaseModel):
    type: Literal["FileObj"] = "FileObj"
    data: Union[io.BufferedIOBase, Path, AnyUrl] = None
    name: str = "output_file.ext"

    def write_buff(self, tmp_dir: Union[str, Path] = None):
        if isinstance(self.data, io.BufferedIOBase):
            directory = tmp_dir if tmp_dir and os.path.isdir(tmp_dir) else None
            safe_name = Path(self.name).name
            with tempfile.NamedTemporaryFile(
                    mode="wb",
                    dir=directory,
                    suffix=safe_name,
                    delete=False) as output:
                shutil.copyfileobj(self.data, output)
                self.data = Path(output.name)
        return str(self.data)


class InputObject(CustomBaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["InputObj"] = "InputObj"
    device: Literal["cpu", "cuda"] = "cuda"
    model_storage_directory: str = utils.resource_path("models")


class OutputObject(CustomBaseModel):
    model_config = ConfigDict(extra="allow")
    type: Literal["OutputObj"] = "OutputObj"


class ErrorMsg(CustomBaseModel):
    type: Literal["ErrorMsg"] = "ErrorMsg"
    message: str = "Something went wrong"
    traceback: str = ""
