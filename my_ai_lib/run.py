from pathlib import Path
from typing import Any, Union, Literal, Optional
from aioz_ainode_adapter.schemas import InputObject, OutputObject, FileObject


class MyInput(InputObject):
    input_image: str
    example_param: Optional[Any] = ""


class MyOutput(OutputObject):
    text: str
    output_image: FileObject


def do_ai_task(
        input_image: Union[str, Path],
        example_param: Any,
        model_storage_directory: Union[str, Path],
        device: Literal["cpu", "cuda", "gpu"] = "cpu",
        *args, **kwargs) -> Any:
    """Define AI task: load model, pre-process, post-process, etc ..."""
    # Define AI task workflow. Below is an example
    text = "This is the AI task result"
    output_image = open("wiki/aioz.png", "rb")  # io.BufferedReader
    return text, output_image


def run(input_obj: InputObject) -> OutputObject:
    try:
        my_input = MyInput.model_validate(input_obj.model_dump())
        print(f"Input: {my_input}")

        # do something
        text, output_image = do_ai_task(
            input_image=my_input.input_image,
            example_param=my_input.example_param,
            model_storage_directory=my_input.model_storage_directory,
            device=my_input.device
        )

        # make output object
        # # create a file object if the output is a file
        output_file = FileObject(data=output_image, name="output_image.png")
        output_obj = MyOutput(text=text, output_image=output_file)
    except Exception as e:
        raise Exception(e)

    return output_obj

