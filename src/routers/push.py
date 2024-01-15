from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from cloud_messaging.cloud_messaging import send_data, send_topic_to_card_user
from models import cloud_messaging_token, cloud_messaging_topic, cloud_messaging_data
from cloud_messaging import send_to_token, send_to_topic

push_router = APIRouter()

@push_router.post("/push-to-token", dependencies=[Depends(HTTPBearer())])
async def push_to_token(req: cloud_messaging_token):
    await send_to_token(request=req)
    
@push_router.post("/push-to-topic", dependencies=[Depends(HTTPBearer())])
async def push_to_topic(req: cloud_messaging_topic, db: Session = Depends(get_db)):
    await send_to_topic(request=req, db=db)
    
@push_router.post("/push-data", dependencies=[Depends(HTTPBearer())])
async def push_data(req: cloud_messaging_data, db: Session = Depends(get_db)):
    await send_data(request=req, db=db)
    
@push_router.post("/push-to-card-user", dependencies=[Depends(HTTPBearer())])
async def push_data(req: cloud_messaging_topic, db: Session = Depends(get_db)):
    await send_topic_to_card_user(request=req, db=db)
