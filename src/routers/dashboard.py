from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from db import get_db
from tokens import Returns
import crud
from models import AnalyticsSchema


dashboard_router = APIRouter()

@dashboard_router.get('/dashboard', dependencies=[Depends(HTTPBearer())])
async def dashboard(db: Session = Depends(get_db)):
    user_count = crud.read_count_users(db=db)
    profile_count = crud.read_count_profiles(db=db)
    post_count = crud.read_count_posts(db=db)
    carduser_count = crud.read_count_card_users(db=db)
    
    profile_view = crud.read_profile_view_count(db=db)
    ads_view = crud.read_ads_view_count(db=db)
    app_visitors = crud.read_app_visitors_count(db=db)
    post_view = crud.read_post_view_count(db=db)
    slider_view = crud.read_slider_view_count(db=db)
    popup_view = crud.read_popup_view_count(db=db)
    
    profile_view_yesterday = crud.read_profile_view_count_yesterday(db=db)
    ads_view_yesterday = crud.read_ads_view_count_yesterday(db=db)
    app_visitors_yesterday = crud.read_app_visitors_count_yesterday(db=db)
    post_view_yesterday = crud.read_post_view_count_yesterday(db=db)
    slider_view_yesterday = crud.read_slider_view_count_yesterday(db=db)
    popup_view_yesterday = crud.read_popup_view_count_yesterday(db=db)
    
    result = {}
    # * Count information
    result["users"] = user_count
    result["profiles"] = profile_count
    result["posts"] = post_count
    result["card_users"] = carduser_count
    # * Todays statistics
    result["profile_view"] = profile_view
    result["ads_view"] = ads_view
    result["app_visitors"] = app_visitors
    result["post_view"] = post_view
    result["slider_view"] = slider_view
    result["popup_view"] = popup_view
    # * Tomorrow's statistics
    result["profile_view_yesterday"] = profile_view_yesterday
    result["ads_view_yesterday"] = ads_view_yesterday
    result["app_visitors_yesterday"] = app_visitors_yesterday
    result["post_view_yesterday"] = post_view_yesterday
    result["slider_view_yesterday"] = slider_view_yesterday
    result["popup_view_yesterday"] = popup_view_yesterday
    
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@dashboard_router.post("/analytics", dependencies=[Depends(HTTPBearer())])
async def alalytics(req: AnalyticsSchema, db: Session = Depends(get_db)):
    result = crud.read_analytics(db=db, req=req)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
