from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from backend.application.backend_api import BackendAPI
from backend.infrastructure.dependencies import get_api, get_current_user


router = APIRouter(prefix="/images", tags=["images"])


# --- Schemas ---
class RenameImageRequest(BaseModel):
    new_name: str

class MoveImageRequest(BaseModel):
    new_theme_id: int | None = None

class DeleteManyRequest(BaseModel):
    image_ids: list[int]


# --- Endpoints ---
@router.post("/")
async def create_image(name: str,
                       file: UploadFile = File(...),
                       theme_id: int | None = None,
                       user_id: int = Depends(get_current_user),
                       api: BackendAPI = Depends(get_api)):
    blob_data = await file.read()
    extension = file.filename.split(".")[-1].lower() if file.filename else ""
    result = api.create_image(user_id, name, blob_data, extension, theme_id)  
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"id": result.obj}


@router.delete("/")
def delete_many_images(body: DeleteManyRequest,  
                       user_id: int = Depends(get_current_user),
                       api: BackendAPI = Depends(get_api)):
    result = api.delete_many_images(user_id, body.image_ids)  
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.delete("/{image_id}")
def delete_image(image_id: int,
                 user_id: int = Depends(get_current_user),
                 api: BackendAPI = Depends(get_api)):
    result = api.delete_image(image_id, user_id)  
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return {"detail": result.info}


@router.patch("/{image_id}/rename")
def rename_image(image_id: int,
                 body: RenameImageRequest,
                 user_id: int = Depends(get_current_user),
                 api: BackendAPI = Depends(get_api)):
    result = api.rename_image(image_id, user_id, body.new_name)  
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.patch("/{image_id}/move")
def move_image_to_theme(image_id: int,
                        body: MoveImageRequest,
                        user_id: int = Depends(get_current_user),
                        api: BackendAPI = Depends(get_api)):
    result = api.move_image_to_theme(image_id, user_id, body.new_theme_id)  
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"detail": result.info}


@router.get("/root/")
def get_images_without_theme(user_id: int = Depends(get_current_user),
                              api: BackendAPI = Depends(get_api)):
    result = api.get_images_without_theme(user_id)  
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return result.obj


@router.get("/unique-name/")
def get_unique_image_name(name: str,
                          theme_id: int | None = None,
                          user_id: int = Depends(get_current_user),
                          api: BackendAPI = Depends(get_api)):
    result = api.get_unique_image_name(user_id, name, theme_id)  
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"name": result.obj}


@router.get("/by-theme/{theme_id}")
def list_images_by_theme(theme_id: int,
                         user_id: int = Depends(get_current_user),
                         api: BackendAPI = Depends(get_api)):
    result = api.list_images_by_theme(theme_id, user_id)  
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj


@router.get("/hierarchy/{theme_id}")
def get_image_ids_by_theme_hierarchy(theme_id: int,
                                     user_id: int = Depends(get_current_user),
                                     api: BackendAPI = Depends(get_api)):
    result = api.get_image_ids_by_theme_hierarchy(theme_id, user_id)  
    if not result.successful:
        raise HTTPException(status_code=400, detail=result.info)
    return {"ids": result.obj}


@router.get("/{image_id}/extension")
def get_image_extension(image_id: int,
                        user_id: int = Depends(get_current_user),
                        api: BackendAPI = Depends(get_api)):
    result = api.get_image_extension(image_id, user_id)  
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return {"extension": result.obj}


@router.get("/{image_id}")
def get_image_details(image_id: int,
                      user_id: int = Depends(get_current_user),
                      api: BackendAPI = Depends(get_api)):
    result = api.get_image_details(image_id, user_id)  
    if not result.successful:
        raise HTTPException(status_code=404, detail=result.info)
    return result.obj