from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from fastapi.security import HTTPBearer
import crud
from typing import List
from models import addProfiles, PhoneNumberSchema, TagsSchema
import json


profile_router = APIRouter()

@profile_router.get("/get-profile", dependencies=[Depends(HTTPBearer())])
async def get_profile(page: int, category: int = 0, db: Session = Depends(get_db)):
    if page == 0:
        return Returns.NULL
    result = await crud.read_profile(db=db, category=category, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
@profile_router.get("/get-name-profile", dependencies=[Depends(HTTPBearer())])
async def get_name_profile(db: Session = Depends(get_db)):
    result = await crud.read_name_profile(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@profile_router.post("/add-profile", dependencies=[Depends(HTTPBearer())])
async def add_profile(profile: addProfiles, db: Session = Depends(get_db)):
    result = await crud.create_profile(db=db, profile=profile)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED
    

@profile_router.put("/update-profile", dependencies=[Depends(HTTPBearer())])
async def update_profile(id: int, req: addProfiles, db: Session = Depends(get_db)):
    result = await crud.update_profile(db=db, req=req, id=id)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@profile_router.post("/add-phone-number", dependencies=[Depends(HTTPBearer())])
async def add_phone_number(phone: PhoneNumberSchema, db: Session = Depends(get_db)):
    result = await crud.create_phone_numbers(db=db, phone=phone)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@profile_router.delete("/delete-phone-number", dependencies=[Depends(HTTPBearer())])
async def delete_phone_number(phone: str = None, db: Session = Depends(get_db)):
    result = await crud.delete_phone_number(db=db, phone=phone)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED
    
    
@profile_router.post("/add-tags", dependencies=[Depends(HTTPBearer())])
async def add_tags(tag: TagsSchema, db: Session = Depends(get_db)):
    result = await crud.create_tags(db=db, tag=tag)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@profile_router.post("/add-sliders", dependencies=[Depends(HTTPBearer())])
async def add_sliders(
        profile_id: int, 
        db: Session = Depends(get_db), 
        file1: List[UploadFile] = File(...),
        file2: List[UploadFile] = File(...)):
    result = await crud.create_sliders(db=db, profile_id=profile_id, file1=file1, file2=file2)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED


@profile_router.post("/add-galleries", dependencies=[Depends(HTTPBearer())])
async def add_galleries(
        profile_id: int, 
        db: Session = Depends(get_db), 
        file1: List[UploadFile] = File(...),
        file2: List[UploadFile] = File(...)):
    result = await crud.create_galleries(db=db, profile_id=profile_id, file1=file1, file2=file2)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@profile_router.post("/add-vr-large-image", dependencies=[Depends(HTTPBearer())])
async def add_vr_large_image(profile_id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.create_vr_large_image(db=db, profile_id=profile_id, file=file)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
@profile_router.put("/add-vr-small-image", dependencies=[Depends(HTTPBearer())])
async def add_vr_small_image(profile_id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.create_vr_small_image(db=db, profile_id=profile_id, file=file)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
@profile_router.delete('/delete-slider', dependencies=[Depends(HTTPBearer())])
async def delete_slider(type: str, id: int, db: Session = Depends(get_db)):
    result = await crud.delete_slider(db=db, type=type, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED
    
    
@profile_router.delete("/delete-profile", dependencies=[Depends(HTTPBearer())])
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    result = await crud.delete_profile(db=db, profile_id=profile_id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED