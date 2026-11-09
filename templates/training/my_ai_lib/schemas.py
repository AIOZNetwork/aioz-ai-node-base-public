"""Input/output schema — TRAINING variant.

Define the fields your task needs. Keep the class names and the base classes
(InputObject / OutputObject); the fields inside are yours.
"""

from typing import Optional

from aioz_ainode_adapter.schemas import FileObject, InputObject, OutputObject


class TaskInput(InputObject):
    dataset_dir: str
    weight_dir: Optional[str] = None
    epochs: int = 10
    batch_size: int = 32
    learning_rate: float = 0.001


class TaskOutput(OutputObject):
    weight_last: FileObject
    weight_last: FileObject
