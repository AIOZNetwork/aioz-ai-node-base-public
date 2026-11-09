# models/

Put your model weights in this folder.

## How AIOZ AI finds them

At run time AIOZ AI sets **`model_storage_directory`** and passes it into
your submission. **Load your weights from that path:**

```python
from pathlib import Path

def load_model(model_storage_directory: Union[str, Path], device: Literal["cpu", "cuda"] = "cuda"):
    weights = Path(model_storage_directory) / "model.pt"   # <- relative to the given dir
    ...
```

Locally, `model_storage_directory` defaults to `./models`, so anything you drop
here is what your code will load during `python preflight.py`.

## Example layouts (per framework)

```
models/                         models/                     models/
├── model.pt        (PyTorch)   ├── model.onnx  (ONNX)      ├── saved_model/   (TF)
└── config.json                 └── labels.txt              │   ├── saved_model.pb
                                                            │   └── variables/
models/                         models/                     └── labels.txt
├── model.joblib   (sklearn)    ├── model.keras  (Keras)
└── scaler.pkl                  └── classes.json
```

Common weight/artifact files: `*.pt` `*.pth` (PyTorch) · `*.onnx` (ONNX) ·
`*.h5` `*.keras` / `saved_model/` (TF/Keras) · `*.pkl` `*.joblib` (scikit-learn) ·
`*.safetensors` + `config.json`/tokenizer files (Transformers).

## Notes

- This `README.md` keeps the folder in place. You can delete it once you add real
  weights, or leave it.
- Track large weights with Git LFS and package every required model asset before
  execution. The runtime operates offline. Read the packaged assets from
  `model_storage_directory`.
