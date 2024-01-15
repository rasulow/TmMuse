from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from fastapi.security import HTTPBearer
from models import BannersSchema
import crud

banner_router = APIRouter()

@banner_router.get("/get-banners", dependencies=[Depends(HTTPBearer())])
async def get_banners(page: int, profile_id: int = None, db: Session = Depends(get_db)):
    result = await crud.read_banner(db=db,page=page, profile_id=profile_id)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
@banner_router.post("/add-banner", dependencies=[Depends(HTTPBearer())])
async def add_banner(banner: BannersSchema, db: Session = Depends(get_db)):
    result = await crud.create_banner(db=db, banner=banner)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
    
@banner_router.put("/update-banner", dependencies=[Depends(HTTPBearer())])
async def update_banner(id: int, banner: BannersSchema, db: Session = Depends(get_db)):
    result = await crud.update_banner(db=db, banner=banner, id=id)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
@banner_router.put("/update-banner-image", dependencies=[Depends(HTTPBearer())])
async def update_image(id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.update_banner_image(db=db, id=id, file=file)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
@banner_router.delete("/delete-banner", dependencies=[Depends(HTTPBearer())])
async def delete_banner(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_banner(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED