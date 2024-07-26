
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate


from account import auth
from partner import views
from application.view.search import router as search_router
from application.view.application_view import router as application_router
from middlewares import AuthMiddleware

from config import get_origins


app = FastAPI()
# app.add_middleware(AuthMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix="/api",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)
app.include_router(
    views.partner_app,
    prefix="/api/partner",
    tags=["partner"],
    responses={404: {"description": "Not found"}}
)
# app.mount("/partner", views.partner_app, name="partner")

app.include_router(
    search_router,
    prefix="/api/search",
    tags=["search"],
    responses={404: {"description": "Not found"}}
)

app.include_router(
    application_router,
    prefix="/api/application",
    tags=["application"],
    responses={404: {"description": "Not found"}}
)

add_pagination(app)