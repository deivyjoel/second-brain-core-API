from backend.infrastructure.repositories.user_repository import UserRepository

from backend.application.decorators.usecase_guard import handle_usecase_errors
from backend.application.results.operation_result import OperationResult
from backend.application.services.user_services import UserService

from backend.domain.models.user import User
from backend.domain.dto.new_user_dto import NewUserDTO



# --- OPERATIONS ---
@handle_usecase_errors
def login_user(user_repo: UserRepository,
                email: str,
                password: str,
                user_service: UserService
                ) -> OperationResult:
    user = user_repo.get_by_mail(email)
    if not user:
        return OperationResult(False, "Credenciales inválidas", None)
    
    if not user_service.verify_pasword(password, user._password):
        return OperationResult(False, "Credenciales inválidas", None)

    return OperationResult(True, "Usuario logueado correctamente", user._id)


@handle_usecase_errors
def register_user(user_repo: UserRepository,
                  name: str,
                  email: str,
                  password: str,
                  user_service: UserService
                  ) -> OperationResult[int]:
    user_with_e = user_repo.get_by_mail(email)
    if user_with_e is not None:
        return OperationResult(False, "El email ya está registrado", None)
    
    pass_hashed = user_service.hash_password(password)
    user: NewUserDTO = User.create(name, email, pass_hashed)
    user_id = user_repo.add(user)
    return OperationResult(True, "Registro creado exitosamente", user_id)

