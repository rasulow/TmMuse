from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from fastapi.security import HTTPBearer
import crud
import json

category_router = APIRouter()

@category_router.get("/get-categories", dependencies=[Depends(HTTPBearer())])
async def get_category(db: Session = Depends(get_db)):
    result = await crud.read_categories(db=db)
    if result:
        return Returns.object(result)
    f = open("json/category.json")
    data = json.load(f)
    for i in data:
        name: str = i.get("name")
        created = await crud.create_category(db=db, name=name)
        if not created:
            return Returns.NOT_INSERTED
    f.close()
    result = await crud.read_categories(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL