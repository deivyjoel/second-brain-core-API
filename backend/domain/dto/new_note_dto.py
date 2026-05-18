from dataclasses import dataclass

@dataclass(frozen=True)
class NewNoteDTO:
    """DTO for transporting new note data to the repository."""
    name: str
    user_id: int
    theme_id: int | None



