from fastapi import Request
from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

    
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return False
    
    
def check_token(header_param: Request):
    token = header_param.headers.get('Authorization')
    if not token:
        return False
    elif token == "Bearer":
        return False
    else:
        token = token.split('Bearer ')[1]
        return token