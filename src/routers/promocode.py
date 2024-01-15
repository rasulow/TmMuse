from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from tokens import Returns
from models import PromoCodeSchema, PromoCodeStatusSchema
from db import get_db
import crud

promocode_router = APIRouter()

@promocode_router.post("/add-promo-code", dependencies=[Depends(get_db)])
async def add_promo_code(promo: PromoCodeSchema, db: Session = Depends(get_db)):
    result = await crud.create_promo_codes(db=db, promo=promo)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
    
@promocode_router.get("/get-promo-codes", dependencies=[Depends(HTTPBearer())])
async def get_promo_codes(page: int, db: Session = Depends(get_db)):
    result = await crud.read_promo_codes(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@promocode_router.put("/update-promo-code", dependencies=[Depends(HTTPBearer())])
async def update_promo_code(id: int, promo: PromoCodeSchema, db: Session = Depends(get_db)):
    result = await crud.update_promo_code(db=db, id=id, promo=promo)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@promocode_router.put("/update-promo-code-status", dependencies=[Depends(HTTPBearer())])
async def update_promo_code_status(id: int, promo: PromoCodeStatusSchema, db: Session = Depends(get_db)):
    result = await crud.update_promo_code_status(db=db, id=id, promo=promo)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@promocode_router.delete("/delete-promo-code", dependencies=[Depends(HTTPBearer())])
async def delete_promo_code(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_promo_code(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED