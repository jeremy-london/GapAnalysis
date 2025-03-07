import logging

from fastapi import APIRouter

from phish_interface import request_linkedin_html

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mock", tags=["mock"])


@router.get("/fetch-linkedin-page/{url}")
async def fetch_linkedin_page(url: str):
    """Fetch LinkedIn page content."""
    return request_linkedin_html(url)


@router.get("/welcome")
async def welcome():
    return {"message": "Welcome"}
