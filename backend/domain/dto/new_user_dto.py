from dataclasses import dataclass

@dataclass(frozen=True)
class NewUserDTO:
    """DTO for transporting new user data to the repository."""
    name: str
    mail: str
    password: str

