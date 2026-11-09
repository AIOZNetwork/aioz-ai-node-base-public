"""Model loading stage.

Load your weights once, here, and reuse the returned object for every
prediction. Read weights from `model_storage_directory` (AIOZ AI sets it);
never hard-code a path.
"""

from pathlib import Path
from typing import Any, Literal, Union


def load_model(
    model_storage_directory: Union[str, Path],
    device: Literal["cpu", "cuda"] = "cuda",
) -> Any:
    """Load and return your model, placed on `device`.

    This placeholder has no model and returns None. Replace it, for example:

        weights = Path(model_storage_directory) / "weights.pt"
        model = MyNet()
        model.load_state_dict(torch.load(weights, map_location=device))
        model.to(device).eval()
        return model
    """
    return None
