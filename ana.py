from fastapi import APIRouter, Request
from phish_interface import request_linkedin_html, create_bait, complete_email_html, target_homepage_dict
import logging

logger = logging.getLogger('router')

router = APIRouter(
    prefix="/mock",
    tags=["mock"],
    responses={404: {"description": "Not found"}},
)

@router.get("/fetch-linkedin-page/{url}")
async def fetch_linkedin_page(request: Request, url:str):
    return request_linkedin_html(url)

@router.get("/bait/{target_name}")
async def bait(request: Request, target_name:str):
    return create_bait(target_name)

@router.get("/email-html/{target_name}")
async def bait(request: Request, target_name:str):
    return complete_email_html(target_homepage_dict[target_name])


@router.get("/welcome")
async def welcome(request: Request):
    return "Welcome"

