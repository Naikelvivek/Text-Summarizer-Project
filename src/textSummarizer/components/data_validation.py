import os
from src.textSummarizer.logging import logger
from src.textSummarizer.entity import DataValidationConfig
from src.textSummarizer.utils.common import create_directories
from pathlib import Path


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        try:
            # Ensure the validation directory exists
            create_directories([str(self.config.root_dir)])

            dataset_dir = os.path.join("artifacts", "data_ingestion", "samsum_dataset")

            if not os.path.exists(dataset_dir):
                validation_status = False
                msg = f"Dataset directory not found: {dataset_dir}"
                status_path = str(self.config.status_file_path)
                os.makedirs(os.path.dirname(status_path), exist_ok=True)
                with open(status_path, 'w') as f:
                    f.write(msg)
                logger.info(msg)
                return False

            # Only consider directory names that match required items
            present_items = set(os.listdir(dataset_dir))
            required_items = set(self.config.all_files_present)

            missing = required_items - present_items
            validation_status = len(missing) == 0

            status_path = str(self.config.status_file_path)
            os.makedirs(os.path.dirname(status_path), exist_ok=True)
            with open(status_path, 'w') as f:
                if validation_status:
                    f.write("Validation status: True\nAll required files/directories are present.")
                    logger.info("All required files/directories are present.")
                else:
                    f.write(f"Validation status: False\nMissing: {sorted(list(missing))}")
                    logger.warning(f"Validation failed. Missing: {sorted(list(missing))}")

            return validation_status

        except Exception as e:
            raise e
