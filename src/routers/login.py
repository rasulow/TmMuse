from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import LoginSchema, SignupSchema, AdminNotifSchema
from fastapi.security import HTTPBearer
import crud
import json

login_router = APIRouter()

@login_router.get("/get-admin-type")
async def get_admin_type(db: Session = Depends(get_db)):
    result = await crud.read_admin_type(db=db)
    if result:
        return Returns.object(result)
    f = open('json/admin_type.json')
    data = json.load(f)
    for i in data:
        type: str = i.get('type')
        created = crud.create_admin_type(db=db, txt=type)
        if not created:
            return Returns.NOT_INSERTED
    f.close()
    result = await crud.read_admin_type(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@login_router.post("/sign-up")
async def sign_up(req: SignupSchema, db: Session = Depends(get_db)):
    result = await crud.create_admin(db=db, req=req)
    if result:
        return Returns.object(result)
    else:
        return Returns.NOT_INSERTED

@login_router.post("/sign-in")
async def sign_in(req: LoginSchema, db: Session = Depends(get_db)):
    result = await crud.read_admin(db=db, username=req.username, password=req.password)
    if result:
        return Returns.object(result)
    else:
        return Returns.USER_NOT_FOUND
    
    
@login_router.put("/update-notif-token", dependencies=[Depends(HTTPBearer())])
async def update_notif_token(req: AdminNotifSchema, db: Session = Depends(get_db)):
    result = await crud.update_admin_notif_token(db=db, req=req)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED