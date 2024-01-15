from fastapi import FastAPI
import uvicorn
from db import Base, engine
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import (
    login_router,
    dashboard_router,
    profile_router,
    category_router,
    banner_router,
    ads_router,
    posts_router,
    popup_router,
    inbox_router,
    certificate_router,
    promocode_router,
    users_router,
    push_router,
    constants_router,
    interest_router,
    card_router,
    ticket_router
)

# app = FastAPI(docs_url=None, redoc_url=None)
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(
    middleware=middleware,
    title='TmMuse Admin API'
)

app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")

# origins = ["*"]
# methods = ["*"]
# headers = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=methods,
#     allow_headers=headers,
# )

Base.metadata.create_all(engine)

app.include_router(login_router         , tags=["Login"])
app.include_router(dashboard_router     , tags=["Dashboard"])
app.include_router(profile_router       , tags=["Profiles"])
app.include_router(category_router      , tags=["Categories"])
app.include_router(banner_router        , tags=["Banners"])
app.include_router(ads_router           , tags=["Ads"])
app.include_router(posts_router         , tags=["Posts"])
app.include_router(popup_router         , tags=["PopUp"])
app.include_router(inbox_router         , tags=["Inbox"])
app.include_router(certificate_router   , tags=["Certificate"])
app.include_router(promocode_router     , tags=["Promo Codes"])
app.include_router(users_router         , tags=["Users"])
app.include_router(push_router          , tags=["Push"])
app.include_router(constants_router     , tags=["Constants"])
app.include_router(interest_router      , tags=["Interests"])
app.include_router(card_router          , tags=["Cards"])
app.include_router(ticket_router        , tags=["Ticket"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)