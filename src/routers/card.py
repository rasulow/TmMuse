from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
import crud
from models import CardUpdateSchema, CardInsertSchema, CardUserInboxSchema

card_router = APIRouter()

@card_router.post("/add-card", dependencies=[Depends(HTTPBearer())])
async def add_card(card: CardInsertSchema, db: Session = Depends(get_db)):
    result = await crud.create_card_user(db=db, card=card)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
@card_router.get("/get-card", dependencies=[Depends(HTTPBearer())])
async def get_card(page: int, db: Session = Depends(get_db)):
    result = await crud.read_card(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
@card_router.put("/update-card", dependencies=[Depends(HTTPBearer())])
async def update_card(id: int, card: CardUpdateSchema, db: Session = Depends(get_db)):
    result = await crud.update_card(db=db, id=id, card=card)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@card_router.delete("/delete-card", dependencies=[Depends(HTTPBearer())])
async def delete_card(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_card(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED
    
    
@card_router.post("/add-card-user-inbox", dependencies=[Depends(HTTPBearer())])
async def add_card_user_inbox(inbox: CardUserInboxSchema, db: Session = Depends(get_db)):
    result = await crud.create_card_user_inbox(db=db, inbox=inbox)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@card_router.get("/get-zero-status-cards", dependencies=[Depends(HTTPBearer())])
async def get_card_zero(db: Session = Depends(get_db)):
    result = await crud.read_zero_card_users(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
