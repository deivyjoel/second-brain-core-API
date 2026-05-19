from log import logger
import os
from datetime import datetime
import re

class ImageStorageError(Exception):
    """Base exception for image storage errors."""
    pass

class ImageStorage:
    def __init__(self, upload_dir: str = "_uploads/images/", trash_dir: str = "_uploads/trash/"):
        self.upload_dir = upload_dir
        self.trash_dir = trash_dir

        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.trash_dir, exist_ok=True)

    # ---------- helpers ----------
    def _generate_filename(self, name: str, extension: str) -> str:
        """Cleans the name and appends a timestamp to ensure uniqueness."""
        clean_name = re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{clean_name}_{timestamp}.{extension.lower().replace('.', '')}"

    def save(self, *, name: str, extension: str, blob_data: bytes) -> str:
        """Saves an image to disk and returns the full file path."""
        filename = self._generate_filename(name, extension)
        full_path = os.path.join(self.upload_dir, filename)

        try:
            with open(full_path, "wb") as f:
                f.write(blob_data)
            return full_path
        except OSError as e:
            raise ImageStorageError("file_write_error") from e


    # Compensation methods (Rollback)
    def undo_save(self, file_path: str) -> None:
        """Permanently deletes a file (useful if the DB transaction fails after saving)."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError as e:
            logger.critical(f"File rollback failed: Could not delete {file_path}: {e}")
 
