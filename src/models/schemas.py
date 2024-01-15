from lib2to3.pgen2 import token
from fastapi import status
from pydantic import BaseModel
from typing import List, Optional

class LoginSchema(BaseModel):
    username : str
    password : str
    
    class Config:
        orm_mode = True
        
class SignupSchema(LoginSchema):
    type     : int
    
    class Config:
        orm_mode = True    
        

class addProfiles(BaseModel):
    nameTM              : str
    nameRU              : str
    short_descTM        : str
    short_descRU        : str
    like                : int = 0
    dislike             : int = 0
    instagram           : str
    site                : str
    location            : str
    address             : str
    is_cash             : bool
    is_terminal         : bool
    work_hours          : str
    delivery            : bool
    cousineTM           : str
    cousineRU           : str
    average_check       : float
    is_active_card      : bool
    tm_muse_card        : float
    is_certificate      : bool
    is_promo            : bool = False
    is_VIP              : int
    WiFi                : bool = False
    status              : int = 0
    category_id         : int = 1
    view_count          : int = 0
    promo_count         : int = 0
    cinema_id           : int = 1
    descriptionTM       : str
    descriptionRU       : str
    order_in_list       : int = 0
    free_time           : str
    own_promotion       : float
    required_promotion  : bool
    
    class Config:
        orm_mode = True
        
        

class PhoneNumberSchema(BaseModel):
    profile_id    : int
    phone_numbers : List[str]
    
    class Config:
        orm_mode = True
        

class TagsSchema(BaseModel):
    profile_id     : int
    category_id    : int
    tagTM          : List[str]
    tagRU          : List[str]
    
    class Config:
        orm_mode = True

        
class BannersSchema(BaseModel):
    link             : str
    order            : int
    profile_id       : int = None
    comment_of_admin : str
    
    class Config:
        orm_mode = True
        
class AdsSchema(BaseModel):
    nameTM           : str
    nameRU           : str
    comment_of_admin : str
    is_main          : bool = False
    site_url         : str
    profile_id       : int
    
    class Config:
        orm_mode = True
        
class PostsSchema(BaseModel):
    titleTM          : str
    titleRU          : str
    promotion        : float
    profile_id       : int
    descriptionTM    : str
    descriptionRU    : str
    comment_of_admin : str
    status           : bool
    
    class Config:
        orm_mode = True
        
class PopUpSchema(BaseModel):
    comment_of_admin    : str
    site_url            : str
    titleTM             : str
    titleRU             : str
    descriptionTM       : str
    descriptionRU       : str
    profile_id          : int
    
    class Config:
        orm_mode = True
        

class CardUserInboxSchema(BaseModel):
    title               : str
    message             : str
    
    class Config:
        orm_mode = True
        
                
class InboxSchema(CardUserInboxSchema):
    is_all              : bool
    user_id             : int
    
    class Config:
        orm_mode = True


class AnsweredMessageSchema(BaseModel):
    title               : str
    message             : str
    inbox_id            : int
    
    class Config:
        orm_mode = True
        
        
class CertificateSchema(BaseModel):
    amount              : float
    status              : int
    profile_id          : int
    user_id             : int
    
    class Config:
        orm_mode = True
        
        
class CertificateStatusSchema(BaseModel):
    status              : int
    
    class Config:
        orm_mode = True
        

class PromoCodeSchema(BaseModel):
    promo_code          : str
    status              : int
    profile_id          : int
    user_id             : int
    
    class Config:
        orm_mode = True
        
class PromoCodeStatusSchema(BaseModel):
    status              : int
    
    class Config:
        orm_mode = True
        
        
class cloud_messaging_topic(BaseModel):
    title               : str
    body                : str
    
    class Config:
        orm_mode = True
        
class cloud_messaging_token(cloud_messaging_topic):
    token               : str
    
    class Config:
        orm_mode = True
        
class cloud_messaging_data(cloud_messaging_topic):
    profile_id          : str
    category_id         : str
    
    class Config:
        orm_mode = True
        
        
class ConstantsSchema(BaseModel):
    titleTM             : str
    titleRU             : str
    contentTM           : str
    contentRU           : str
    contentTM_dark      : str
    contentRU_dark      : str
    type                : str
    
    class Config:
        orm_mode = True
        
        
class InterestsSchema(BaseModel):
    titleTM             : str
    titleRU             : str
    
    class Config:
        orm_mode = True
        


class UpdateInterestItemsSchema(BaseModel):
    titleTM             : List[str]
    titleRU             : List[str]
    
    class Config:
        orm_mode = True   

      
class InterestItemsSchema(UpdateInterestItemsSchema):
    interest_id         : int
    
    class Config:
        orm_mode = True
        

        

class CardUpdateSchema(BaseModel):
    date_of_birth       : str
    gender              : int
    email               : str
    is_sms              : bool
    status              : int
    card_id             : str
    expired             : str
    
    class Config:
        orm_mode = True
        
        
class CardInsertSchema(CardUpdateSchema):
    fullname            : str
    phone_number        : str
    
    class Config:
        orm_mode = True
        
        
class AnalyticsSchema(BaseModel):
    type                : str = None
    start_date          : str = None
    end_date            : str = None
    profile_id          : int = None
    
    class Config:
        orm_mode = True
        
        
class TicketFilterSchema(BaseModel):
    cinema_id           : int = None
    status              : int = None
    movie_date          : str = None
    profile_id          : int = None
    
    class Config:
        orm_mode = True
        
        
class TicketStatusUpdateSchema(BaseModel):
    status              : int
    
    class Config:
        orm_mode = True
        
        
class CineamaProfileSchema(BaseModel):
    cinema_id           : int
    
    class Config:
        orm_mode = True
        
        
class AdminNotifSchema(BaseModel):
    admin_id            : int
    notif_token         : str
    
    class Config:
        orm_mode = True