from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from tokens import Returns
from db import get_db
from models import PostsSchema
import crud

posts_router = APIRouter()

@posts_router.get("/get-posts", dependencies=[Depends(HTTPBearer())])
async def get_posts(page: int, profile_id: int = None, db: Session = Depends(get_db)):
    result = await crud.read_posts(db=db, page=page, profile_id=profile_id)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
@posts_router.post("/add-posts", dependencies=[Depends(HTTPBearer())])
async def add_posts(post: PostsSchema, db: Session = Depends(get_db)):
    result = await crud.create_posts(db=db, post=post)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
    
@posts_router.put("/update-posts", dependencies=[Depends(HTTPBearer())])
async def update_posts(id: int, post: PostsSchema, db: Session = Depends(get_db)):
    result = await crud.update_posts(db=db, post=post, id=id)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    

@posts_router.put("/update-post-image", dependencies=[Depends(HTTPBearer())])
async def update_post_image(id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):
    result = await crud.update_post_image(db=db, id=id, file=file)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@posts_router.delete("/delete-post", dependencies=[Depends(HTTPBearer())])
async def delete_post(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_post(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED
    
    
@posts_router.get("/get-all-posts", dependencies=[Depends(HTTPBearer())])
async def get_all_posts(db: Session = Depends(get_db)):
    result = await crud.read_all_posts(db=db)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
