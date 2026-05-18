from backend.domain.errors.user_errors import (
    InvalidUserNameError,
    InvalidUserMailError,
    InvalidUserPasswordError,
)
from backend.domain.dto.new_user_dto import NewUserDTO


class User:
    __slots__ = ("_id", "_name", "_mail", "_password")

    def __init__(self, id: int, name: str, mail: str, password: str):
        self._id = id
        self._name = name
        self._mail = mail
        self._password = password

    # --- Creation ---
    @staticmethod
    def create(name: str, mail: str, password: str) -> NewUserDTO:
        clean_name = name.strip()
        if not clean_name:
            raise InvalidUserNameError("El nombre no puede estar vacío")

        clean_mail = mail.strip().lower()
        if not clean_mail or "@" not in clean_mail:
            raise InvalidUserMailError("El correo no es válido")

        if not password or len(password) < 8:
            raise InvalidUserPasswordError("La contraseña debe tener al menos 8 caracteres")

        return NewUserDTO(
            name=clean_name,
            mail=clean_mail,
            password=password
        )     

    # --- Changes ---
    def change_name(self, new_name: str) -> None:
        clean_name = new_name.strip()
        if not clean_name:
            raise InvalidUserNameError("El nombre no puede estar vacío")
        self._name = clean_name

    def change_password(self, new_password: str) -> None:
        if not new_password or len(new_password) < 8:
            raise InvalidUserPasswordError("La contraseña debe tener al menos 8 caracteres")
        self._password = new_password
