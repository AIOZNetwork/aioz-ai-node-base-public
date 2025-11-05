[![Generic badge](https://img.shields.io/badge/aioz_ainode_adapter-1.0.0-green.svg)]()
[![Generic badge](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-360/)

# AIOZ AI MODEL
A lightweight Python adapter that allows your custom AI library to seamlessly integrate and run inside the **AIOZ-AI-Node** environment.  
This package defines standard interfaces for **input**, **output**, and **file objects**, ensuring your AI task can communicate properly with the **AIOZ-AI-Node** system.

## Dependencies

Since your AI library will run on the **AIOZ-AI-Node** environment, below are listed all the libraries and corresponding versions available in the **AIOZ-AI-Node** environment.
On your local machine, you can create a new virtual environment and install all the libraries below:

```shell
pip install -r requirements.txt
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118
pip install xformers==0.0.23 --index-url https://download.pytorch.org/whl/cu118
```
## Tutorial

### Step 1: Define your AI library
Your AI library should contain a **_run()_** entrypoint, which the AIOZ-AI-Node system will call automatically.

#### 1.1: Define _my_ai_lib/init.py_

```python
from .run import run
```

This file defines that the `run()` function in run.py as an attribute of the `my_ai_lib` and that I can call it by `my_ai_lib.run()`

#### 1.2: Define _my_ai_lib/run.py_

Define your input object and output object inherit from `InputObject`, `OutputObject`

Example input / output object:

```python
from pathlib import Path
from typing import Any, Union, Literal
from aioz_ainode_adapter.schemas import InputObject, OutputObject, FileObject


class MyInput(InputObject):
    input_image: str
    example_param: Any


class MyOutput(OutputObject):
    text: str
    output_image: FileObject
```

<br/>
<br/>

In **_aioz_ainode_adapter_** library we def ine 3 Object type: `InputObject`, `OutputObject`, `FileObject` (define base on pydantic.BaseModel)

- **_InputObject_**: Define the format for input when the AIOZ-AI-Node system sends to your AI library. This object has two default param: `device` and `model_storage_directory`.

| Attribute                 | Type   | Desc                                                                             |
|:--------------------------|:-------|:---------------------------------------------------------------------------------|
| `device`                  | Choice | This is a device for your AI model, it has three options ["cuda", "cpu"] |
| `model_storage_directory` | String | This is a directory storing your model weights                                   |

> NOTE: If your AI library needs to provide a directory path where your AI model weights are stored, that path must be obtained from **_model_storage_directory_**.
> Because the AIOZ-AI-Node system will specify this.

<br/>

- **_OutputObject_**: Define the format for output when your AI library sends to the AIOZ-AI-Node system.
  
- **_FileObject_**: Define the format for the file, if your output has a file. This object has two fields: `data` and `name`.

| Attribute | Type   | Desc                                                                                                   |
|:----------|:-------|:-------------------------------------------------------------------------------------------------------|
| `data`    | Choice | This is a file data, this attr allows three formats: io.BufferedReader, Path (local file path) and URL |
| `name`    | String | This is a file name                                                                                    |

Example for creating **_FileObject_** from local file.
  
```python
output_file = FileObject(data=open("file/path.txt", "rb"), name="output.txt")
```

<br/>

>NOTE:
>
> If your input params have a file, it must be a **_local file path_** or **_URL_**.
>
> And if your output has a file, it must be a **_FileObject_**.

#### 1.3: Define _run()_ function

```python
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
    return output_obj
```

In which the **_run()_** function is a mandatory function and is the main function, you are not allowed to change the name.
<br/>
And **_do_ai_task()_** is your function to define your AI-task workflow, you can rename this function, and do anything you want to.

>NOTE: 
> - Output from **_run()_** function must be a OutputObject.
> - If you need to import external code or utility modules from within your project, please use relative imports, for example:
> ```
> from .lib import lib_a
> ```
> This ensures the code runs correctly inside the sandboxed environment.

### Step 2: Define _demo.py_ to test your AI library

Example

```python
import my_ai_lib
from aioz_ainode_adapter.schemas import InputObject


def main():
    input_obj = InputObject(input_image="wiki/aioz.png", example_param="example")
    output_obj = my_ai_lib.run(input_obj)
    print(f"Output: {output_obj}")


if __name__ == '__main__':
    main()
```

In this file **_my_ai_lib.run()_** receives an **_InputObject_** and returns an **_OutputObject_**.
<br/>
After run demo.py you can see console like that.

```shell
Input: type='InputObj' device='cuda' model_storage_directory='models' input_image='wiki/aioz.png' example_param='example'
Output: type='OutputObj' text='This is the AI task result' output_image=FileObject(type='FileObj', data=<_io.BufferedReader name='wiki/aioz.png'>, name='output_image.png')
```

# License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
  <img alt="License Creative Commons " style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" />
</a><br />
This repo is shared with terms of
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
  Creative Commons Attribution 4.0 International (CC BY 4.0)
</a> @ <a rel="author" href="https://ai.aioz.io/"> AIOZ Pte Ltd </a>
