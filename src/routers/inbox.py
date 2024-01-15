from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import InboxSchema, AnsweredMessageSchema
import crud


inbox_router = APIRouter()

@inbox_router.get("/get-inbox", dependencies=[Depends(HTTPBearer())])
async def get_inbox(db: Session = Depends(get_db)):
    result = await crud.read_inbox(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@inbox_router.post("/add-inbox", dependencies=[Depends(HTTPBearer())])
async def add_inbox(inbox: InboxSchema, db: Session = Depends(get_db)):
    result = await crud.create_inbox(db=db, inbox=inbox)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
@inbox_router.post("/add-answered-message", dependencies=[Depends(HTTPBearer())])
async def add_answered_message(answer: AnsweredMessageSchema, db: Session = Depends(get_db)):
    result = await crud.create_answered_message(db=db, answer=answer)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED