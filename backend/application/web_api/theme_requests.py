from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.application.backend_api import BackendAPI
from backend.infrastructure.dependencies import get_api, get_current_user


router = APIRouter(prefix="/themes", tags=["themes"])


# --- Schemas ---
class CreateThemeRequest(BaseModel):
    name: str
    parent_id: int | None = None

class RenameThemeRequest(BaseModel):
    new_name: str

class MoveThemeRequest(BaseModel):
    new_parent_id: int | None = None

class DeleteManyRequest(BaseModel):
    theme_ids: list[int]


# --- Endpoints ---
@router.post("/")
def create_theme(body: CreateThemeRequest,
                 user_id: int = Depends(get_current_user),
                 api: BackendAPI = Depends(get_api)):
    result = api.create_theme(user_id, body.name, body.parent_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"id": result.obj}


@router.delete("/")
def delete_many_themes(body: DeleteManyRequest,  # ✅ schema Pydantic
                       user_id: int = Depends(get_current_user),
                       api: BackendAPI = Depends(get_api)):
    result = api.delete_many_themes(user_id, body.theme_ids)  # ✅
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.delete("/{theme_id}")
def delete_theme(theme_id: int,
                 user_id: int = Depends(get_current_user),
                 api: BackendAPI = Depends(get_api)):
    result = api.delete_theme(theme_id, user_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return {"detail": result.info}


@router.patch("/{theme_id}/rename")
def rename_theme(theme_id: int,
                 body: RenameThemeRequest,
                 user_id: int = Depends(get_current_user),
                 api: BackendAPI = Depends(get_api)):
    result = api.rename_theme(theme_id, user_id, body.new_name)  # ✅
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.patch("/{theme_id}/move")
def move_theme(theme_id: int,
               body: MoveThemeRequest,
               user_id: int = Depends(get_current_user),
               api: BackendAPI = Depends(get_api)):
    result = api.move_theme(theme_id, user_id, body.new_parent_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.get("/root/")
def list_root_themes(user_id: int = Depends(get_current_user),
                     api: BackendAPI = Depends(get_api)):
    result = api.list_root_themes(user_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return result.obj


@router.get("/unique-name/")
def get_unique_theme_name(name: str,
                          theme_id: int | None = None,
                          user_id: int = Depends(get_current_user),
                          api: BackendAPI = Depends(get_api)):
    result = api.get_unique_theme_name(user_id, name, theme_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"name": result.obj}


@router.get("/")
def list_themes(user_id: int = Depends(get_current_user),
                api: BackendAPI = Depends(get_api)):
    result = api.list_themes(user_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return result.obj


@router.get("/{theme_id}/analytics")
def get_theme_analytics(theme_id: int,
                        user_id: int = Depends(get_current_user),
                        api: BackendAPI = Depends(get_api)):
    result = api.get_theme_analytics(theme_id, user_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj


@router.get("/{theme_id}/descendants")
def get_themes_descendants(theme_id: int,
                           user_id: int = Depends(get_current_user),
                           api: BackendAPI = Depends(get_api)):
    result = api.get_themes_descendants(theme_id, user_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return {"ids": result.obj}


@router.get("/{theme_id}/children")
def list_child_themes(theme_id: int,
                      user_id: int = Depends(get_current_user),
                      api: BackendAPI = Depends(get_api)):
    result = api.list_child_themes(theme_id, user_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj


@router.get("/{theme_id}")
def get_theme_details(theme_id: int,
                      user_id: int = Depends(get_current_user),
                      api: BackendAPI = Depends(get_api)):
    result = api.get_theme_details(theme_id, user_id)  # ✅
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj