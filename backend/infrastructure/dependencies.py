from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from backend.infrastructure.repositories.sql_alchemy import models
from backend.infrastructure.repositories.note_repository import NoteRepository
from backend.infrastructure.repositories.theme_repository import ThemeRepository
from backend.infrastructure.repositories.analytics_repository import AnalyticsRepository
from backend.infrastructure.repositories.search_efficiency_repository import SearchEfficiencyRepository
from backend.infrastructure.repositories.image_repository import ImageRepository
from backend.infrastructure.repositories.user_repository import UserRepository
from backend.application.backend_api import BackendAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY no está definida en el .env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # type: ignore
    return payload["user_id"]


engine = create_engine('sqlite:///app.db', echo=False)
models.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()

def get_api(session=Depends(get_db)) -> BackendAPI:
    nt_repo = NoteRepository(session)
    thm_repo = ThemeRepository(session)
    usr_repo = UserRepository(session)
    an_repo = AnalyticsRepository(session)
    sc_repo = SearchEfficiencyRepository(session)
    img_repo = ImageRepository(session)
    return BackendAPI(nt_repo, thm_repo, usr_repo, an_repo, sc_repo, img_repo)