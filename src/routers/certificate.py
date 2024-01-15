from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from db import get_db
from tokens import Returns
from models import CertificateSchema, CertificateStatusSchema
import crud


certificate_router = APIRouter()

@certificate_router.post("/add-certificate", dependencies=[Depends(HTTPBearer())])
async def add_certificate(certificate: CertificateSchema, db: Session = Depends(get_db)):
    result = await crud.create_certificate(db=db, certificate=certificate)
    if result:
        return Returns.id(result)
    else:
        return Returns.NOT_INSERTED
    
    
@certificate_router.get("/get-certificates", dependencies=[Depends(HTTPBearer())])
async def get_certificates(page: int, db: Session = Depends(get_db)):
    result = await crud.read_certificates(db=db, page=page)
    if result:
        return Returns.object(result)
    else:
        return Returns.NULL
    
    
@certificate_router.put("/update-certificate", dependencies=[Depends(HTTPBearer())])
async def update_certificate(id: int, certificate: CertificateSchema, db: Session = Depends(get_db)):
    result = await crud.update_certificate(db=db, id=id, certificate=certificate)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@certificate_router.put("/update-certificate-status", dependencies=[Depends(HTTPBearer())])
async def update_certificate_status(id: int, status: CertificateStatusSchema, db: Session = Depends(get_db)):
    result = await crud.update_certificate_status(db=db, id=id, status=status)
    if result:
        return Returns.UPDATED
    else:
        return Returns.NOT_UPDATED
    
    
@certificate_router.delete("/delete-certificate", dependencies=[Depends(HTTPBearer())])
async def delete_certificate(id: int, db: Session = Depends(get_db)):
    result = await crud.delete_certificate(db=db, id=id)
    if result:
        return Returns.DELETED
    else:
        return Returns.NOT_DELETED