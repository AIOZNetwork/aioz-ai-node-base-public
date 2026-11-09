# AIOZ AI Training Template

Use this template to train a model on AIOZ AI, defining your own input and output
fields. The example is shaped for a **model training** workflow:

- **input**: `dataset_dir`, `weight_dir` (optional, for resume), `epochs`, `batch_size`, `learning_rate`
- **output**: `last_weight: FileObject`, `best_weight: FileObject`

Keep the contract shape (`InputObject` / `OutputObject` and the `run()`
entrypoint); the fields inside are yours.

## What's fixed vs. yours

| Part | Rule |
| --- | --- |
| `my_ai_lib` package name | **Fixed.** AIOZ AI imports `my_ai_lib.run(...)`. Do not rename the folder or remove `from .run import run`. |
| `run()` in `run.py` | **Fixed.** It is the entrypoint AIOZ AI calls. Adapt its body to your stages; do not rename or remove it. |
| `TaskInput` / `TaskOutput` in `schemas.py` | **Yours.** Define the hyperparameters and fields your training needs. |
| `define_model` / `load_model` in `model.py` | **Yours.** Define your model architecture and weight loading logic. |
| `load_data` / `train_model` / `evaluate_model` / `save_model` in `pipeline.py` | **Yours.** Fill in these stages with your dataset loading, preprocessing, and training loops. |
| `requirements.txt` | **Yours.** Add every dependency you import. |

## Where your code goes

```
my_ai_lib/
├── __init__.py     # exposes run() — do not touch
├── schemas.py      # your input/output fields
├── model.py        # define_model() / load_model() <- model architecture & resume logic
├── pipeline.py     # data/train/eval/save      <- your training logic
└── run.py          # entrypoint — wires the stages together
```

## Quickstart

```bash
pip install -r requirements.txt   # installs the AIOZ AI adapter + your deps
python preflight.py               # runs a dummy training workflow and verifies the output
```

## The contract

* **`InputObject`** (base fields your `TaskInput` inherits):
  * `device`: one of `cpu`, `cuda`, `gpu` (default `cpu`).
  * `model_storage_directory`: directory where your output models/checkpoints are stored by default.
* This example's input:
  * **`dataset_dir: str`**: path to the folder containing your user-defined dataset.
  * **`weight_dir: Optional[str] = None`**: optional path to pre-trained weights/checkpoint for resuming.
  * **`epochs: int`**, **`batch_size: int`**, **`learning_rate: float`**: training hyperparameters.
* This example's output: **`last_weight: FileObject`**, **`best_weight: FileObject`**.

## Defining your own fields

1. Edit `TaskInput` / `TaskOutput` in `my_ai_lib/schemas.py`.
2. Update the stages in `my_ai_lib/pipeline.py`, `my_ai_lib/model.py` (and `run()` if needed) to use them.
3. Update the `TaskInput(...)` call in `preflight.py` to match.

## Dataset (User-Defined)

The dataset format and loading logic are **completely user-defined**:

- **Input path:** AIOZ AI passes the path to your dataset via `task_input.dataset_dir`.
- **Layout:** Organize your files (e.g. images, labels, CSVs) inside `dataset_dir` however your model requires.
- **Loading:** Implement `load_data(dataset_dir)` in `my_ai_lib/pipeline.py` to parse files and return your train/val sets or loaders.
- **Local testing:** In `preflight.py`, point `dataset_dir` to your local dataset folder to test loading before submission.

### Code example

```python
# Example: Custom Dataset & DataLoader in my_ai_lib/pipeline.py
from pathlib import Path
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data_dir: Path):
        self.files = sorted(data_dir.glob("*.*"))
    def __len__(self):
        return len(self.files)
    def __getitem__(self, idx):
        # Load and preprocess single sample
        return sample, label

def load_data(dataset_dir: str):
    base = Path(dataset_dir)
    train_loader = DataLoader(CustomDataset(base / "train"), batch_size=32, shuffle=True)
    val_loader = DataLoader(CustomDataset(base / "val"), batch_size=32, shuffle=False)
    return train_loader, val_loader
```

## Resuming Training

The `run.py` script automatically checks if a checkpoint (`last.pth` or `best.pth`) exists inside `weight_dir`. If it does, it calls `load_model()` to resume training from the last saved state instead of starting from scratch using `define_model()`.

## Notes

* Use **relative imports** for your own modules (`from .lib import helper`) so
  your code runs inside the sandbox.
* Let exceptions propagate — AIOZ AI reports them; do not catch and hide them.
* Run `python preflight.py` before submitting.

# License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
  <img alt="License Creative Commons " style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" />
</a><br />
This repo is shared with terms of
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
  Creative Commons Attribution 4.0 International (CC BY 4.0)
</a> @ <a rel="author" href="https://ai.aioz.io/"> AIOZ Pte Ltd </a>
