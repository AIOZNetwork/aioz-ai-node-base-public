"""Model definition stage.

Define your model architecture here.
"""

from pathlib import Path
from typing import Any, Literal, Optional, Union


def define_model(device: Literal["cpu", "cuda"] = "cpu") -> Any:
    """Define and return your model.

    This placeholder returns None. Replace it with your model architecture:

        import torch.nn as nn

        model = nn.Sequential(
            nn.Linear(10, 10),
            nn.ReLU(),
            nn.Linear(10, 2)
        )
        return model.to(device)
    """
    return None


def load_model(
    weight_dir: Optional[Union[str, Path]] = None,
    device: Literal["cpu", "cuda"] = "cpu",
) -> Any:
    """Load and return your model from a previous training checkpoint, placed on `device`.

    This placeholder has no model and returns None. Replace it, for example:

        import torch
        model = define_model(device) # or instantiate your model class directly
        if not weight_dir:
            return model

        weights_path = Path(weight_dir)
        if weights_path.is_dir():
            weights_path = weights_path / "last.pth"

        if weights_path.exists():
            checkpoint = torch.load(weights_path, map_location=device)
            if isinstance(checkpoint, dict) and "model" in checkpoint:
                model.load_state_dict(checkpoint["model"])
            else:
                model.load_state_dict(checkpoint)
        return model
    """
    print(f"Loading model from {weight_dir} (placeholder)")
    # return model
    return None
