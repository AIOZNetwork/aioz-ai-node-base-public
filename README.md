# AIOZ AI Node Adapter

`aioz-ainode-adapter` defines the contract the contract for deploying AI models to
AIOZ AI. Authors use its schemas to describe task inputs and outputs, then expose a
`my_ai_lib.run` entrypoint through an official template.

## Installation

```bash
python -m pip install \
  "git+https://github.com/AIOZNetwork/aioz-ai-node-base-public.git@v1.1.0"
```

The adapter supports Python 3.10 and newer and installs Pydantic 2.4.2 as its runtime
dependency.

## Start from a template

Choose a template and follow its README for purpose, structure, and usage:

- [Challenge template](templates/challenge/README.md): submit models to AIOZ AI
  Challenges.
- [Inference template](templates/inference/README.md): create models on AIOZ AI.

Each template supplies the required package structure, schema module, `run`
entrypoint, model-loading stage, processing pipeline, dependency file, and preflight
check.

## Author contract

Keep the author package named `my_ai_lib` and expose a callable `my_ai_lib.run`.
The entrypoint receives one object derived from `InputObject` and returns one object
derived from `OutputObject`.

Define task-specific `TaskInput` and `TaskOutput` classes in the template schema
module. These classes inherit the adapter fields and add the fields required by the
task. Pydantic validates the resulting objects at the entrypoint boundary.

The fields on `TaskOutput` form the output key-value object. Wrap every file-valued
field in `FileObject` so the file can be identified and materialized correctly.

## Inputs

Every `InputObject` includes `device` and `model_storage_directory`.

`device` is either `cpu` or `cuda` and defaults to `cuda`. Use this value when placing
the model and its inputs on the selected execution device.

Place model weights and related assets in the selected template's `./models`
directory. During execution, `model_storage_directory` provides the path to those
packaged assets. Load every model resource through that supplied path so the model
remains portable across execution environments.

Task-specific input fields belong on the template's `TaskInput` subclass.

## Outputs and files

Task-specific output fields belong on the template's `TaskOutput` subclass. Return a
fully populated `TaskOutput` from `my_ai_lib.run`.

`FileObject.data` accepts an open binary file, a local `Path`, or a URL. A local
`Path` provides the simplest form for a file produced during the task. When using an
open binary file, keep the handle readable through the return from `run`.

Set `FileObject.name` to the filename presented with the output. Use a clear extension
that matches the file content.

## Dependencies and model weights

Add every model-specific Python dependency to the selected template's
`requirements.txt`. Pin dependency versions so clean builds resolve the same runtime
environment.

Store model weights under the template's `./models` directory before packaging or
submission. In author code, resolve those files relative to
`model_storage_directory`. Keep source code independent from machine-specific paths.

## Preflight

Run the selected template's preflight from that template directory before packaging
or submission:

```bash
python preflight.py
```

Preflight imports `my_ai_lib`, validates the schema and entrypoint contract, executes
the sample task, and checks the resulting output artifact.

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 AIOZ Network.
