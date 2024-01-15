import firebase_admin
from sqlalchemy.orm import Session
from firebase_admin import messaging
from models import cloud_messaging_token, cloud_messaging_topic, cloud_messaging_data
from firebase_admin import credentials
import crud

cred = credentials.Certificate("/home/tmmuse_server/TmMuse_admin/src/cloud_messaging/cloud_messaging_credential.json")
# cred = credentials.Certificate("D:\\Project\\TmMuse_admin\\src\\cloud_messaging\\cloud_messaging_credential.json")
default_app = firebase_admin.initialize_app(cred)

# * Send to token
async def send_to_token(request: cloud_messaging_token):
    message = messaging.Message(
        notification=messaging.Notification(
            title=request.title,
            body=request.body
        ),
        token=request.token
    )
    
    response = messaging.send(message=message)
    print("Successfully sent message to token: ", response)
    

# * Send to topic
async def send_to_topic(request: cloud_messaging_topic, db: Session):
    user_count = crud.read_count_users(db=db)
    if user_count % 1000 != 0:
        user_count = user_count // 1000 + 1
    else:
        user_count = user_count // 1000
    condition = "'topic1' in topics"
    for i in range(user_count - 1):
        condition += f" || 'topic{i + 2}' in topics"
    message = messaging.Message(
        notification=messaging.Notification(
            title=request.title,
            body=request.body
        ),
        condition=condition
    )
    
    response = messaging.send(message=message)
    print("Successfully sent message to topic: ", response)
    
    
    
# * Send to data
async def send_data(request: cloud_messaging_data, db: Session):
    user_count = crud.read_count_users(db=db)
    if user_count % 1000 != 0:
        user_count = user_count // 1000 + 1
    else:
        user_count = user_count // 1000
    condition = "'topic1' in topics"
    for i in range(user_count - 1):
        condition += f" || 'topic{i + 2}' in topics"
    
    if request.profile_id != "":
        send = {"profile_id" : request.profile_id}
    elif request.category_id != "":
        send = {"category_id" : request.category_id}
    else:
        send = {}
        
    message = messaging.Message(
        notification=messaging.Notification(
            title=request.title,
            body=request.body
        ),
        data=send,
        condition=condition
    )
    
    response = messaging.send(message=message)
    print("Successfully sent message to topic: ", response)
    
    
    
# * Send to card users
async def send_topic_to_card_user(request: cloud_messaging_topic, db: Session):
    topic = "card_user"
    message = messaging.Message(
        notification=messaging.Notification(
            title=request.title,
            body=request.body
        ),
        topic=topic
    )
    
    response = messaging.send(message=message)
    print("Successfully sent message to topic: ", response)