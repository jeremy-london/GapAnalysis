import logging
from db import Database
from fastapi import APIRouter, Request
from models import Bait
from phish_interface import (
    complete_email_html,
    create_bait,
    request_linkedin_html,
    target_homepage_dict,
)

logger = logging.getLogger('router')

router = APIRouter(
    prefix="/mock",
    tags=["mock"],
    responses={404: {"description": "Not found"}},
)


@router.get("/fetch-linkedin-page/{url}")
async def fetch_linkedin_page(request: Request, url: str):
    return request_linkedin_html(url)


@router.get("/bait/{target_name}")
async def bait(request: Request, target_name: str):
    content = create_bait(target_name)
    db: Database = request.app.state.db
    with db.get_session() as session:
        bait = Bait(name=target_name,content=content)
        session.add(bait)
        session.commit()
        session.refresh(bait)
        return {bait.id: bait.content}


@router.get("/email-html/{target_name}")
async def get_email_html(request: Request, target_name: str):
    return complete_email_html(target_homepage_dict[target_name])


@router.get("/welcome")
async def welcome(request: Request):
    return "Welcome"
