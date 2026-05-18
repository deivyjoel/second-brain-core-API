from dataclasses import dataclass

@dataclass(frozen=True)
class NewThemeDTO:
    """DTO for transporting new theme data to the repository."""
    name: str
    user_id: int
    parent_id: int | None



