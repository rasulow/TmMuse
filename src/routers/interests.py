from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from models import InterestsSchema, InterestItemsSchema, UpdateInterestItemsSchema
from tokens import Returns
import crud


interest_router = APIRouter()

@interest_router.post("/add-interests", dependencies=[Depends(HTTPBearer())])
async def add_interests(interest: InterestsSchema, db: Session = Depends(get_db)):
    result = await crud.create_interest(db=db, interest=interest)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
    
@interest_router.post("/add-interest-items", dependencies=[Depends(HTTPBearer())])
async def add_interest_items(item: InterestItemsSchema, db: Session = Depends(get_db)):
    result = await crud.create_interest_items(db=db, item=item)
    if result:
        return Returns.INSERTED
    else:
        return Returns.NOT_INSERTED
    
    
@interest_router.get("/get-interests", dependencies=[Depends(HTTPBearer())])
async def get_interests(page: int, db: Session = Depends(get_db)):
    result = await crud.read_interests(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@interest_router.put("/update-interest", dependencies=[Depends(HTTPBearer())])
async def update_interests(id: int, interest: InterestsSchema, db: Session = Depends(get_db)):
    result = await crud.update_interest(db=db, id=id, interest=interest)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@interest_router.put("/update-interest-items", dependencies=[Depends(HTTPBearer())])
async def update_interest_items(id: int, item: UpdateInterestItemsSchema, db: Session = Depends(get_db)):
    result = await crud.update_interest_item(db=db, id=id, item=item)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@interest_router.delete("/delete-interest", dependencies=[Depends(HTTPBearer())])
async def delete_interest(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_interest(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED