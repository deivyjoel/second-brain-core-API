from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime

from backend.infrastructure.repositories.sql_alchemy.date_reference import get_utc_now


class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    mail: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255)) # En capa infrastructure se aplica hash.
    state: Mapped[bool] = mapped_column(default=True) # 1: activo, 0: inactivo

    themes = relationship('ThemeModel', back_populates='user')
    images = relationship('ImageModel', back_populates='user')
    notes = relationship('NoteModel', back_populates='user')
    times = relationship('TimeModel', back_populates='user')



class ThemeModel(Base):
    __tablename__ = 'theme'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    parent_id : Mapped[int | None] = mapped_column(ForeignKey("theme.id"))
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=get_utc_now
        )
    last_edited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now
    )
    state: Mapped[bool] = mapped_column(default=True) # 1: activo, 0: inactivo

    parent = relationship("ThemeModel", remote_side=[id], back_populates="children")
    children = relationship("ThemeModel", back_populates="parent")

    images = relationship("ImageModel", back_populates="theme")
    notes = relationship("NoteModel", back_populates="theme")
    user = relationship('UserModel', back_populates='themes')
    

class NoteModel(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    theme_id: Mapped[int | None] = mapped_column(ForeignKey("theme.id"))
    name: Mapped[str] = mapped_column(String(100))
    content: Mapped[str | None] 
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=get_utc_now
    )
    last_edited_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now
    )
    state: Mapped[bool] = mapped_column(default=True) # 1: activo, 0: inactivo

    theme = relationship("ThemeModel", back_populates="notes")
    times = relationship("TimeModel", back_populates="note")
    user = relationship('UserModel', back_populates='notes')


class TimeModel(Base):
    __tablename__ = 'time'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    note_id: Mapped[int] = mapped_column(ForeignKey("note.id"))
    minutes: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now
    )
    state: Mapped[bool] = mapped_column(default=True) # 1: activo, 0: inactivo

    note = relationship("NoteModel", back_populates="times")
    user = relationship('UserModel', back_populates='times')



"""Only saves file paths"""
class ImageModel(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    theme_id: Mapped[int | None] = mapped_column(ForeignKey("theme.id"))
    name: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=get_utc_now
    )
    state: Mapped[bool] = mapped_column(default=True) # 1: activo, 0: inactivo

    theme = relationship("ThemeModel", back_populates="images")
    user = relationship('UserModel', back_populates='images')