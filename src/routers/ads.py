from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from models import AdsSchema
from tokens import Returns
import crud

ads_router = APIRouter()

@ads_router.get("/get-ads", dependencies=[Depends(HTTPBearer())])
async def get_ads(page: int, db: Session = Depends(get_db)):
    result = await crud.read_ads(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@ads_router.post("/add-ads", dependencies=[Depends(HTTPBearer())])
async def add_ads(ads: AdsSchema, db: Session = Depends(get_db)):
    result = await crud.create_ads(db=db, ads=ads)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
@ads_router.put("/update-ads", dependencies=[Depends(HTTPBearer())])
async def update_ads(id: int, ads: AdsSchema, db: Session = Depends(get_db)):
    result = await crud.update_ads(db=db, id=id, ads=ads)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
@ads_router.delete("/delete-ads", dependencies=[Depends(HTTPBearer())])
async def delete_ads(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_ads(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED
    
@ads_router.put("/update-ads-image", dependencies=[Depends(HTTPBearer())])
async def update_image(id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.update_ads_image(db=db, id=id, file=file)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED