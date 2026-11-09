# AIOZ AI Challenge Submission Template

Use this template to submit a model to an AIOZ AI Challenge. AIOZ AI defines the
input/output schema, and you implement the AI logic.

## Fixed and editable parts

| Part | Rule |
| --- | --- |
| `my_ai_lib` package name | **Locked.** Keep this folder name and export `run` through `from .run import run`. |
| `TaskInput` / `TaskOutput` in `schemas.py` | **Locked.** Preserve these challenge schemas exactly. |
| `run()` in `run.py` | **Locked.** Preserve this entrypoint name and signature. |
| `load_model` / `preprocess` / `predict` / `postprocess` | **Yours.** Fill in these stages with your logic. |
| `requirements.txt` | **Yours.** Add every dependency you import. |

## Where your code goes

```
my_ai_lib/
├── __init__.py     # fixed: exposes run()
├── schemas.py      # fixed: challenge input/output schema
├── model.py        # load_model()          <- load your weights here
├── pipeline.py     # preprocess/predict/postprocess  <- your logic
└── run.py          # fixed entrypoint
```

## Quickstart

```bash
pip install -r requirements.txt   # installs the AIOZ AI adapter + your deps
python preflight.py               # runs the sample end-to-end and verifies the output
```

`python preflight.py` prints the input, the output, and a run of ✅ checks
ending in `Preflight passed`:

```
✅  my_ai_lib.run found
✅  locked schema is intact
Input:  type='InputObj' device='cuda' model_storage_directory='.../models' input_folder='sample_input/'
Output: type='OutputObj' output_file=FileObject(type='FileObj', data=..., name='result.csv')
✅  run() returned a valid TaskOutput with a file
```

## The contract

* **`InputObject`** (base fields your `TaskInput` inherits):
  * `device`: one of `cpu`, `cuda` (default `cuda`).
  * `model_storage_directory`: supplied model-weight path; resolve every model asset from it.
* This challenge adds one input field: **`input_folder: str`**.
* **`OutputObject`**: this challenge returns **`output_file: FileObject`**.
* **`FileObject`**: `data` (a local `Path`, an open binary file, or a URL) + `name`.

## Notes

* Use **relative imports** for your own modules (`from .lib import helper`) so
  your code runs inside the sandbox.
* Allow exceptions to propagate so AIOZ AI can report them.
* Run `python preflight.py` before every submission.
