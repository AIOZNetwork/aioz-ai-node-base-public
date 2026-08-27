"""Challenge submission entrypoint."""

import os

from aioz_ainode_adapter.schemas import FileObject

from .model import load_model
from .pipeline import postprocess, predict, preprocess
from .schemas import TaskInput, TaskOutput


def run(input_obj: TaskInput) -> TaskOutput:
    """Mandatory entrypoint — DO NOT RENAME IT."""
    task_input = TaskInput.model_validate(input_obj.model_dump())  # validate the input

    model = load_model(task_input.model_storage_directory, task_input.device)
    samples = preprocess(task_input.input_folder)
    predictions = predict(model, samples)
    output_path = postprocess(predictions)
    output = open(output_path, "rb")
    output_file = FileObject(data=output, name=os.path.basename(output.name))
    return TaskOutput(output_file=output_file)
