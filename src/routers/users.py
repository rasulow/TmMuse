from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from tokens import Returns
from db import get_db
import crud

users_router = APIRouter()

@users_router.get("/get-users", dependencies=[Depends(HTTPBearer())])
async def get_users(page: int, db: Session = Depends(get_db)):
    result = crud.read_users(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@users_router.get("/get-user-name", dependencies=[Depends(HTTPBearer())])
async def get_user_name(db: Session = Depends(get_db)):
    result = await crud.read_user_name(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@users_router.get("/get-all-admin-users-cinema", dependencies=[Depends(HTTPBearer())])
async def get_all_cinema(db: Session = Depends(get_db)):
    result = await crud.read_admin_cinema(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL