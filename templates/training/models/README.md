# models/

This directory is used to store model weights and checkpoints generated **during** and **after** the training process.

## How AIOZ AI saves and collects weights

At run time, AIOZ AI sets **`model_storage_directory`** on your `TaskInput` (inherited from `InputObject`).

- **Save weights to this path:** During training (e.g. at every epoch) and after training completes, save your model checkpoints (such as `last.pth` and `best.pth`) into `model_storage_directory`.
- **Locally:** `model_storage_directory` defaults to `./models`, so any checkpoints generated during local execution or `python preflight.py` will be saved here.
- **Output contract:** AIOZ AI expects the training workflow to return `weight_last` and `weight_best` as `FileObject` instances in `TaskOutput`.

## Core Checkpoints

| Weight File            | Description                                                                                | Purpose                                                               |
| :--------------------- | :----------------------------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| **`best.pth`** | Weights achieving the best validation metric (e.g. lowest val loss, highest accuracy/mAP). | Final evaluation, deployment, or downstream tasks.                    |
| **`last.pth`** | Weights from the most recent training epoch or final training step.                        | Checkpointing, training continuity, or resuming interrupted training. |

You can also save intermediate checkpoints (e.g., `epoch_10.pth`) here if needed.

## Code Example

### 1. Saving checkpoints in `pipeline.py`

```python
import os
import torch
from pathlib import Path
from typing import Any, Tuple, Union

def save_model(
    model: Any, 
    model_storage_directory: Union[str, Path]
) -> Tuple[Any, Any]:
    """Save best and last weights to `model_storage_directory` and return opened file objects."""
    storage_dir = Path(model_storage_directory)
    storage_dir.mkdir(parents=True, exist_ok=True)

    best_path = storage_dir / "best.pth"
    last_path = storage_dir / "last.pth"

    # Save checkpoint state / state_dict
    torch.save(model.state_dict(), last_path)
  
    # Save or update best weights when validation metric improves
    torch.save(model.state_dict(), best_path)

    # Return opened file objects (binary read mode) for TaskOutput
    return open(last_path, "rb"), open(best_path, "rb")
```

### 2. Returning weights via `TaskOutput` in `run.py`

```python
from aioz_ainode_adapter.schemas import FileObject
from .schemas import TaskInput, TaskOutput
from .pipeline import save_model

def run(input_obj: TaskInput) -> TaskOutput:
    try:
        task_input = TaskInput.model_validate(input_obj.model_dump())
        ...
        
        # Train and evaluate model
        ...

        # Save model weights to model_storage_directory
        weight_last_file, weight_best_file = save_model(model, task_input.model_storage_directory)

        output_obj = TaskOutput(
            weight_last=FileObject(
                data=weight_last_file,
                name=os.path.basename(weight_last_file.name)
            ),
            weight_best=FileObject(
                data=weight_best_file,
                name=os.path.basename(weight_best_file.name)
            )
        )
    except Exception as e:
        raise Exception(e)

    return output_obj

```

## Resuming vs. Saving Weights

- **`model_storage_directory` (Output):** Destination where the current training run saves checkpoints (`best.pth`, `last.pth`).
- **`weight_dir` (Optional Input):** Directory containing pre-trained weights or a previous checkpoint to resume training from.

## Example Directory Layout

```
models/
├── best.pth                # Best model checkpoint based on validation score
├── last.pth                # Most recent checkpoint from training
├── epoch_10.pth            # (Optional) Periodic epoch checkpoint
└── training_stats.json     # (Optional) Additional training metrics/logs
```

## Notes

- This `README.md` keeps the folder tracked in git when no weights are present.
- **Do not commit large weight files directly to git** unless tracked by Git LFS. Heavy checkpoint files should typically be listed in `.gitignore`.
- Always ensure the directory exists before saving (e.g. `os.makedirs(model_storage_directory, exist_ok=True)`).
