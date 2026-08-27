"""Pre-submission preflight for the AIOZ AI inference template.

Run it before you submit:

    python preflight.py

It runs a sample input through run(), prints the output, and verifies:
  1. my_ai_lib imports and exposes a callable run.
  2. TaskInput / TaskOutput subclass the AIOZ AI base classes.
  3. run() returns a valid TaskOutput.

Your schema is yours; this does not enforce specific fields. If you changed your
input fields, update the TaskInput(...) call below to match.
"""

import sys
import io
import tempfile
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import NoReturn

from pydantic import BaseModel


def fail(msg: str) -> NoReturn:
    print(f"❌  {msg}")
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"✅  {msg}")


def find_file_objects(value: object) -> Iterator[object]:
    from aioz_ainode_adapter.schemas import FileObject

    if isinstance(value, FileObject):
        yield value
    elif isinstance(value, BaseModel):
        for field_name in type(value).model_fields:
            yield from find_file_objects(getattr(value, field_name))
    elif isinstance(value, Mapping):
        for item in value.values():
            yield from find_file_objects(item)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            yield from find_file_objects(item)


def validate_file_objects(output: BaseModel) -> int:
    files = list(find_file_objects(output))
    with tempfile.TemporaryDirectory(prefix="aioz-preflight-") as raw:
        materialization_directory = Path(raw)
        for index, file_object in enumerate(files, start=1):
            if file_object.data is None:
                fail(f"FileObject {index} has no data.")

            if isinstance(file_object.data, io.BufferedIOBase):
                artifact = Path(file_object.write_buff(materialization_directory))
            elif isinstance(file_object.data, Path):
                artifact = file_object.data
            else:
                continue

            if not artifact.is_file():
                fail(f"FileObject {index} references a missing file: {artifact}")
            if artifact.stat().st_size == 0:
                fail(f"FileObject {index} references an empty file: {artifact}")
    return len(files)


def main() -> None:
    # 1. Import ------------------------------------------------------------
    try:
        import my_ai_lib
        from my_ai_lib.schemas import TaskInput, TaskOutput
    except Exception as e:
        fail(f"Could not import my_ai_lib (check your code / requirements): {e}")
    from aioz_ainode_adapter.schemas import InputObject, OutputObject

    if not callable(getattr(my_ai_lib, "run", None)):
        fail("my_ai_lib.run is missing or not callable. Keep `from .run import run`.")
    ok("my_ai_lib.run found")

    # 2. Base relationship holds ------------------------------------------
    if not issubclass(TaskInput, InputObject):
        fail("TaskInput must subclass InputObject.")
    if not issubclass(TaskOutput, OutputObject):
        fail("TaskOutput must subclass OutputObject.")
    ok("TaskInput / TaskOutput subclass the AIOZ AI base classes")

    # 3. Run on a sample input --------------------------------------------
    # Update this TaskInput(...) if you changed your input fields.
    task_input = TaskInput(
        prompt="a red apple on a wooden table", negative_prompt="blurry", seed=42
    )
    print(f"Input:  {task_input}")
    try:
        output = my_ai_lib.run(task_input)
    except Exception as e:
        fail(f"run() raised an exception: {e}")
    print(f"Output: {output}")

    # 4. Output contract --------------------------------------------------
    if not isinstance(output, TaskOutput):
        fail(f"run() must return your TaskOutput, got {type(output).__name__}.")
    file_count = validate_file_objects(output)
    ok(
        f"run() returned a valid TaskOutput; validated {file_count} file "
        f"artifact{'s' if file_count != 1 else ''}"
    )

    print("\nPreflight passed — your submission is well-formed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
