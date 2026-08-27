"""Task pipeline stages: preprocess -> predict -> postprocess.

These stages ship as a runnable placeholder that tallies the files in the input
folder, so `python preflight.py` works out of the box. Replace each stage's body
with your logic. Keep the stage boundaries or reshape them for your task.
"""

import csv
import os
from pathlib import Path
from typing import Any, List, Tuple


def preprocess(input_folder: str) -> List[str]:
    """Turn the raw input into model-ready samples.

    Placeholder: collect every file path under `input_folder`.
    """
    samples: List[str] = []
    for root, _, files in os.walk(input_folder):
        for name in files:
            samples.append(os.path.join(root, name))
    return samples


def predict(model: Any, samples: List[str]) -> List[Tuple[str, int]]:
    """Run the model over the samples and return raw predictions.

    Placeholder: return each file's byte size as its prediction.
    """
    predictions: List[Tuple[str, int]] = []
    for path in samples:
        # pred = model.predict(path)   # <- your real prediction goes here
        predictions.append((os.path.basename(path), os.path.getsize(path)))
    return predictions


def postprocess(predictions: List[Tuple[str, int]], output_path: Path = Path("result.csv")) -> Path:
    """Turn predictions into your output file and return its path.

    Placeholder: write the predictions to result.csv.
    """
    with output_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file_name", "size_bytes"])
        writer.writerows(predictions)
    return output_path