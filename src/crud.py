from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from models import (
    AdminType, Admin, Users, Profiles, Posts, CardUsers, Categories, PhoneNumbers, Tags, addProfiles, 
    PhoneNumberSchema, TagsSchema, Images, Galleries, Banners, BannersSchema, Ads, AdsSchema, PostsSchema, 
    PopUp, PopUpSchema, Inbox, AnsweredMessages, Answers, SendUser, InboxSchema, AnsweredMessageSchema, 
    CertificateSchema, Certificates, CertificateStatusSchema, PromoCodes, PromoCodeSchema, PromoCodeStatusSchema,
    InterestItems, UserInterests, Constants, ConstantsSchema, Interests, InterestsSchema, InterestItemsSchema,
    UpdateInterestItemsSchema, CardInsertSchema, CardUpdateSchema, ProfileView, AdsView, Ads2Profile_count, 
    AppVisitors, AnalyticsSchema, SignupSchema, TicketFilterSchema, TicketBron, TicketStatusUpdateSchema, 
    CineamaProfileSchema, CardUserInboxSchema, AdminNotifSchema)
from models.models import JoinCategoryAds
from tokens import create_access_token
from upload_depends import upload_image, delete_uploaded_image
import random
from datetime import datetime, date, timedelta


def create_admin_type(db: Session, txt):
    new_add = AdminType(
        type = txt
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
async def read_admin_type(db: Session):
    result = db.query(
        AdminType.id,
        AdminType.type
    ).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_admin(db: Session, username, password):
    result = db.query(
        Admin.id,
        Admin.token,
        AdminType.type
    )
    result = result.join(AdminType, AdminType.id == Admin.type)
    result = result.filter(
        and_(
            Admin.username == username,
            Admin.password == password    
        )).first()
    db.close()
    if result:
        return result
    else:
        return None
    
def read_count_users(db: Session):
    return db.query(Users).filter(Users.id > 0).count()
 
def read_count_profiles(db: Session):
    return db.query(Profiles).filter(Profiles.id > 0).count()
    
def read_count_posts(db: Session):
    return db.query(Posts).filter(Posts.id > 0).count()
    
def read_count_card_users(db: Session):
    return db.query(CardUsers).filter(CardUsers.id > 0).count()

    
async def create_admin(db: Session, req: SignupSchema):
    dict = {
        "username" : req.username,
        "password" : req.password
    }
    jwt_token = create_access_token(data=dict)
    if not jwt_token:
        return None
    new_add = Admin(**req.dict(), token = jwt_token)
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return jwt_token
    else:
        return None
    
async def read_profile(db: Session, page, category):
    get_zero = db.query(Profiles.id).filter(Profiles.id == 0).first()
    db.close()
    if not get_zero:
        new_add = Profiles(id = 0)
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.like,
        Profiles.dislike,
        Profiles.instagram,
        Profiles.site,
        Profiles.location,
        Profiles.address,
        Profiles.is_cash,
        Profiles.is_terminal,
        Profiles.work_hours,
        Profiles.delivery,
        Profiles.cousineTM,
        Profiles.cousineRU,
        Profiles.average_check,
        Profiles.is_active_card,
        Profiles.tm_muse_card,
        Profiles.is_certificate,
        Profiles.is_VIP,
        Profiles.is_promo,
        Profiles.WiFi,
        Profiles.status,
        Profiles.category_id,
        Profiles.cinema_id,
        Profiles.view_count,
        Profiles.promo_count,
        Profiles.descriptionTM,
        Profiles.descriptionRU,
        Profiles.order_in_list,
        Profiles.free_time,
        Profiles.required_promotion,
        Profiles.own_promotion,
        Profiles.created_at,
        Profiles.updated_at 
    )
    if category > 0:
        result = result.join(Categories, Categories.id == Profiles.category_id)
    if category > 0:
        result = result.filter(Profiles.category_id == category)
    result_count = result.count()
    result = result.order_by(desc(Profiles.id)).offset(20 * (page-1)).limit(20).all()
    db.close()
    newList = []
    for res in result:
        res = dict(res)
        get_tags = db.query(
            Tags.id,
            Tags.tagTM,
            Tags.tagRU
        ).filter(Tags.profile_id == res["id"]).all()
        db.close()
        get_phone_numbers = db.query(PhoneNumbers.id, PhoneNumbers.phone_number)\
        .filter(PhoneNumbers.profile_id == res["id"]).all()
        db.close()
        get_sliders = db.query(Images.id, Images.large_image, Images.small_image, Images.isVR)\
        .filter(Images.profile_id == res["id"]).all()
        db.close()
        get_galleries = db.query(Galleries.id, Galleries.large_image, Galleries.medium_image)\
        .filter(Galleries.profile_id == res["id"]).all()
        db.close()
        if get_tags:
            res["tags"] = get_tags
        if get_phone_numbers:
            res["phone_numbers"] = get_phone_numbers
        if get_sliders:
            res["sliders"] = get_sliders
        if get_galleries:
            res["galleries"] = get_galleries
        newList.append(res)
    result = newList
    final = {}
    final["profiles"] = result
    final["page_count"] = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
        
async def read_name_profile(db: Session):
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU
    ).all()
    db.close()
    if result:
        return result
    else:
        return None

async def create_profile(db: Session, profile: addProfiles):
    new_add = Profiles(**profile.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    dictionary = {}
    dictionary["profile_id"] = new_add.id
    dictionary["category_id"] = profile.category_id
    if new_add:
        return dictionary
    else:
        return None
    
async def update_profile(db: Session, req: addProfiles, id):
    new_update = db.query(Profiles).filter(Profiles.id == id).\
        update({
            Profiles.nameTM             : req.nameTM,
            Profiles.nameRU             : req.nameRU,
            Profiles.short_descTM       : req.short_descTM,
            Profiles.short_descRU       : req.short_descRU,
            Profiles.like               : req.like,
            Profiles.dislike            : req.dislike,
            Profiles.instagram          : req.instagram,
            Profiles.site               : req.site,
            Profiles.location           : req.location,
            Profiles.address            : req.address,
            Profiles.is_cash            : req.is_cash,
            Profiles.is_terminal        : req.is_terminal,
            Profiles.work_hours         : req.work_hours,
            Profiles.delivery           : req.delivery,
            Profiles.cousineTM          : req.cousineTM,
            Profiles.cousineRU          : req.cousineRU,
            Profiles.average_check      : req.average_check,
            Profiles.is_active_card     : req.is_active_card,
            Profiles.tm_muse_card       : req.tm_muse_card,
            Profiles.is_certificate     : req.is_certificate,
            Profiles.is_promo           : req.is_promo,
            Profiles.status             : req.status,
            Profiles.category_id        : req.category_id,
            Profiles.view_count         : req.view_count,
            Profiles.promo_count        : req.promo_count,
            Profiles.descriptionTM      : req.descriptionTM,
            Profiles.descriptionRU      : req.descriptionRU,
            Profiles.order_in_list      : req.order_in_list,
            Profiles.free_time          : req.free_time,
            Profiles.required_promotion : req.required_promotion,
            Profiles.is_VIP             : req.is_VIP,
            Profiles.WiFi               : req.WiFi,
            Profiles.cinema_id          : req.cinema_id,
            Profiles.own_promotion      : req.own_promotion
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
async def delete_profile(db: Session, profile_id):
    # !!! DELETE SLIDERS
    sliders = db.query(
        Images.id,
        Images.small_image,
        Images.large_image
    )\
    .filter(Images.profile_id == profile_id)\
    .all()
    db.close()
    if sliders:
        for slider in sliders:
            if slider.small_image is not None:
                delete_uploaded_image(image_name=slider.small_image)
            if slider.large_image is not None:
                delete_uploaded_image(image_name=slider.large_image)
            db.query(Images).filter(Images.id == slider.id).delete(synchronize_session=False)
            db.commit()
            db.close()
    
    # !!! DELETE GALLERIES
    galleries = db.query(
        Galleries.id,
        Galleries.medium_image,
        Galleries.large_image
    )\
    .filter(Galleries.profile_id == profile_id)\
    .all()
    db.close()
    if galleries:
        for gallery in galleries:
            if gallery.medium_image is not None:
                delete_uploaded_image(image_name=gallery.medium_image)
            if gallery.large_image is not None:
                delete_uploaded_image(image_name=gallery.large_image)
            db.query(Galleries).filter(Galleries.id == gallery.id).delete(synchronize_session=False)
            db.commit()
            db.close()
    
    # !!! DELETE PHONE NUMBERS
    db.query(PhoneNumbers)\
    .filter(PhoneNumbers.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    # !!! DELETE TAGS
    db.query(Tags)\
    .filter(Tags.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    # !!! DELETE BANNERS
    db.query(Banners)\
    .filter(Banners.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    # !!! DELETE TICKET
    db.query(TicketBron)\
    .filter(TicketBron.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    # !!! DELETE PROMO_CODES
    db.query(PromoCodes)\
    .filter(PromoCodes.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    # !!! DELETE CERTIFICATES
    db.query(Certificates)\
    .filter(Certificates.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    
    # !!! DELETE POSTS
    db.query(Posts)\
    .filter(Posts.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    # !!! DELETE ADS
    get_ads = db.query(Ads.id)\
    .filter(Ads.profile_id == profile_id)\
    .all()
    db.close()
    if get_ads:
        for ads in get_ads:
            db.query(JoinCategoryAds).filter(JoinCategoryAds.ads_id == ads.id).delete(synchronize_session=False)
            db.commit()
            db.close()
    db.query(Ads).filter(Ads.profile_id == profile_id).delete(synchronize_session=False)
    db.commit()
    db.close()
    
    
    # !!! DELETE POPUP
    db.query(PopUp)\
    .filter(PopUp.profile_id == profile_id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    
    
    # !!! DELETE PROFILE
    new_delete = db.query(Profiles).filter(Profiles.id == profile_id).delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
async def create_phone_numbers(db: Session, phone: PhoneNumberSchema):
    db.query(PhoneNumbers).filter(PhoneNumbers.profile_id == phone.profile_id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    for phone_numberItem in phone.phone_numbers:
        if phone_numberItem == '':
            continue
        phone_numberItem = phone_numberItem.strip()
        new_add = PhoneNumbers(
            phone_number = phone_numberItem,
            profile_id   = phone.profile_id
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    return True


async def delete_phone_number(db: Session, phone):
    if phone is None:
        phone = ''
    delete = db.query(PhoneNumbers).filter(PhoneNumbers.phone_number == phone)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    if delete:
        return True
    else:
        return False

async def create_tags(db: Session, tag: TagsSchema):
    get_tags = db.query(Tags).filter(Tags.profile_id == tag.profile_id).all()
    db.close()
    if get_tags:
        db.query(Tags).filter(Tags.profile_id == tag.profile_id).delete(synchronize_session=False)
        db.commit()
        db.close()
    
    len1 = len(tag.tagTM)
    len2 = len(tag.tagRU)
    if len1 > len2:
        for i in range(len1 - len2):
            tag.tagRU.append("")
    else:
        for i in range(len2 - len1):
            tag.tagTM.append("")
    for i in range(len1):
        new_add = Tags(
            tagTM = tag.tagTM[i],
            tagRU = tag.tagRU[i],
            category_id = tag.category_id,
            profile_id  = tag.profile_id
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    return True

async def create_category(db: Session, name):
    new_add = Categories(name = name)
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None

async def read_categories(db: Session):
    result = db.query(
        Categories.id,
        Categories.name
    ).all()
    db.close()
    if result:
        return result
    else:
        return None
    
async def read_banner(db: Session, profile_id, page):
    if profile_id is None:
        result = db.query(
            Banners.id,
            Banners.image,
            Banners.link,
            Banners.order,
            Banners.comment_of_admin,
            Banners.profile_id
        )
        result_count = result.count()
        result = result.order_by(desc(Banners.id)).offset(20 * (page-1)).limit(20).all()
        db.close()
    else:
        result = db.query(
            Banners.id,
            Banners.image,
            Banners.link,
            Banners.order,
            Banners.comment_of_admin,
            Banners.profile_id,
            Profiles.nameTM,
            Profiles.nameRU
        )
        result = result.join(Profiles, Banners.profile_id == Profiles.id)
        result = result.filter(Banners.profile_id == profile_id)
        result_count = result.count()
        result = result.offset(20 * (page-1)).limit(20).all()
        db.close()
    final = {}
    final["banners"] = result
    final["page_count"] = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
async def create_banner(db: Session, banner: BannersSchema):
    new_add = Banners(**banner.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
async def update_banner(db: Session, banner: BannersSchema, id):
    new_update = db.query(Banners).filter(Banners.id == id).\
        update({
            Banners.link             : banner.link,
            Banners.order            : banner.order,
            Banners.profile_id       : banner.profile_id,
            Banners.comment_of_admin : banner.comment_of_admin
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
async def update_banner_image(db: Session, id, file):
    banner = db.query(
        Banners.id,
        Banners.image
    ).filter(Banners.id == id).first()
    db.close()

    if banner.image is not None:
        try:
            delete_img = delete_uploaded_image(banner.image)
        except Exception as e:
            print(e)
        

    upload_img = upload_image(directory="banners", file=file)
    if not upload_img:
        return None
        
    new_update = db.query(Banners).filter(Banners.id == id).\
        update({
            Banners.image : upload_img
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
async def delete_banner(db: Session, id):
    get_image = db.query(Banners.image).filter(Banners.id == id).first()
    db.close()
    if get_image.image is not None:
        delete_img = delete_uploaded_image(get_image.image)
        if not delete_img:
            return None
    new_delete = db.query(Banners).filter(Banners.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
async def read_ads(db: Session, page):
    result = db.query(
        Ads.id,
        Ads.nameTM,
        Ads.nameRU,
        Ads.comment_of_admin,
        Ads.image,
        Ads.is_main,
        Ads.site_url,
        Ads.profile_id
    )
    result_count = result.count()
    result = result.order_by(desc(Ads.id)).offset(20 * (page-1)).limit(20).all()
    db.close()
    final = {}
    final["ads"] = result
    final["page_count"] = (result_count // 20) + 1
    if final:
        return final
    else:
        return None

async def create_ads(db: Session, ads: AdsSchema):
    new_add = Ads(**ads.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None  
    
async def update_ads(db: Session, id, ads: AdsSchema):
    new_update = db.query(Ads).filter(Ads.id == id).\
        update({
            Ads.nameTM           : ads.nameTM,
            Ads.nameRU           : ads.nameRU,
            Ads.comment_of_admin : ads.comment_of_admin,
            Ads.is_main          : ads.is_main,
            Ads.site_url         : ads.site_url,
            Ads.profile_id       : ads.profile_id
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
async def delete_ads(db: Session, id):
    ads = db.query(
        Ads.id,
        Ads.image
    ).filter(Ads.id == id).first()
    db.close()
    if ads.image is not None:
        delete_img = delete_uploaded_image(image_name=ads.image)
        if not delete_img:
            return None
    new_delete = db.query(Ads).filter(Ads.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
async def update_ads_image(db: Session, file, id):
    ads = db.query(
        Ads.id,
        Ads.image
    ).filter(Ads.id == id).first()
    db.close()
    if ads.image is not None:
        try:
            delete_img = delete_uploaded_image(image_name=ads.image)
        except Exception as e:
            print(e)


    upload_img = upload_image(directory="ads", file=file)
        
    new_update = db.query(Ads).filter(Ads.id == id).\
        update({
            Ads.image : upload_img
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
async def create_sliders(db: Session, profile_id, file1, file2):
    get_sliders = db.query(
        Images.id,
        Images.large_image,
        Images.small_image
    ).filter(and_(Images.profile_id == profile_id, Images.isVR == False)).all()
    db.close()
    if get_sliders:
        for slider in get_sliders:
            if slider.large_image is not None:
                delete_uploaded_image(image_name=slider.large_image)
            if slider.small_image is not None:
                delete_uploaded_image(image_name=slider.small_image)
        db.query(Images).filter(and_(Images.profile_id == profile_id, Images.isVR == False)).\
            delete(synchronize_session=False)
        db.commit()
        db.close()
    for i in range(len(file1)):
        uploaded_image_name1 = upload_image(directory="sliders/large_images", file=file1[i])
        uploaded_image_name2 = upload_image(directory="sliders/small_images", file=file2[i])
        if not uploaded_image_name1 or not uploaded_image_name2:
            return None
        new_add = Images(
            large_image = uploaded_image_name1,
            small_image = uploaded_image_name2,
            profile_id  = profile_id
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    return True
    

async def create_galleries(db: Session, profile_id, file1, file2):
    get_galleries = db.query(
        Galleries.id,
        Galleries.large_image,
        Galleries.medium_image
    ).filter(Galleries.profile_id == profile_id).all()
    db.close()
    if get_galleries:
        for gallery in get_galleries:
            if gallery.large_image is not None:
                delete_uploaded_image(image_name=gallery.large_image)
            if gallery.medium_image is not None:
                delete_uploaded_image(image_name=gallery.medium_image)
            db.query(Galleries).filter(Galleries.profile_id == profile_id).\
                delete(synchronize_session=False)
            db.commit()
            db.close()
    for i in range(len(file1)):
        uploaded_image_name1 = upload_image(directory="galleries/large_images", file=file1[i])
        uploaded_image_name2 = upload_image(directory="galleries/medium_images", file=file2[i])
        if not uploaded_image_name1 or not uploaded_image_name2:
            return None
        new_add = Galleries(
            large_image     = uploaded_image_name1,
            medium_image    = uploaded_image_name2,
            profile_id      = profile_id
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    return True

        
async def read_posts(db: Session, page, profile_id):
    get_zero = db.query(Posts.id).filter(Posts.id == 0).first()
    db.close()
    if not get_zero:
        new_add = Posts(id = 0)
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    result = db.query(
        Posts.id,
        Posts.titleTM,
        Posts.titleRU,
        Posts.descriptionTM,
        Posts.descriptionRU,
        Posts.comment_of_admin,
        Posts.status,
        Posts.image,
        Posts.promotion,
        Posts.profile_id
    )
    if profile_id is not None:
        result = result.filter(Posts.profile_id == profile_id)
    result_count = result.count()
    result = result.order_by(desc(Posts.id)).offset(20 * (page - 1)).limit(20).all()
    db.close()
    final = {}
    final["posts"]  = result
    final["page_count"]  = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
async def read_all_posts(db: Session):
    result = db.query(
        Posts.id,
        Posts.titleTM,
        Posts.titleRU
    ).all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def create_posts(db: Session, post: PostsSchema):
    new_add = Posts(**post.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
    
async def update_posts(db: Session, post: PostsSchema, id):
    new_update = db.query(Posts).filter(Posts.id == id).\
        update({
            Posts.titleTM          : post.titleTM,
            Posts.titleRU          : post.titleRU,
            Posts.descriptionTM    : post.descriptionTM,
            Posts.descriptionRU    : post.descriptionRU,
            Posts.comment_of_admin : post.comment_of_admin,
            Posts.status           : post.status,
            Posts.promotion        : post.promotion,
            Posts.profile_id       : post.profile_id
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def update_post_image(db: Session, id, file):
    get_image = db.query(Posts.image).filter(Posts.id == id).first()
    db.close()
    if get_image.image is not None:
        delete_uploaded_image(image_name=get_image.image)
    uploaded_img = upload_image(directory="posts", file=file)
    new_update = db.query(Posts).filter(Posts.id == id).\
        update({
            Posts.image : uploaded_img
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    

async def delete_post(db: Session, id):
    post = db.query(Posts.image).filter(Posts.id == id).first()
    db.close()
    if post.image is not None:
        delete_uploaded_image(image_name=post.image)
    new_delete = db.query(Posts).filter(Posts.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
    
async def read_popup(db: Session, page):
    result = db.query(
        PopUp.id,
        PopUp.titleTM,
        PopUp.site_url,
        PopUp.titleTM,
        PopUp.titleRU,
        PopUp.descriptionTM,
        PopUp.descriptionRU,
        PopUp.image,
        PopUp.profile_id,
        PopUp.comment_of_admin,
    )
    result_count = result.count()
    result = result.order_by(desc(PopUp.id)).offset(20 * (page - 1)).limit(20).all()
    db.close()
    final = {}
    final["popup"] = result
    final["page_count"] = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
async def create_popup(db: Session, popup: PopUpSchema):
    new_add = PopUp(**popup.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
async def update_popup(db: Session, id, popup: PopUpSchema):
    tm = popup.descriptionTM.replace(" \n ", " ")
    tm = popup.descriptionTM.replace("\n ", " ")
    tm = popup.descriptionTM.replace(" \n", " ")
    ru = popup.descriptionRU.replace(" \n ", " ")
    ru = popup.descriptionRU.replace("\n ", " ")
    ru = popup.descriptionRU.replace(" \n", " ")
    try:
        new_update = db.query(PopUp).filter(PopUp.id == id).\
            update({
                PopUp.titleTM          : popup.titleTM,
                PopUp.titleRU          : popup.titleRU,
                PopUp.descriptionTM    : tm,
                PopUp.descriptionRU    : ru,
                PopUp.comment_of_admin : popup.comment_of_admin,
                PopUp.site_url         : popup.site_url,
                PopUp.profile_id       : popup.profile_id,
            }, synchronize_session=False)
        db.commit()
        db.close()
    except Exception as e:
        print(e)
    if new_update:
        return True
    else:
        return None
    
async def update_popup_image(db: Session, id, file):
    get_image = db.query(
        PopUp.image
    ).filter(PopUp.id == id).first()
    db.close()
    if get_image.image is not None:
        delete_uploaded_image(image_name=get_image.image)
    uploaded_img = upload_image(directory="popup", file=file)
    new_update = db.query(PopUp).filter(PopUp.id == id).\
        update({
            PopUp.image : uploaded_img
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
async def delete_popup(db: Session, id):
    get_image = db.query(
        PopUp.image
    ).filter(PopUp.id == id).first()
    db.close()
    if get_image.image is not None:
        delete_uploaded_image(image_name=get_image.image)
    new_delete = db.query(PopUp).filter(PopUp.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
async def create_vr_large_image(db: Session, profile_id, file):
    get_vr = db.query(
        Images.large_image,
        Images.small_image
    ).filter(and_(Images.profile_id == profile_id, Images.isVR == True)).first()
    db.close()
    if get_vr:
        if get_vr.large_image is not None:
            delete_uploaded_image(image_name=get_vr.large_image)
        if get_vr.small_image is not None:
            delete_uploaded_image(image_name=get_vr.small_image)
        db.query(Images).filter(and_(Images.profile_id == profile_id, Images.isVR == True)).\
            delete(synchronize_session=False)
        db.commit()
        db.close()
    uploaded_large_img = upload_image(directory="VR/large_images", file=file)
    new_add = Images(
        large_image = uploaded_large_img,
        profile_id  = profile_id,
        isVR        = True
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return True
    else:
        return None
    
async def create_vr_small_image(db: Session, profile_id, file):
    get_vr = db.query(
        Images.id
    ).filter(and_(Images.profile_id == profile_id, Images.isVR == True, Images.small_image == None)).first()
    db.close()
    if get_vr:
        uploaded_small_img = upload_image(directory="VR/small_images", file=file)
        new_update = db.query(Images).filter(Images.id == get_vr.id)\
        .update({
            Images.small_image : uploaded_small_img
        }, synchronize_session=False)
        db.commit()
        db.close()
        if new_update:
            return True
        else:
            return None
    else:
        return None
    
    
async def read_inbox(db: Session):
    inbox_1 = db.query(
        Inbox.id,
        Inbox.title,
        Inbox.message,
        Inbox.is_all,
        Inbox.created_at,
        Inbox.updated_at,
        Users.fullname,
        Users.phone_number
    )
    inbox_1 = inbox_1.join(SendUser, SendUser.inbox_id == Inbox.id)
    inbox_1 = inbox_1.join(Users, Users.id == SendUser.user_id)
    inbox_1 = inbox_1.filter(Inbox.is_all == False)
    inbox_1 = inbox_1.distinct().all()
    db.close()
    inbox_2 = db.query(
        Inbox.id,
        Inbox.title,
        Inbox.message,
        Inbox.is_all,
        Inbox.created_at,
        Inbox.updated_at
    ).filter(Inbox.is_all == True).distinct().all()
    db.close()
    inbox = []
    for inb in inbox_1:
        inbox.append(inb)
    for inb in inbox_2:
        inbox.append(inb)
    answered_messages = db.query(
        AnsweredMessages.id,
        AnsweredMessages.title,
        AnsweredMessages.message,
        AnsweredMessages.created_at,
        AnsweredMessages.updated_at,
        Users.fullname,
        Users.phone_number
    )
    answered_messages = answered_messages.join(Answers, Answers.answered_msg_id == AnsweredMessages.id)
    answered_messages = answered_messages.join(Inbox, Inbox.id == Answers.inbox_id)
    answered_messages = answered_messages.join(SendUser, SendUser.inbox_id == Inbox.id)
    answered_messages = answered_messages.join(Users, Users.id == SendUser.user_id)
    answered_messages = answered_messages.distinct().all()
    db.close()
    if answered_messages:
        for i in answered_messages:
            inbox.append(i)
    inbox = sorted(inbox, key=lambda d: d["id"], reverse=True)
    if inbox:
        return inbox
    else:
        return None
    
    
async def create_inbox(db: Session, inbox: InboxSchema):
    new_add = Inbox(
        title   = inbox["title"],
        message = inbox["message"],
        is_all  = inbox["is_all"]
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if inbox['is_all'] == False:
        new_id_add = SendUser(
            user_id  = inbox["user_id"],
            inbox_id = new_add.id
        )
        db.add(new_id_add)
        db.commit()
        db.refresh(new_id_add)
        db.close()
        if not new_id_add:
            return None
    if new_add:
        return new_add.id
    else:
        return None
    

def create_inbox_tiny(db: Session, title, message, user_id):
    new_add = Inbox(
        title   = title,
        message = message,
        is_all  = False
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    
    new_id_add = SendUser(
        user_id  = user_id,
        inbox_id = new_add.id
    )
    db.add(new_id_add)
    db.commit()
    db.refresh(new_id_add)
    db.close()
    if not new_id_add:
        return None
    if new_add:
        return new_add.id
    else:
        return None
    
    
async def create_answered_message(db: Session, answer: AnsweredMessageSchema):
    new_add = AnsweredMessages(
        title   = answer.title,
        message = answer.message
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if not new_add:
        return None
    new_id_add = Answers(
        answered_msg_id = new_add.id,
        inbox_id        = answer.inbox_id
    )
    db.add(new_id_add)
    db.commit()
    db.refresh(new_id_add)
    db.close()
    if new_id_add:
        return True
    else:
        return None
    
    
async def create_certificate(db: Session, certificate: CertificateSchema):
    new_add = Certificates(**certificate.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    profile = db.query(
        Profiles.nameTM,
        Profiles.nameRU
    )\
    .filter(Profiles.id == certificate.profile_id)\
    .first()
    db.close()
    user = db.query(
        Users.id,
        Users.fullname
    )\
    .filter(Users.id == certificate.user_id)\
    .first()
    db.close()
    if certificate.status == 1:
        txtTM = "Salam, {}!\nSiziň \"{}\" atly alan sertifikatyňyz adminstrasiýa tarapyndan üstünlikli tassyklanyldy.\nSertifikat möçberi: {} TMT \n\n".format(user.fullname, profile.nameTM, certificate.amount)
        txtRU = "Здравствуйте, {}!\nВаш сертификат, полученный \"{}\", успешно одобрен администрацией.\nРазмер сертификата: {} TMT".format(user.fullname, profile.nameTM, certificate.amount)
        title = "Tassyklanyldy / Одобрен"
    elif certificate.status == 0:
        txtTM = "Salam, {}!\nSiziň \"{}\" atly alan sertifikatyňyz üstünlikli hasaba alyndy. Adminstrasiýa tarapyndan tassyklanmagyna garaşyň.\nSertifikat möçberi: {} TMT \n\n".format(user.fullname, profile.nameTM, certificate.amount)
        txtRU = "Здравствуйте {}!\nВаш сертификат \"{}\" успешно зарегистрирован. Дождитесь одобрения администрации.\nСумма сертификата: {} TMT".format(user.fullname, profile.nameRU, certificate.amount)
        title = "Sertifikat / Сертификат"
    txt = txtTM + txtRU
    send = create_inbox_tiny(db=db, title=title, message=txt, user_id=user.id)
    if not send:
        return None
    if new_add:
        return new_add.id
    else:
        return None
    
    
async def read_certificates(db: Session, page):
    result = db.query(
        Certificates.id,
        Certificates.amount,
        Certificates.status,
        Users.id.label("user_id"),
        Users.fullname,
        Users.phone_number,
        Profiles.id.label("profile_id"),
        Profiles.nameTM,
        Profiles.nameRU
    )
    result = result.join(Users, Users.id == Certificates.user_id)
    result = result.join(Profiles, Profiles.id == Certificates.profile_id)
    result_count = result.count()
    result = result.order_by(desc(Certificates.id)).offset(20 * (page - 1)).limit(20).all()
    db.close()
    final = {}
    final["certificates"] = result
    final["page_count"]   = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
    
async def update_certificate(db: Session, id, certificate: CertificateSchema):
    new_update = db.query(Certificates).filter(Certificates.id == id).\
        update({
            Certificates.amount     : certificate.amount,
            Certificates.status     : certificate.status,
            Certificates.profile_id : certificate.profile_id,
            Certificates.user_id    : certificate.user_id
        }, synchronize_session=False)
    db.commit()
    db.close()
    profile = db.query(
        Profiles.nameTM,
        Profiles.nameRU
    )\
    .filter(Profiles.id == certificate.profile_id)\
    .first()
    db.close()
    user = db.query(
        Users.id,
        Users.fullname
    )\
    .filter(Users.id == certificate.user_id)\
    .first()
    db.close()
    if certificate.status == 1:
        txtTM = "Salam, {}!\nSiziň \"{}\" atly alan sertifikatyňyz adminstrasiýa tarapyndan üstünlikli tassyklanyldy.\nSertifikat möçberi: {} TMT \n\n".format(user.fullname, profile.nameTM, certificate.amount)
        txtRU = "Здравствуйте, {}!\nВаш сертификат, полученный \"{}\", успешно одобрен администрацией.\nРазмер сертификата: {} TMT".format(user.fullname, profile.nameTM, certificate.amount)
        title = "Tassyklanyldy / Одобрен"
    elif certificate.status == 0:
        txtTM = "Salam, {}!\nSiziň \"{}\" atly alan sertifikatyňyz adminstrasiýa tarapyndan ýatyryldy.\nSertifikat möçberi: {} TMT".format(user.fullname, profile.nameTM, certificate.amount)
        txtRU = "Здравствуйте, {}!\nВаш сертификат, полученный \"{}\", отменён администрацией.\nРазмер сертификата: {} TMT".format(user.fullname, profile.nameTM, certificate.amount)
        title = "Ýatyryldy / Отменён"
    txt = txtTM + txtRU
    send = create_inbox_tiny(db=db, title=title, message=txt, user_id=user.id)
    if not send:
        return None
    if new_update:
        return True
    else:
        return None
    
async def update_certificate_status(db: Session, id, status: CertificateStatusSchema):
    new_update = db.query(Certificates).filter(Certificates.id == id).\
        update({
            Certificates.status : status.status
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def delete_certificate(db: Session, id):
    new_delete = db.query(Certificates).filter(Certificates.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
    
async def create_promo_codes(db: Session, promo: PromoCodeSchema):
    new_add = PromoCodes(**promo.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
    
async def read_promo_codes(db: Session, page):
    result = db.query(
        PromoCodes.id,
        PromoCodes.promo_code,
        PromoCodes.status,
        Users.id.label("user_id"),
        Users.fullname,
        Users.phone_number,
        Profiles.id.label("profile_id"),
        Profiles.nameTM,
        Profiles.nameRU
    )
    result = result.join(Users, Users.id == PromoCodes.user_id)
    result = result.join(Profiles, Profiles.id == PromoCodes.profile_id)
    result_count = result.count()
    result = result.order_by(desc(PromoCodes.id)).offset(20 * (page - 1)).limit(20).all()
    db.close()
    final = {}
    final["promo_codes"]  = result
    final["page_count"]   = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
    
async def update_promo_code(db: Session, id, promo: PromoCodeSchema):
    new_update = db.query(PromoCodes).filter(PromoCodes.id == id).\
        update({
            PromoCodes.promo_code   : promo.promo_code,
            PromoCodes.status       : promo.status,
            PromoCodes.profile_id   : promo.profile_id,
            PromoCodes.user_id      : promo.user_id
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def update_promo_code_status(db: Session, id, promo: PromoCodeStatusSchema):
    new_update = db.query(PromoCodes).filter(PromoCodes.id == id).\
        update({
            PromoCodes.status : promo.status
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def delete_promo_code(db: Session, id):
    new_delete = db.query(PromoCodes).filter(PromoCodes.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
def read_users(db: Session, page):
    get_zero = db.query(Users).filter(Users.id == 0).first()
    if not get_zero:
        new_add = Users(id = 0)
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
        
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number
    )
    result_count = result.count()
    result = result.order_by(desc(Users.id)).offset(20 * (page - 1)).limit(20).all()
    db.close()
    newList = []
    for res in result:
        res = dict(res)
        get_user_interests = db.query(UserInterests.interest_item_id)\
        .filter(res["id"] == UserInterests.user_id).all()
        db.close()
        newList_item = []
        for get_user in get_user_interests:
            get_interest_items = db.query(
                InterestItems.id,
                InterestItems.titleTM, 
                InterestItems.titleRU
            )\
            .filter(get_user.interest_item_id == InterestItems.id).first()
            db.close()
            newList_item.append(get_interest_items)
        res["interest_items"] = newList_item
        newList.append(res)
    result = newList
        
    final = {}
    final["users"]        = result
    final["page_count"]   = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
    
async def read_user_name(db: Session):
    result = db.query(
        Users.id,
        Users.fullname,
        Users.phone_number,
        Users.token,
        Users.notif_token
    ).all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def create_constants(db: Session, const: ConstantsSchema):
    new_add = Constants(**const.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
    
async def read_constants(db: Session, page):
    result = db.query(
        Constants.id,
        Constants.titleTM,
        Constants.titleRU,
        Constants.contentTM,
        Constants.contentRU,
        Constants.contentTM_dark,
        Constants.contentRU_dark,
        Constants.type
    )
    result_count = result.count()
    result = result.order_by(desc(Constants.id)).offset(20 * (page - 1)).limit(20).all()
    db.close()
    final = {}
    final["constants"]    = result
    final["page_count"]   = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
    
async def update_constants(db: Session, id, const: ConstantsSchema):
    new_update = db.query(Constants).filter(Constants.id == id).\
        update({
            Constants.titleTM        : const.titleTM,
            Constants.titleRU        : const.titleRU,
            Constants.contentTM      : const.contentTM,
            Constants.contentRU      : const.contentRU,
            Constants.contentTM_dark : const.contentTM_dark,
            Constants.contentRU_dark : const.contentRU_dark,
            Constants.type           : const.type
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def delete_constant(db: Session, id):
    new_delete = db.query(Constants).filter(Constants.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
    
async def create_interest(db: Session, interest: InterestsSchema):
    new_add = Interests(**interest.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
async def create_interest_items(db: Session, item: InterestItemsSchema):
    length = len(item.titleTM)
    for i in range(length):
        new_add = InterestItems(
            titleTM     = item.titleTM[i],
            titleRU     = item.titleRU[i],
            interest_id = item.interest_id
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    return True



async def read_interests(db: Session, page):
    subq = db.query(
        func.count(InterestItems.id)
    ).filter(InterestItems.interest_id == Interests.id).label("items_count")
    
    result = db.query(
        Interests.id,
        Interests.titleTM,
        Interests.titleRU,
        subq
    )
    result_count = result.count()
    result = result.order_by(desc(Interests.id)).offset(20 * (page - 1)).limit(20).all()
    db.close()
    new_list = []
    for interest in result:
        interest = dict(interest)
        items = db.query(
            InterestItems.id,
            InterestItems.titleTM,
            InterestItems.titleRU
        ).filter(InterestItems.interest_id == interest["id"]).all()
        db.close()
        interest["items"] = items
        new_list.append(interest)
    result = new_list
    final = {}
    final["interests"]    = result
    final["page_count"]   = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
    
async def update_interest(db: Session, id, interest: InterestsSchema):
    new_update = db.query(Interests).filter(Interests.id == id).\
        update({
            Interests.titleTM : interest.titleTM,
            Interests.titleRU : interest.titleRU
        }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def update_interest_item(db: Session, id, item: UpdateInterestItemsSchema):
    get_items = db.query(InterestItems.id).filter(InterestItems.interest_id == id).all()
    db.close()
    if get_items:
        for items in get_items:
            db.query(InterestItems).filter(InterestItems.id == items.id).\
                delete(synchronize_session=False)
            db.commit()
            db.close()
    length = len(item.titleTM)
    for i in range(length):
        new_add = InterestItems(
            titleTM     = item.titleTM[i],
            titleRU     = item.titleRU[i],
            interest_id = id
        )
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        db.close()
        if not new_add:
            return None
    return True


async def delete_interest(db: Session, id):
    new_delete_interest_item = db.query(InterestItems).\
        filter(InterestItems.interest_id == id).\
            delete(synchronize_session=False)
    db.commit()
    db.close()
    new_delete_interest = db.query(Interests).filter(Interests.id == id).\
        delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete_interest:
        return True
    else:
        return None
    
    
    
def create_user(db: Session, fullname, phone_number):
    newDict = {
        "fullname"      : fullname,
        "phone_number"  : phone_number
    }
    access_token = create_access_token(data=newDict)
    new_add = Users(
        fullname     = fullname,
        phone_number = phone_number,
        token        = access_token
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
    
    
async def create_card_user(db: Session, card: CardInsertSchema):
    str2date_birth   = datetime.strptime(card.date_of_birth, '%d/%m/%Y').date()
    str2date_expired = datetime.strptime(card.expired, '%d/%m/%Y').date()
    get_user = db.query(Users.id)\
    .filter(Users.phone_number == card.phone_number)\
    .first()
    db.close()
    if not get_user:
        user_creation = create_user(db=db, fullname=card.fullname, phone_number=card.phone_number)
        if user_creation:
            user_id = user_creation
    else:
        user_id = get_user.id
    new_add = CardUsers(
        date_of_birth = str2date_birth,
        expired       = str2date_expired,
        gender        = card.gender,
        email         = card.email,
        is_sms        = card.is_sms,
        status        = card.status,
        card_id       = card.card_id,
        user_id       = user_id,
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    db.close()
    if new_add:
        return new_add.id
    else:
        return None
    
    
async def read_card(db: Session, page):

    result = db.query(
        CardUsers.id,
        CardUsers.date_of_birth,
        CardUsers.expired,
        CardUsers.gender,
        CardUsers.email,
        CardUsers.is_sms,
        CardUsers.status,
        CardUsers.card_id,
        CardUsers.user_id,
        Users.fullname,
        Users.phone_number,

    )
    result = result.join(Users, Users.id == CardUsers.user_id)
    result_count = result.count()
    result = result.order_by(desc(CardUsers.id)).offset(20 * (page - 1)).limit(20).distinct().all()
    db.close()
    final = {}
    final["cards"] = result
    final["page_count"] = (result_count // 20) + 1
    if final:
        return final
    else:
        return None
    
async def update_card(db: Session, id, card: CardUpdateSchema):
    str2date_birth   = datetime.strptime(card.date_of_birth, '%d/%m/%Y')
    str2date_expired = datetime.strptime(card.expired, '%d/%m/%Y')
    new_update = db.query(CardUsers)\
    .filter(CardUsers.id == id)\
    .update({
        CardUsers.date_of_birth : str2date_birth,
        CardUsers.expired       : str2date_expired,
        CardUsers.gender        : card.gender,
        CardUsers.email         : card.email,
        CardUsers.is_sms        : card.is_sms,
        CardUsers.status        : card.status,
        CardUsers.card_id       : card.card_id
    }, synchronize_session=False)
    db.commit()
    db.close()
    if not new_update:
        return None
    
    card_user = await read_current_card_user(db=db, id=id)
    user = await read_current_user(db=db, user_id=card_user["user_id"])
    if card.status == 0:
        title = "Tassyklanmady / Не принято"
        message = f"Hormatly {user['fullname']}! Siziň kartyňyz admin tarapyndan tassyklanýança garaşyň / Уважаемый {user['fullname']}! Подождите, пока ваша карточка будет принята администратором"
    elif card.status == 1:
        title = "Tassyklandy / Принято"
        message = f"Hormatly {user['fullname']}! Siziň kartyňyz admin tarapyndan tassyklandy / Уважаемый {user['fullname']}! Ваша карточка принята администратором"
    new_dict = {
        "title"     : title,
        "message"   : message,
        "is_all"    : False,
        "user_id"   : user.id
    }
    
    new_inbox = await create_inbox(db=db, inbox=new_dict)
    if  new_inbox:
        return True
    else:
        return None
        
    
    
async def read_current_user(db: Session, user_id):
    result = db.query(Users.id, Users.fullname).filter(Users.id == user_id).first()
    if result:
        return result
    else:
        return None    

    
async def read_current_card_user(db: Session, id):
    result = db.query(CardUsers.user_id).filter(CardUsers.id == id).first()
    if result:
        return result
    else:
        return None     

    
async def delete_card(db: Session, id):
    new_delete = db.query(CardUsers)\
    .filter(CardUsers.id == id)\
    .delete(synchronize_session=False)
    db.commit()
    db.close()
    if new_delete:
        return True
    else:
        return None
    
    
async def read_zero_card_users(db: Session):
    result = db.query(CardUsers).filter(CardUsers.status == 0).count()
    if result:
        return result
    else:
        return None
    
# !!! TODAY DASHBOARD
def read_profile_view_count(db: Session):
    return db.query(ProfileView)\
        .filter(func.date(ProfileView.created_at) == datetime.now().date())\
        .count()


def read_app_visitors_count(db: Session):
    return db.query(AppVisitors)\
        .filter(func.date(AppVisitors.created_at) == datetime.now().date())\
        .count()


def read_ads_view_count(db: Session):
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == "ads", 
                func.date(AdsView.created_at) == datetime.now().date()
            )
        )\
        .count()
        
        
def read_post_view_count(db: Session):
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == 'post',
                func.date(AdsView.created_at) == datetime.now().date()
            )
        )\
        .count()

def read_slider_view_count(db: Session):
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == 'banner',
                func.date(AdsView.created_at) == datetime.now().date()
            )
        )\
        .count()

def read_popup_view_count(db: Session):
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == 'popup',
                func.date(AdsView.created_at) == datetime.now().date()
            )
        )\
        .count()

def last_day():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    return yesterday

# !!! YESTERDAY DASHBOARD
def read_profile_view_count_yesterday(db: Session):
    yesterday = last_day()
    return db.query(ProfileView)\
        .filter(func.date(ProfileView.created_at) == yesterday)\
        .count()

def read_app_visitors_count_yesterday(db: Session):
    yesterday = last_day()
    return db.query(AppVisitors)\
        .filter(func.date(AppVisitors.created_at) == yesterday)\
        .count()


def read_ads_view_count_yesterday(db: Session):
    yesterday = last_day()
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == "ads", 
                func.date(AdsView.created_at) == yesterday
            )
        )\
        .count()

def read_post_view_count_yesterday(db: Session):
    yesterday = last_day()
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == 'post',
                func.date(AdsView.created_at) == yesterday
            )
        )\
        .count()

def read_slider_view_count_yesterday(db: Session):
    yesterday = last_day()
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == 'banner',
                func.date(AdsView.created_at) == yesterday
            )
        )\
        .count()
        
def read_popup_view_count_yesterday(db: Session):
    yesterday = last_day()
    return db.query(AdsView)\
        .filter(
            and_(
                AdsView.type == 'popup',
                func.date(AdsView.created_at) == yesterday
            )
        )\
        .count()

   
 
def read_click_view(db: Session, type, profile_id, start_date, end_date):
    
    view_count = db.query(AdsView, AdsView.created_at, AdsView.created_at)
    click_count = db.query(Ads2Profile_count, Ads2Profile_count.created_at, Ads2Profile_count.updated_at)
    if type is not None:
        view_count = view_count.filter(AdsView.type == type)
        click_count = click_count.filter(Ads2Profile_count.type == type)
    if profile_id is not None:
        view_count = view_count.filter(AdsView.profile_id == profile_id)
        click_count = click_count.filter(Ads2Profile_count.profile_id == profile_id)
    
        
    if start_date is not None:
        view_count = view_count.filter(func.date(AdsView.created_at) >= start_date)
        click_count = click_count.filter(func.date(Ads2Profile_count.created_at) >= start_date)        
        
    if end_date is not None:
        view_count = view_count.filter(func.date(AdsView.created_at) <= end_date)
        click_count = click_count.filter(func.date(Ads2Profile_count.created_at) <= end_date)
        
    view_count = view_count.count()
    click_count = click_count.count()
    result = {}
    result["view"] = view_count
    result["click"] = click_count
    if result:
        return result
    else:
        return None
    
def read_analytics(db: Session, req: AnalyticsSchema):
    # * GET ALL PROFILES
    profiles = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.like,
        Profiles.dislike
    )
    if req.profile_id is not None:
        profiles = profiles.filter(Profiles.id == req.profile_id)
    profiles = profiles.all()
    db.close()
    result_list = []
    for profile in profiles:
        
        # * TYPE == PROFILE
        profile_view_count = db.query(ProfileView.created_at).filter(ProfileView.profile_id == profile.id)
        if req.start_date is not None:
            profile_view_count = profile_view_count.filter(func.date(ProfileView.created_at) >= req.start_date)
        if req.end_date is not None:
            profile_view_count = profile_view_count.filter(func.date(ProfileView.created_at) <= req.end_date)
        profile_view_count = profile_view_count.count()
        new_dict = {}
        new_dict["id"] = profile.id
        new_dict["nameTM"] = profile.nameTM 
        new_dict["nameRU"] = profile.nameRU
        new_dict["type"] = "profile"
        new_dict["view_count"] = profile_view_count
        new_dict["click_count"] = 0
        new_dict["like"] = profile.like
        new_dict["dislike"] = profile.dislike
        result_list.append(new_dict)
        
        # * TYPE == POST
        posts_like_dislike = db.query(
            Posts.id,
            Posts.like,
            Posts.dislike
        ).filter(Posts.profile_id == profile.id).first()
        db.close()
        view_click = read_click_view(db=db, type='post', 
                                     profile_id=profile.id, 
                                     start_date=req.start_date, 
                                     end_date=req.end_date)
        view_count: int = view_click.get("view")
        click_count: int = view_click.get("click")
        new_dict = {}
        new_dict["id"] = profile.id
        new_dict["nameTM"] = profile.nameTM 
        new_dict["nameRU"] = profile.nameRU
        new_dict["type"] = "post"
        new_dict["view_count"] = view_count
        new_dict["click_count"] = click_count
        if posts_like_dislike:
            new_dict["like"] = posts_like_dislike.like
            new_dict["dislike"] = posts_like_dislike.dislike
        else:
            new_dict["like"] = 0
            new_dict["dislike"] = 0
        result_list.append(new_dict)
        
        # * TYPE == ADS
        view_click = read_click_view(db=db, type='ads', 
                                     profile_id=profile.id, 
                                     start_date=req.start_date, 
                                     end_date=req.end_date)
        view_count: int = view_click.get("view")
        click_count: int = view_click.get("click")
        new_dict = {}
        new_dict["id"] = profile.id
        new_dict["nameTM"] = profile.nameTM 
        new_dict["nameRU"] = profile.nameRU
        new_dict["type"] = "ads"
        new_dict["view_count"] = view_count
        new_dict["click_count"] = click_count
        new_dict["like"] = 0
        new_dict["dislike"] = 0
        result_list.append(new_dict)
        
        # * TYPE == BANNER
        view_click = read_click_view(db=db, type='banner', 
                                     profile_id=profile.id, 
                                     start_date=req.start_date, 
                                     end_date=req.end_date)
        view_count: int = view_click.get("view")
        click_count: int = view_click.get("click")
        new_dict = {}
        new_dict["id"] = profile.id
        new_dict["nameTM"] = profile.nameTM 
        new_dict["nameRU"] = profile.nameRU
        new_dict["type"] = "banner"
        new_dict["view_count"] = view_count
        new_dict["click_count"] = click_count
        new_dict["like"] = 0
        new_dict["dislike"] = 0
        result_list.append(new_dict)
        
        # * TYPE == POPUP
        view_click = read_click_view(db=db, type='popup', 
                                     profile_id=profile.id, 
                                     start_date=req.start_date, 
                                     end_date=req.end_date)
        view_count: int = view_click.get("view")
        click_count: int = view_click.get("click")
        new_dict = {}
        new_dict["id"] = profile.id
        new_dict["nameTM"] = profile.nameTM 
        new_dict["nameRU"] = profile.nameRU
        new_dict["type"] = "popup"
        new_dict["view_count"] = view_count
        new_dict["click_count"] = click_count
        new_dict["like"] = 0
        new_dict["dislike"] = 0
        result_list.append(new_dict)
    if req.type is not None:
        result_list = filter(lambda dict: dict["type"] == req.type, result_list)
        result_list = list(result_list)
    if req.profile_id is not None:
        result_list = filter(lambda dict: dict["id"] == req.profile_id, result_list)
        result_list = list(result_list)
    if result_list:
        return result_list
    else:
        return None
    
    
async def read_ticket(db: Session, ticket: TicketFilterSchema):
    result = db.query(
        TicketBron.id,
        TicketBron.cinema_id,
        TicketBron.profile_id,
        TicketBron.user_id,
        TicketBron.movie_date,
        TicketBron.movie_time,
        TicketBron.ticket_price,
        TicketBron.ticket_count,
        TicketBron.ticket_discount,
        TicketBron.status,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.descriptionTM,
        Profiles.descriptionRU,
        Users.fullname,
        Users.phone_number,
        TicketBron.created_at,
        TicketBron.updated_at
    )
    result = result.join(Profiles, Profiles.id == TicketBron.profile_id)
    result = result.join(Users, Users.id == TicketBron.user_id)
    if ticket.cinema_id is not None:
        result = result.filter(TicketBron.cinema_id == ticket.cinema_id)    
    if ticket.status is not None:
        result = result.filter(TicketBron.status == ticket.status)
    if ticket.movie_date is not None:
        result = result.filter(TicketBron.movie_date == ticket.movie_date)
    if ticket.profile_id is not None:
        result = result.filter(TicketBron.profile_id == ticket.profile_id)
    result = result.all()
    db.close()
    new_list = []
    for res in result:
        res = dict(res)
        image = await read_images_by_profile_id_isVR_false(db=db, profile_id=res["profile_id"])
        if image:
            res["image"] = image
        new_list.append(res)
    result = new_list
    result = sorted(result, key=lambda d: d["id"], reverse=True)
    if result:
        return result
    else:
        return None
    
    
async def read_images_by_profile_id_isVR_false(db: Session, profile_id):
    result = db.query(
        Images.id,
        Images.small_image,
        Images.large_image,
        Images.isVR
    )
    result = result.filter(Images.profile_id == profile_id)
    result = result.filter(Images.isVR == False).all()
    db.close()
    if result:
        return result
    else:
        return None    

async def update_ticket_status(db: Session, id, ticket: TicketStatusUpdateSchema):
    new_update = db.query(TicketBron)\
    .filter(TicketBron.id == id)\
    .update({
        TicketBron.status : ticket.status
    }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def read_current_ticket(db: Session, id):
    result = db.query(
        TicketBron.id,
        TicketBron.cinema_id,
        TicketBron.profile_id,
        TicketBron.user_id,
        TicketBron.movie_date,
        TicketBron.movie_time,
        TicketBron.ticket_count,
        TicketBron.ticket_discount,
        TicketBron.ticket_price,
        TicketBron.status,
        Profiles.nameTM,
        Profiles.nameRU,
        Profiles.short_descTM,
        Profiles.short_descRU,
        Profiles.descriptionTM,
        Profiles.descriptionRU,
        Users.fullname,
        Users.phone_number,
        TicketBron.created_at,
        TicketBron.updated_at
    )
    result = result.join(Profiles, Profiles.id == TicketBron.profile_id)
    result = result.join(Users, Users.id == TicketBron.user_id)
    result = result.filter(TicketBron.id == id).first()
    db.close()
    result = dict(result)
    image = await read_images_by_profile_id_isVR_false(db=db, profile_id=result["profile_id"])
    if image:
        result["image"] = image
    if result:
        return result
    else:
        return None
    
    
async def read_admin_cinema(db: Session):
    result = db.query(
        Admin.id,
        Admin.username,
        Admin.token
    ).filter(Admin.type == 5).all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def read_cineme_profile(db: Session, cinema: CineamaProfileSchema):
    result = db.query(
        Profiles.id,
        Profiles.nameTM,
        Profiles.nameRU
    ).filter(and_(Profiles.category_id == 2, Profiles.cinema_id == cinema.cinema_id)).all()
    db.close()
    if result:
        return result
    else:
        return None
    
    
async def create_card_user_inbox(db: Session, inbox: CardUserInboxSchema):
    users = db.query(
        CardUsers.user_id
    )\
    .filter(CardUsers.status == 1)\
    .all()
    db.close()
    if users:
        for user in users:
            send = create_inbox_tiny(db=db, title=inbox.title, message=inbox.message, user_id=user.user_id)
            if not send:
                return None
    return True


async def update_admin_notif_token(db: Session, req: AdminNotifSchema):
    new_update = db.query(Admin)\
    .filter(Admin.id == req.admin_id)\
    .update({
        Admin.notif_token : req.notif_token
    }, synchronize_session=False)
    db.commit()
    db.close()
    if new_update:
        return True
    else:
        return None
    
    
async def delete_slider(db: Session, type, id):
    if type == 'image':
        db.query(Images).filter(Images.id == id).delete(synchronize_session=False)
        db.commit()
        db.close()
    elif type == 'gallery':
        db.query(Galleries).filter(Galleries.id == id).delete(synchronize_session=False)
        db.commit()
        db.close()
    else:
        return False
    return True