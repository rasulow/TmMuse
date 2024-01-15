from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from models import PopUpSchema
from tokens import Returns
import crud

popup_router = APIRouter()

@popup_router.get("/get-popup", dependencies=[Depends(HTTPBearer())])
async def get_popup(page: int, db: Session = Depends(get_db)):
    result = await crud.read_popup(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
@popup_router.post("/add-popup", dependencies=[Depends(HTTPBearer())])
async def add_popup(popup: PopUpSchema, db: Session = Depends(get_db)):
    result = await crud.create_popup(db=db, popup=popup)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
@popup_router.put("/update-popup", dependencies=[Depends(HTTPBearer())])
async def update_popup(id: int, popup: PopUpSchema, db: Session = Depends(get_db)):
    result = await crud.update_popup(db=db, id=id, popup=popup)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
@popup_router.put("/add-popup-image", dependencies=[Depends(HTTPBearer())])
async def add_popup_image(id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.update_popup_image(db=db, id=id, file=file)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
@popup_router.delete("/delete-popup", dependencies=[Depends(HTTPBearer())])
async def delete_popup(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_popup(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED