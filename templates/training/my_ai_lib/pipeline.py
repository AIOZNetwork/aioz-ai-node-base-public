"""Task pipeline stages: load_data -> train -> evaluate -> save_model.

These stages ship as a runnable placeholder. Replace each stage's body with your
logic. Keep the stage boundaries or reshape them for your task.
"""

import io
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union


def load_data(dataset_dir: str) -> Tuple[Any, Any]:
    """Load and preprocess the dataset from `dataset_dir`.

    Placeholder: returns empty lists. Replace with actual data loading logic.
    """
    print(f"Loading dataset from {dataset_dir}")
    train_data = []
    val_data = []
    return train_data, val_data


def train_model(
    model: Any,
    train_data: Any,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    model_storage_directory: Union[str, Path],
    weight_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Train the model using the provided data.

    Placeholder: returns mock metrics and saves dummy weights. Replace with your training loop.
    """
    os.makedirs(model_storage_directory, exist_ok=True)
    if weight_dir:
        print(f"Resuming training from {weight_dir}")
    else:
        print("Starting training from scratch")
    print(
        f"Training for {epochs} epochs with batch_size={batch_size} and lr={learning_rate}"
    )
    return {"loss": 0.5, "accuracy": 0.85}


def evaluate_model(model: Any, val_data: Any) -> Dict[str, Any]:
    """Evaluate the model on validation data.

    Placeholder: returns mock metrics. Replace with your evaluation logic.
    """
    print("Evaluating model...")
    return {"val_loss": 0.6, "val_accuracy": 0.82}


def save_model(
    model: Any, model_storage_directory: Union[str, Path]
) -> Tuple[io.BufferedReader, io.BufferedReader]:
    """Save the trained model weights to `model_storage_directory` and return opened file objects."""
    os.makedirs(model_storage_directory, exist_ok=True)
    best_path = os.path.join(model_storage_directory, "best.pth")
    last_path = os.path.join(model_storage_directory, "last.pth")
    if not os.path.exists(best_path):
        with open(best_path, "wb") as f:
            f.write(b"dummy best model weights")
    if not os.path.exists(last_path):
        with open(last_path, "wb") as f:
            f.write(b"dummy last model weights")

    return open(last_path, "rb"), open(best_path, "rb")
