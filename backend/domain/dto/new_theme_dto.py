from dataclasses import dataclass

@dataclass(frozen=True)
class NewThemeDTO:
    """DTO for transporting new theme data to the repository."""
    user_id: int
    name: str
    parent_id: int | None



