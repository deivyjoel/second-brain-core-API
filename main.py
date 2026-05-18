from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.application.web_api.note_requests import router as notes_router
from backend.application.web_api.theme_requests import router as themes_router
from backend.application.web_api.user_requests import router as users_router
from backend.application.web_api.image_requests import router as images_router

app = FastAPI(title="Second Brain API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(notes_router)
app.include_router(themes_router)
app.include_router(images_router)