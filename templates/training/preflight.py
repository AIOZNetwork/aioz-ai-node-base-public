"""Pre-submission preflight for the AIOZ AI training template.

Run it before you submit:

    python preflight.py

It runs a sample input through run(), prints the output, and verifies:
  1. my_ai_lib imports and exposes a callable run.
  2. TaskInput / TaskOutput subclass the AIOZ AI base classes.
  3. run() returns a valid TaskOutput.

Your schema is yours; this does not enforce specific fields. If you changed your
input fields, update the TaskInput(...) call below to match.
"""

import os
import shutil
import sys
from typing import NoReturn

from aioz_ainode_adapter.schemas import FileObject, InputObject, OutputObject


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
    # Create dummy directory for testing
    dummy_data = "dummy_dataset"
    os.makedirs(dummy_data, exist_ok=True)

    try:
        # TaskInput without weight_dir trains from scratch
        task_input = TaskInput(
            dataset_dir=dummy_data,
            weight_dir=None,
            epochs=1,
            batch_size=4,
            learning_rate=0.01,
        )
        print(f"Input:  {task_input}")
        try:
            output = my_ai_lib.run(task_input)
        except Exception as e:
            fail(f"run() raised an exception: {e}")
        print(f"Output: {output}")

        # 4. Output shape -----------------------------------------------------
        if not isinstance(output, TaskOutput):
            fail(f"run() must return your TaskOutput, got {type(output).__name__}.")
        if not isinstance(output.weight_last, FileObject) or not isinstance(
            output.weight_best, FileObject
        ):
            fail(
                "TaskOutput must contain weight_last and weight_best as FileObject instances."
            )
        ok(
            "run() returned a valid TaskOutput with weight_last and weight_best FileObjects"
        )

        print("\nPreflight passed — your submission is well-formed.")
    finally:
        if os.path.exists(dummy_data):
            shutil.rmtree(dummy_data, ignore_errors=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
