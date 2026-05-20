from log import logger
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from backend.infrastructure.repositories._image_storage import ImageStorage, ImageStorageError
from backend.infrastructure.repositories.sql_alchemy import models
from backend.infrastructure.errors.db import RepositoryError, UniqueConstraintViolation

from backend.domain.models.image import Image 
from backend.domain.dto.new_image_dto import NewImageDTO

class ImageRepository():
    def __init__(self, session):
        self.session = session
        self.image_store = ImageStorage()
        logger.info("ImageRepository initialized successfully: %s", session)

    def _to_domain(self, img: models.ImageModel) -> Image:
        return Image(
            id=img.id,
            user_id = img.user_id,
            name=img.name,
            file_path=img.file_path,
            theme_id=img.theme_id,
            created_at=img.created_at
        )

    # --- CRUD ---
    def add(self, image: NewImageDTO) -> int:
        file_path = None
        is_committed = False
        try:
            file_path = self.image_store.save(
                name=image.name,
                extension=image.extension,
                blob_data=image.blob_data
            )
            obj = models.ImageModel(
                user_id = image.user_id,
                name=image.name,
                file_path=file_path, 
                theme_id=image.theme_id
            )
            self.session.add(obj)
            self.session.commit()
            is_committed = True
            logger.info("add_image(id=%s, user_id=%s) [Success]", obj.id, obj.user_id)
            return obj.id

        except ImageStorageError as e:
            logger.exception("add_image(name=%s, user_id=%s) [StorageError]: %s", image.name, image.user_id, e)
            raise RepositoryError("file_error") from e

        except IntegrityError as e:
            self.session.rollback()
            logger.exception("add_image(name=%s, user_id=%s) [IntegrityError]: %s", image.name, image.user_id, e)
            raise UniqueConstraintViolation("unique_violation") from e
        
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.exception("add_image(name=%s, user_id=%s) [SQLAlchemyError]: %s", image.name, image.user_id, e)
            raise RepositoryError("db_error") from e
        
        finally:
            if not is_committed and file_path:
                self.image_store.undo_save(file_path)


    def delete(self, image_id: int, user_id: int) -> None:
        image_obj = self.session.query(models.ImageModel).filter(
            models.ImageModel.id == image_id,
            models.ImageModel.user_id == user_id,
            models.ImageModel.state == True
        ).first()
        if not image_obj:
            logger.warning("delete_image(id=%s, user_id=%s) [Not found]", image_id, user_id)
            raise RepositoryError("not_found")

        try:
            image_obj.state = False
            self.session.commit()
            logger.info("delete_image(id=%s, user_id=%s) [Success]", image_id, user_id)

        except ImageStorageError as e:
            logger.exception("delete_image(id=%s, user_id=%s) [StorageError]: %s", image_id, user_id, e)
            raise RepositoryError("file_error") from e
        
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.exception("delete_image(id=%s, user_id=%s) [SQLAlchemyError]: %s", image_id, user_id, e)
            raise RepositoryError("db_error") from e
        
        except Exception as e:
            self.session.rollback()
            logger.exception("delete_image(id=%s, user_id=%s) [Unexpected error]", image_id, user_id)
            raise RepositoryError("unexpected_error") from e


    def update(self, image: Image) -> None:
        image_obj = self.session.query(models.ImageModel).filter(
            models.ImageModel.id == image._id,
            models.ImageModel.user_id == image._user_id,
            models.ImageModel.state == True
        ).first()
        if not image_obj:
            logger.warning("update_image(id=%s, user_id=%s) [Not found]", image._id, image._user_id)
            raise RepositoryError("not_found")

        image_obj.name = image._name
        image_obj.theme_id = image._theme_id

        try:
            self.session.commit()
            logger.info("update_image(id=%s, user_id=%s) [Success]", image._id, image._user_id)

        except IntegrityError as e:
            self.session.rollback()
            logger.exception("update_image(id=%s, user_id=%s) [IntegrityError]: %s", image._id, image._user_id, e)
            raise UniqueConstraintViolation("unique_violation") from e
        
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.exception("update_image(id=%s, user_id=%s) [SQLAlchemyError]: %s", image._id, image._user_id, e)
            raise RepositoryError("db_error") from e

    def delete_many(self, image_ids: list[int], user_id: int) -> None:
        if not image_ids:
            return
        
        try:
            stmt = (
                update(models.ImageModel).where(
                    models.ImageModel.id.in_(image_ids),
                    models.ImageModel.user_id == user_id,
                    models.ImageModel.state == True
                ).values(state=False)
            )
            self.session.execute(stmt)
            self.session.commit()
            logger.info("delete_many_images(ids=%s, user_id=%s) [Success]", image_ids, user_id)  # ✅ bug corregido

        except ImageStorageError as e:
            logger.exception("delete_many_images(ids=%s, user_id=%s) [StorageError]: %s", image_ids, user_id, e)
            raise RepositoryError("file_error") from e
    
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.exception("delete_many_images(user_id=%s) [SQLAlchemyError]: %s", user_id, e)  # ✅ nombre corregido
            raise RepositoryError("db_error") from e
        except Exception as e:
            self.session.rollback()
            logger.exception("delete_many_images(user_id=%s) [Unexpected error]", user_id)  # ✅ nombre corregido
            raise RepositoryError("unexpected_error") from e


    # --- QUERIES ---
    def get_by_id(self, image_id: int, user_id: int) -> Image | None:
        try:
            obj = self.session.query(models.ImageModel).filter(
                models.ImageModel.id == image_id,
                models.ImageModel.user_id == user_id,
                models.ImageModel.state == True
            ).first()
            logger.info("get_image_by_id(id=%s, user_id=%s) [Success]", image_id, user_id)
            return self._to_domain(obj) if obj else None
        
        except SQLAlchemyError as e:
            logger.exception("get_image_by_id(id=%s, user_id=%s) [SQLAlchemyError]: %s", image_id, user_id, e)
            raise RepositoryError("db_error") from e
        
    def _query_images(self, **filters) -> list[Image]:
        try:
            objs = self.session.query(models.ImageModel).filter_by(**filters).all()
            logger.info("query_images(filters=%s) [Success] - %d images found", filters, len(objs))
            return [self._to_domain(obj) for obj in objs]
        
        except SQLAlchemyError as e:
            logger.exception("query_images(filters=%s) [SQLAlchemyError]: %s", filters, e)
            raise RepositoryError("db_error") from e

    def get_all_images(self, user_id: int):
        return self._query_images(user_id = user_id, state=True)

    def get_images_by_theme_id(self, theme_id: int, user_id: int):
        return self._query_images(theme_id=theme_id, user_id = user_id, state=True)

    def get_images_without_theme_id(self, user_id: int):
        return self._query_images(theme_id=None, user_id=user_id, state=True)