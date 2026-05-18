from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from application.backend_api import BackendAPI
from backend.infrastructure.dependencies import get_api, get_current_user


router = APIRouter(prefix="/notes", tags=["notes"])


# --- Schemas ---
class CreateNoteRequest(BaseModel):
    name: str
    theme_id: int | None = None

class RenameNoteRequest(BaseModel):
    new_name: str

class MoveNoteRequest(BaseModel):
    new_theme_id: int | None = None

class UpdateNoteContentRequest(BaseModel):
    content: str

class RegisterTimeRequest(BaseModel):
    minutes: float


# --- Endpoints ---
@router.post("/")
def create_note(body: CreateNoteRequest,
                user_id: int = Depends(get_current_user),
                api: BackendAPI = Depends(get_api)):
    result = api.create_note(body.name, user_id, body.theme_id)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"id": result.obj}


@router.delete("/{note_id}")
def delete_note(note_id: int,
                user_id: int = Depends(get_current_user),
                api: BackendAPI = Depends(get_api)):
    result = api.delete_note(note_id)
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return {"detail": result.info}


@router.delete("/")
def delete_many_notes(note_ids: list[int],
                      user_id: int = Depends(get_current_user),
                      api: BackendAPI = Depends(get_api)):
    result = api.delete_many_notes(note_ids)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.patch("/{note_id}/rename")
def rename_note(note_id: int,
                body: RenameNoteRequest,
                user_id: int = Depends(get_current_user),
                api: BackendAPI = Depends(get_api)):
    result = api.rename_note(note_id, body.new_name)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.patch("/{note_id}/move")
def move_note_to_theme(note_id: int,
                       body: MoveNoteRequest,
                       user_id: int = Depends(get_current_user),
                       api: BackendAPI = Depends(get_api)):
    result = api.move_note_to_theme(note_id, body.new_theme_id)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.patch("/{note_id}/content")
def update_note_content(note_id: int,
                        body: UpdateNoteContentRequest,
                        user_id: int = Depends(get_current_user),
                        api: BackendAPI = Depends(get_api)):
    result = api.update_note_content(note_id, body.content)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.post("/{note_id}/time")
def register_time_to_note(note_id: int,
                           body: RegisterTimeRequest,
                           user_id: int = Depends(get_current_user),
                           api: BackendAPI = Depends(get_api)):
    result = api.register_time_to_note(note_id, body.minutes)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.get("/{note_id}")
def get_note_details(note_id: int,
                     user_id: int = Depends(get_current_user),
                     api: BackendAPI = Depends(get_api)):
    result = api.get_note_details(note_id)
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj


@router.get("/{note_id}/analytics")
def get_note_analytics(note_id: int,
                       user_id: int = Depends(get_current_user),
                       api: BackendAPI = Depends(get_api)):
    result = api.get_note_analytics(note_id)
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj


@router.get("/by-theme/{theme_id}")
def list_notes_by_theme(theme_id: int,
                        user_id: int = Depends(get_current_user),
                        api: BackendAPI = Depends(get_api)):
    result = api.list_notes_by_theme(theme_id)
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj


@router.get("/root/")
def get_notes_without_themes(user_id: int = Depends(get_current_user),
                              api: BackendAPI = Depends(get_api)):
    result = api.get_notes_without_themes()
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return result.obj


@router.get("/unique-name/")
def get_unique_note_name(name: str,
                         theme_id: int | None = None,
                         user_id: int = Depends(get_current_user),
                         api: BackendAPI = Depends(get_api)):
    result = api.get_unique_note_name(name, theme_id)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"name": result.obj}


@router.get("/hierarchy/{theme_id}")
def get_note_ids_by_theme_hierarchy(theme_id: int,
                                    user_id: int = Depends(get_current_user),
                                    api: BackendAPI = Depends(get_api)):
    result = api.get_note_ids_by_theme_hierarchy(theme_id)
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"ids": result.obj}