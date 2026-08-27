"""Input/output schema — INFERENCE variant.

Define the fields your task needs. Keep the class names and the base classes
(InputObject / OutputObject); the fields inside are yours.

This example is shaped for an image-generation model:
  input  = prompt, negative_prompt, seed
  output = an image file

Inherited from InputObject:
  device: Literal["cpu", "cuda"] = "cuda"
  model_storage_directory: str  (set by AIOZ AI; load weights from here)
"""

import random

from pydantic import Field

from aioz_ainode_adapter.schemas import FileObject, InputObject, OutputObject


class TaskInput(InputObject):
    prompt: str
    negative_prompt: str = ""
    seed: int = Field(default_factory=lambda: random.randint(0, 2**32 - 1))


class TaskOutput(OutputObject):
    image: FileObject
