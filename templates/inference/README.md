# AIOZ AI Inference Template

Use this template to run a model on AIOZ AI, defining your own input and output
fields. The example is shaped for an **image-generation** model:

- **input**: `prompt`, `negative_prompt`, `seed`
- **output**: an image file

Keep the contract shape (`InputObject` / `OutputObject` and the `run()`
entrypoint); the fields inside are yours.

## What's fixed vs. yours

| Part | Rule |
| --- | --- |
| `my_ai_lib` package name | **Fixed.** Keep this folder name and export `run` through `from .run import run`. |
| `run()` in `run.py` | **Fixed.** Preserve this entrypoint name while adapting its body to your stages. |
| `TaskInput` / `TaskOutput` in `schemas.py` | **Yours.** Define the fields your model needs. |
| `load_model` / `preprocess` / `predict` / `postprocess` | **Yours.** Fill in these stages with your logic. |
| `requirements.txt` | **Yours.** Add every dependency you import. |

## Where your code goes

```
my_ai_lib/
├── __init__.py     # fixed: exposes run()
├── schemas.py      # your input/output fields
├── model.py        # load_model()          <- load your weights here
├── pipeline.py     # preprocess/predict/postprocess  <- your logic
└── run.py          # entrypoint — wires the stages together
```

## Quickstart

```bash
pip install -r requirements.txt   # installs the AIOZ AI adapter + your deps
python preflight.py               # runs a sample prompt end-to-end and verifies the output
```

## The contract

* **`InputObject`** (base fields your `TaskInput` inherits):
  * `device`: one of `cpu`, `cuda` (default `cuda`).
  * `model_storage_directory`: supplied model-weight path; resolve every model asset from it.
* This example's input: **`prompt: str`**, **`negative_prompt: str = ""`**, **`seed: int`** (default: a random 32-bit value).
* This example's output: **`image: FileObject`**.
* **`FileObject`**: `data` (a local `Path`, an open binary file, or a URL) + `name`.

## Defining your own fields

1. Edit `TaskInput` / `TaskOutput` in `my_ai_lib/schemas.py`.
2. Update the stages in `my_ai_lib/pipeline.py` (and `run()` if needed) to use them.
3. Update the `TaskInput(...)` call in `preflight.py` to match.

## Notes

* Use **relative imports** for your own modules (`from .lib import helper`) so
  your code runs inside the sandbox.
* Allow exceptions to propagate so AIOZ AI can report them.
* Run `python preflight.py` before submitting.
