"""AIOZ AI training entrypoint.

Wires the pipeline stages for a model training task. Adapt the stages to your model.
"""

import os

from .model import define_model, load_model
from .pipeline import evaluate_model, load_data, save_model, train_model
from .schemas import FileObject, TaskInput, TaskOutput


def run(input_obj: TaskInput) -> TaskOutput:
    try:
        """Mandatory entrypoint — DO NOT RENAME IT."""
        task_input = TaskInput.model_validate(input_obj.model_dump())

        # 1. Load data
        train_data, val_data = load_data(task_input.dataset_dir)

        # 2. Define or load model
        resume_path = None
        if task_input.weight_dir:
            for fname in ["last.pth", "best.pth", "model_weights.pth"]:
                cand = os.path.join(task_input.weight_dir, fname)
                if os.path.exists(cand):
                    resume_path = cand
                    break

        if resume_path:
            model = load_model(task_input.weight_dir, task_input.device)
        else:
            model = define_model(task_input.device)

        # 3. Train model
        train_metrics = train_model(
            model,
            train_data,
            epochs=task_input.epochs,
            batch_size=task_input.batch_size,
            learning_rate=task_input.learning_rate,
            model_storage_directory=task_input.model_storage_directory,
            weight_dir=task_input.weight_dir,
        )

        # 4. Evaluate model
        val_metrics = evaluate_model(model, val_data)

        # 5. Save model
        last_weight_file, best_weight_file = save_model(
            model, task_input.model_storage_directory
        )

        print(
            f"Training completed. Train Metrics: {train_metrics}. Validation Metrics: {val_metrics}."
        )

        output_obj = TaskOutput(
            weight_last=FileObject(
                data=last_weight_file, name=os.path.basename(last_weight_file.name)
            ),
            weight_best=FileObject(
                data=best_weight_file, name=os.path.basename(best_weight_file.name)
            ),
        )
    except Exception as e:
        raise Exception(e)

    return output_obj
