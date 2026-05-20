from dataclasses import dataclass

@dataclass(frozen=True)
class NewImageDTO:
    """DTO for transporting new image data to the repository."""
    user_id: int
    name: str
    blob_data: bytes
    extension: str  # Extension of the image file, e.g., 'png', 'jpg'
    theme_id: int | None = None
