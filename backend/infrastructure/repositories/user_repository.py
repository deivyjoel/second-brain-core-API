from log import logger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.infrastructure.repositories.sql_alchemy import models
from backend.infrastructure.errors.db import RepositoryError, UniqueConstraintViolation

from backend.domain.models.user import User
from backend.domain.dto.new_user_dto import NewUserDTO

class UserRepository():
    def __init__(self, session):
        self.session = session
        logger.info("UserRepository initialized successfully: %s", session)

    def _to_domain(self, obj: models.UserModel) -> User:
        """Converts database model to domain entity."""
        return User(
            id=obj.id,
            name=obj.name,
            mail=obj.mail,
            password=obj.password
        )

    # --- CRUD ---
    def add(self, user: NewUserDTO) -> int:
        obj = models.UserModel(
            name=user.name,
            mail=user.mail,
            password=user.password
        )
        try:
            self.session.add(obj)
            self.session.commit()
            logger.info("add_user(id=%s) [Success]", obj.id)
            return obj.id
        except IntegrityError as e:
            self.session.rollback()
            logger.exception("add_user(mail=%s) [IntegrityError - Possible duplicate]: %s", user.mail, e)
            raise UniqueConstraintViolation("unique_violation") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.exception("add_user(mail=%s) [SQLAlchemyError]: %s", user.mail, e)
            raise RepositoryError("db_error") from e
        except Exception as e:
            self.session.rollback()
            logger.exception("add_user(mail=%s) [Unexpected error]", user.mail)
            raise RepositoryError("unexpected_error") from e

    def update(self, user: User) -> None:
        user_obj = self.session.get(models.UserModel, user._id)
        if not user_obj:
            logger.warning("update_user(id=%s) [Not Found]", user._id)
            raise RepositoryError("not_found")

        user_obj.name = user._name
        user_obj.mail = user._mail
        user_obj.password = user._password

        try:
            self.session.commit()
            logger.info("update_user(id=%s) [Success]", user._id)
        except IntegrityError as e:
            self.session.rollback()
            logger.exception("update_user(id=%s) [IntegrityError]: %s", user._id, e)
            raise UniqueConstraintViolation("unique_violation") from e
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.exception("update_user(id=%s) [SQLAlchemyError]: %s", user._id, e)
            raise RepositoryError("db_error") from e
        except Exception as e:
            self.session.rollback()
            logger.exception("update_user(id=%s) [Unexpected error]", user._id)
            raise RepositoryError("unexpected_error") from e

    # --- QUERIES ---
    def get_by_id(self, user_id: int) -> User | None:
        try:
            obj = self.session.get(models.UserModel, user_id)
            logger.info("get_user_by_id(id=%s) [Success]", user_id)
            return self._to_domain(obj) if obj else None
        except SQLAlchemyError as e:
            logger.exception("get_user_by_id(id=%s) [SQLAlchemyError]: %s", user_id, e)
            raise RepositoryError("db_error") from e
        except Exception as e:
            self.session.rollback()
            logger.exception("get_user_by_id(id=%s) [Unexpected error]", user_id)
            raise RepositoryError("unexpected_error") from e

    def get_by_mail(self, mail: str) -> User | None:
        try:
            obj = self.session.query(models.UserModel).filter_by(mail=mail).first()
            logger.info("get_user_by_mail(mail=%s) [Success]", mail)
            return self._to_domain(obj) if obj else None
        except SQLAlchemyError as e:
            logger.exception("get_user_by_mail(mail=%s) [SQLAlchemyError]: %s", mail, e)
            raise RepositoryError("db_error") from e
        except Exception as e:
            self.session.rollback()
            logger.exception("get_user_by_mail(mail=%s) [Unexpected error]", mail)
            raise RepositoryError("unexpected_error") from e