"""Pre-submission preflight for the AIOZ AI Challenge.

Run it before you submit:

    python preflight.py

Passing here means your submission is well-formed, not that your model scores well.
"""

import csv
import sys
from pathlib import Path
from typing import NoReturn


def fail(msg: str) -> NoReturn:
    print(f"❌  {msg}")
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"✅  {msg}")


def main() -> None:
    # 1. Import ------------------------------------------------------------
    try:
        import my_ai_lib
        from my_ai_lib.schemas import TaskInput, TaskOutput
    except Exception as e:
        fail(f"Could not import my_ai_lib (check your code / requirements): {e}")
    from aioz_ainode_adapter.schemas import FileObject, InputObject, OutputObject

    if not callable(getattr(my_ai_lib, "run", None)):
        fail("my_ai_lib.run is missing or not callable. Keep `from .run import run`.")
    ok("my_ai_lib.run found")

    # 2. Locked schema intact ---------------------------------------------
    if not issubclass(TaskInput, InputObject):
        fail("TaskInput must subclass InputObject — did you edit schemas.py?")
    if not issubclass(TaskOutput, OutputObject):
        fail("TaskOutput must subclass OutputObject — did you edit schemas.py?")

    required = [
        (TaskInput, "input_folder", str),
        (TaskOutput, "output_file", FileObject),
    ]
    for model, field_name, expected_type in required:
        field = model.model_fields.get(field_name)
        if field is None:
            fail(
                f"{model.__name__} is missing the locked field `{field_name}`. Do not edit schemas.py."
            )
        if field.annotation is not expected_type:
            fail(
                f"{model.__name__}.{field_name} must stay typed as `{expected_type.__name__}`."
            )
    ok("locked schema is intact")

    # 3. Run on the sample input ------------------------------------------
    task_input = TaskInput(input_folder="sample_input/")
    print(f"Input:  {task_input}")
    try:
        output = my_ai_lib.run(task_input)
    except Exception as e:
        fail(f"run() raised an exception on sample_input/: {e}")
    print(f"Output: {output}")

    # 4. Output shape -----------------------------------------------------
    if not isinstance(output, TaskOutput):
        fail(f"run() must return a TaskOutput, got {type(output).__name__}.")
    if not isinstance(output.output_file, FileObject):
        fail("output_file must be a FileObject.")
    if output.output_file.data is None:
        fail("output_file.data is empty — your FileObject carries no file.")
    if output.output_file.name != "result.csv":
        fail(f"output_file.name must be result.csv, got {output.output_file.name!r}.")

    result_path = Path("result.csv")
    if not result_path.is_file():
        fail("run() did not create result.csv.")
    with result_path.open(newline="") as result_file:
        rows = list(csv.reader(result_file))
    expected = [["file_name", "size_bytes"], ["notes.txt", "220"]]
    if rows != expected:
        fail(f"result.csv content is incorrect: expected {expected!r}, got {rows!r}.")
    ok("run() returned the expected TaskOutput and result.csv artifact")

    print("\nPreflight passed — your submission is well-formed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
