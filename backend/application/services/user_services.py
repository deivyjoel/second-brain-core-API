from backend.infrastructure.repositories.user_repository import UserRepository
from passlib.hash import bcrypt


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str):
        return bcrypt.hash(password)
    
    def verify_pasword(self, password, password_hash):
        return bcrypt.verify(password, password_hash)

