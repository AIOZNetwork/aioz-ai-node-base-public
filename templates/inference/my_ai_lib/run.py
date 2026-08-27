"""AIOZ AI inference entrypoint.

Wires the pipeline stages for an image-generation task
(prompt / negative_prompt / seed -> image). Adapt the stages to your model.
"""
import os
from aioz_ainode_adapter.schemas import FileObject

from .model import load_model
from .pipeline import postprocess, predict, preprocess
from .schemas import TaskInput, TaskOutput


def run(input_obj: TaskInput) -> TaskOutput:
    """Mandatory entrypoint — DO NOT RENAME IT."""
    task_input = TaskInput.model_validate(input_obj.model_dump())  # validate the input

    model = load_model(task_input.model_storage_directory, task_input.device)
    params = preprocess(task_input.prompt, task_input.negative_prompt, task_input.seed)
    image_bytes = predict(model, params)
    image_path = postprocess(image_bytes)
    output = open(image_path, "rb")
    return TaskOutput(image=FileObject(data=output, name=os.path.basename(output.name)))
