from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import ConstantsSchema
import crud

constants_router = APIRouter()

@constants_router.post("/add-constant", dependencies=[Depends(HTTPBearer())])
async def add_constants(const: ConstantsSchema, db: Session = Depends(get_db)):
    result = await crud.create_constants(db=db, const=const)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
    
@constants_router.get("/get-constants", dependencies=[Depends(HTTPBearer())])
async def get_constants(page: int, db: Session = Depends(get_db)):
    result = await crud.read_constants(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@constants_router.put("/update-constant", dependencies=[Depends(HTTPBearer())])
async def update_constant(id: int, const: ConstantsSchema, db: Session = Depends(get_db)):
    result = await crud.update_constants(db=db, id=id, const=const)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@constants_router.delete("/delete-constant", dependencies=[Depends(HTTPBearer())])
async def delete_constant(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_constant(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED