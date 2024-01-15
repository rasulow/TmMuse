from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import TicketFilterSchema, TicketStatusUpdateSchema, CineamaProfileSchema
import crud


ticket_router = APIRouter()

@ticket_router.post("/get-ticket", dependencies=[Depends(HTTPBearer())])
async def get_ticket(ticket: TicketFilterSchema, db: Session = Depends(get_db)):
    result = await crud.read_ticket(db=db, ticket=ticket)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@ticket_router.put("/ticket-status-update", dependencies=[Depends(HTTPBearer())])
async def ticket_status_update(id: int, ticket: TicketStatusUpdateSchema, db: Session = Depends(get_db)):
    result = await crud.update_ticket_status(db=db, id=id, ticket=ticket)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@ticket_router.get("/get-current-ticket", dependencies=[Depends(HTTPBearer())])
async def get_current_ticket(id: int, db: Session = Depends(get_db)):
    result = await crud.read_current_ticket(db=db, id=id)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@ticket_router.post("/get-cineme-profile", dependencies=[Depends(HTTPBearer())])
async def get_cineme_profile(cinema: CineamaProfileSchema, db: Session = Depends(get_db)):
    result = await crud.read_cineme_profile(db=db, cinema=cinema)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL