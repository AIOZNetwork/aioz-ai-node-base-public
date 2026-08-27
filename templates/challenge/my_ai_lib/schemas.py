"""Input/output schema

=============================================================================
DO NOT EDIT (controlled by AIOZ AI for this challenge)
Editing these classes will fail grading and your submission will be rejected.
=============================================================================
"""

from aioz_ainode_adapter.schemas import FileObject, InputObject, OutputObject


class TaskInput(InputObject):
    input_folder: str


class TaskOutput(OutputObject):
    output_file: FileObject
