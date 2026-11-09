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