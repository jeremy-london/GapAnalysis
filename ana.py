from fastapi import APIRouter, Request

import logging

logger = logging.getLogger('router')

router = APIRouter(
    prefix="/mock",
    tags=["mock"],
    responses={404: {"description": "Not found"}},
)


@router.get("/welcome")
async def welcome(request: Request):
    return "Welcome"

